import pandas as pd
import numpy as np
import os
import rebound
from collections import OrderedDict

path = '/scratch/dtamayo/'
icpath = path +'random/initial_conditions/runs/ic'
fcpath = path +'random/final_conditions/runs/fc'

df = pd.read_csv(path+'random/random.csv', index_col=0)

maxorbs = 1e4
Nout = 100
window = 10
Navg = 10

def collision(reb_sim, col):
    reb_sim.contents._status = 5 # causes simulation to stop running and have flag for whether sim stopped due to collision
    return 0

def generate_features(sim):
    ps = sim.particles
    
    sim2 = rebound.Simulation()
    sim2.G = sim.G
    for p in ps:
        sim2.add(p)

    P0 = ps[1].P
    tmax = maxorbs * P0 # number of inner planet orbital periods to integrate
    
    sim.collision_resolve = collision
    sim2.collision_resolve = collision

    kicksize=1.e-11
    sim2.particles[2].x += kicksize
    
    E0 = sim.calculate_energy()
    times = np.linspace(0,tmax,Nout)
    
    a = np.zeros((sim.N,Nout))
    e = np.zeros((sim.N,Nout))
    inc = np.zeros((sim.N,Nout))
    e2shadow = np.zeros(Nout)
    
    Rhill12 = ps[1].a*((ps[1].m+ps[2].m)/3.)**(1./3.)
    Rhill23 = ps[2].a*((ps[2].m+ps[3].m)/3.)**(1./3.)
    
    eHill = [0, Rhill12/ps[1].a, max(Rhill12, Rhill23)/ps[2].a, Rhill23/ps[3].a]
    daOvera = [0, (ps[2].a-ps[1].a)/ps[1].a, min(ps[3].a-ps[2].a, ps[2].a-ps[1].a)/ps[2].a, (ps[3].a-ps[2].a)/ps[3].a]
    
    for i, t in enumerate(times):
        for j in [1,2,3]:
            a[j,i] = ps[j].a
            e[j,i] = ps[j].e
            inc[j,i] = ps[j].inc
        e2shadow[i] = sim2.particles[2].e
        sim.integrate(t)
        sim2.integrate(t)
    
    features = OrderedDict()
    features['t_final_short'] = sim.t/P0
    Ef = sim.calculate_energy()
    features['Rel_Eerr_short'] = abs((Ef-E0)/E0)
    
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

    N = min((e[2] > 0).sum(), (e2shadow > 0).sum()) # Number of nonzero entries in each array, in case either go unstable before end of run
    Nfit = N//Navg # N of binned points
    Ntrim = Nfit*Navg # trim array to number that can fit in bins of size Navg
    e2avg = np.average(e[2][:Ntrim].reshape(Nfit, Navg), axis=1) # reshape into Nfit lists of Navg consecutive values and average
    e2shadowavg = np.average(e2shadow[:Ntrim].reshape(Nfit, Navg), axis=1)
    timesavg = np.average(times[:Ntrim].reshape(Nfit, Navg), axis=1)
    e2diff = np.abs(e2avg - e2shadowavg)
    par = np.polyfit(timesavg, np.log10(e2diff), 1, full=True)
    features['Lyapunov_time'] = 1/par[0][0]
    
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
        df_full.to_csv('../csvs/tmp/short_integration_features'+str(start)+'.csv', encoding='ascii')

simIDmax = 15000
Ncores = 10
Npercore = simIDmax // Ncores
params = [[i*Npercore, (i+1)*Npercore, df] for i in range(Ncores)]
params[-1][1] = simIDmax

pool = InterruptiblePool(Ncores)
pool.map(dorows, params)

starts = [i*Npercore for i in range(Ncores)]
dfs = []
for start in starts:
    dfs.append(pd.read_csv('../csvs/tmp/short_integration_features'+str(start)+'.csv', index_col=0))
df = pd.concat(dfs)
df.to_csv('../csvs/short_integration_features.csv', encoding='ascii')

