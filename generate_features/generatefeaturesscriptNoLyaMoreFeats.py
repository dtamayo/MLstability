import pandas as pd
import numpy as np
import os
import sys
import rebound
import time
from collections import OrderedDict

path = '/scratch/dtamayo/'
icpath = path +'random/initial_conditions/runs/ic'
fcpath = path +'random/final_conditions/runs/fc'

df = pd.read_csv(path+'random/random.csv', index_col=0)

maxorbs = float(sys.argv[1])    # how many orbits to do
Nout = int(sys.argv[2])         # how many output samples
window = int(sys.argv[3])       # number of points to take for the 'window' features

def collision(reb_sim, col):
    reb_sim.contents._status = 5 # causes simulation to stop running and have flag for whether sim stopped due to collision
    return 0

def generate_features(sim):
    t0 = time.time()
    ps = sim.particles
    

    P0 = ps[1].P
    tmax = maxorbs * P0 # number of inner planet orbital periods to integrate
    
    sim.collision_resolve = collision

    #kicksize=1.e-11
    #sim2.particles[2].x += kicksize
    
    E0 = sim.calculate_energy()
    times = np.linspace(0,tmax,Nout)
    
    a = np.zeros((sim.N,Nout))
    e = np.zeros((sim.N,Nout))
    inc = np.zeros((sim.N,Nout))
    
    beta12 = np.zeros( Nout)
    beta23 = np.zeros(Nout)

    Rhill12 = ps[1].a*((ps[1].m+ps[2].m)/3.)**(1./3.)
    Rhill23 = ps[2].a*((ps[2].m+ps[3].m)/3.)**(1./3.)
    
    eHill = [0, Rhill12/ps[1].a, max(Rhill12, Rhill23)/ps[2].a, Rhill23/ps[3].a]
    daOvera = [0, (ps[2].a-ps[1].a)/ps[1].a, min(ps[3].a-ps[2].a, ps[2].a-ps[1].a)/ps[2].a, (ps[3].a-ps[2].a)/ps[3].a]
    
    for i, t in enumerate(times):
        for j in [1,2,3]:
            a[j,i] = ps[j].a
            e[j,i] = ps[j].e
            inc[j,i] = ps[j].inc

        #need to update rhills?
        Rhill12 = ps[1].a*((ps[1].m+ps[2].m)/3.)**(1./3.)
        Rhill23 = ps[2].a*((ps[2].m+ps[3].m)/3.)**(1./3.)
        
        beta12[i] = (ps[2].a - ps[1].a)/Rhill12
        beta23[i] = (ps[3].a - ps[2].a)/Rhill23   
        sim.integrate(t)
    
    features = OrderedDict()
    features['t_final_short'] = sim.t/P0
    Ef = sim.calculate_energy()
    features['Rel_Eerr_short'] = abs((Ef-E0)/E0)




    for string, feature in [("beta12", beta12), ("beta23", beta23)]:
        mean = feature.mean()
        std = feature.std()
        features["avg_"+string] = mean
        features["std_"+string] = std
        features["min_"+string] = min(feature)
        features["max_"+string] = max(feature)

    
    for j in [1,2,3]:
        for string, feature in [('a', a), ('e', e), ('inc', inc)]:
            mean = feature[j].mean()
            std = feature[j].std()
            features['avg_'+string+str(j)] = mean
            features['std_'+string+str(j)] = std
            features['max_'+string+str(j)] = feature[j].max()
            features['min_'+string+str(j)] = feature[j].min()
            features['norm_std_'+string+str(j)] = std/mean
            features['norm_max_'+string+str(j)] = np.abs(feature[j] - mean).max()/mean
            sample = feature[j][:window]
            samplemean = sample.mean()
            features['norm_std_window'+str(window)+'_'+string+str(j)] = sample.std()/samplemean
            features['norm_max_window'+str(window)+'_'+string+str(j)] = np.abs(sample - samplemean).max()/samplemean

        for string, feature in [('eH', e), ('iH', inc)]:
            mean = feature[j].mean()
            std = feature[j].std()

            features['avg_'+string+str(j)] = mean/eHill[j]
            features['std_'+string+str(j)] = std/eHill[j]
            features['max_'+string+str(j)] = feature[j].max()/eHill[j]
            features['min_'+string+str(j)] = feature[j].min()/eHill[j]

        string, feature = ('ecross', e)
        features['avg_'+string+str(j)] = mean/daOvera[j]
        features['std_'+string+str(j)] = std/daOvera[j]
        features['max_'+string+str(j)] = feature[j].max()/daOvera[j]
        features['min_'+string+str(j)] = feature[j].min()/daOvera[j]

        xx = range(a[j].shape[0])
        yy = a[j]/a[j].mean()/features["t_final_short"]
        par = np.polyfit(xx, yy, 1, full=True)
        features['norm_a'+str(j)+'_slope'] = par[0][0]

    t = time.time()
    features['wall_time'] = t-t0
    return pd.Series(features, index=list(features.keys()))

def system(row):
    sim = rebound.Simulation.from_file(icpath+row['runstring'])
    E0 = sim.calculate_energy()
    features = generate_features(sim)
    simf = rebound.Simulation.from_file(fcpath+row['runstring'])
    features['Stable'] = 1 if np.isclose(simf.t, 1.e9) else 0
    features['instability_time'] = simf.t
    features['Rel_Eerr'] = abs((simf.calculate_energy()-E0)/E0)
    features.name = row.name
    return features    

from rebound import InterruptiblePool
def dorows(params):
    start, end, df = params
    first = pd.concat([df.iloc[start], system(df.iloc[start])])
    df_full = pd.DataFrame([first])
    for i in range(start+1,end):
        if i == 11003:
            continue
        df_full = df_full.append(pd.concat([df.iloc[i], system(df.iloc[i])]))
        df_full.to_csv('../csvs/tmp/sifOrbsMore={0}Nout={1}window={2}_'.format(maxorbs, Nout, window)+str(start)+'.csv', encoding='ascii')

simIDmax = 25000 #out of ?
Ncores = 10
Npercore = simIDmax // Ncores
params = [[i*Npercore, (i+1)*Npercore, df] for i in range(Ncores)]
params[-1][1] = simIDmax

pool = InterruptiblePool(Ncores)
pool.map(dorows, params)

starts = [i*Npercore for i in range(Ncores)]
dfs = []
for start in starts:
    dfs.append(pd.read_csv('../csvs/tmp/sifOrbsMore={0}Nout={1}window={2}_'.format(maxorbs, Nout, window)+str(start)+'.csv', index_col=0))
df = pd.concat(dfs)
df.to_csv('../csvs/sifOrbsMore={0}Nout={1}window={2}.csv'.format(maxorbs, Nout, window), encoding='ascii')
