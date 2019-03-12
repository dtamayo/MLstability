import rebound
import numpy as np
import pandas as pd
import dask.dataframe as dd
from collections import OrderedDict

def collision(reb_sim, col):
    reb_sim.contents._status = 5
    return 0

def training_data(row, safolder, runfunc, args):
    try:
        sa = rebound.SimulationArchive(safolder+'sa'+row['runstring'])
        sim = sa[0]
    except:
        print("traininst_data_functions.py Error reading " + safolder+'sa'+row['runstring'])
        return None
    
    return runfunc(sim, args)

def gen_training_data(outputfolder, safolder, runfunc, args):
    df = pd.read_csv(outputfolder+"/runstrings.csv", index_col = 0)
    ddf = dd.from_pandas(df, npartitions=24)
    sa = rebound.SimulationArchive(safolder+'sa'+df.loc[0]['runstring'])
    testres = runfunc(sa[0], args) # Choose formatting based on selected runfunc return type
    
    if isinstance(testres, np.ndarray): # for runfuncs that return an np array of time series
        res = ddf.apply(training_data, axis=1, meta=('f0', 'object'), args=(safolder, runfunc, args)).compute(scheduler='processes') # dask meta autodetect fails. Here we're returning a np.array not Series or DataFrame so meta = object
        Nsys = df.shape[0]
        Ntimes = res[0].shape[0]
        Nvals = res[0].shape[1] # Number of values at each time (18 for orbtseries, 6 per planet + 1 for time)
        matrix = np.concatenate(res.values).ravel().reshape((Nsys, Ntimes, Nvals)) 
        np.save(outputfolder+'/trainingdata.npy', matrix)

    if isinstance(testres, pd.Series):
        metadf = pd.DataFrame([testres]) # make single row dataframe to autodetect meta
        res = ddf.apply(training_data, axis=1, meta=metadf, args=(safolder, runfunc, args)).compute(scheduler='processes')
        # meta autodetect should work for simple functions that return a series
        res.to_csv(outputfolder+'/trainingdata.csv')

# write functions to take args and unpack them at top so it's clear what you have to pass in args
def orbtseries(sim, args):
    Norbits = args[0]
    Nout = args[1]
    val = np.zeros((Nout, 19))

    ###############################
    sim.collision_resolve = collision
    sim.ri_whfast.keep_unsynchronized = 1
    ###############################
    # Chunk above should be the same in all runfuncs we write in order to match simarchives
    # Fill in values below
    
    times = np.linspace(0, Norbits*sim.particles[1].P, Nout) # TTV systems don't have ps[1].P=1, so must multiply!
    
    for i, time in enumerate(times):
        try:
            sim.integrate(time, exact_finish_time=0)
        except:
            return val # if there's a collision will return 0s from that point on

        orbits = sim.calculate_orbits()
        for j, o in enumerate(orbits):
            val[i,0] = sim.t
            val[i,6*j+1] = o.a
            val[i,6*j+2] = o.e
            val[i,6*j+3] = o.inc
            val[i,6*j+4] = o.Omega
            val[i,6*j+5] = o.pomega
            val[i,6*j+6] = o.M
    return val

def orbsummaryfeaturesxgb(sim, args):
    Norbits = args[0]
    Nout = args[1]
    window = args[2]

    ###############################
    sim.collision_resolve = collision
    sim.ri_whfast.keep_unsynchronized = 1
    ##############################
    
    times = np.linspace(0, Norbits*sim.particles[1].P, Nout) # TTV systems don't have ps[1].P=1, so must multiply!

    ps = sim.particles
    P0 = ps[1].P
    Nout = len(times)

    a = np.zeros((sim.N,Nout))
    e = np.zeros((sim.N,Nout))
    inc = np.zeros((sim.N,Nout))
    
    beta12 = np.zeros(Nout)
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

        # mutual hill radii since that's what goes into Hill stability
        Rhill12 = ps[1].a*((ps[1].m+ps[2].m)/3.)**(1./3.)
        Rhill23 = ps[2].a*((ps[2].m+ps[3].m)/3.)**(1./3.)
        
        beta12[i] = (ps[2].a - ps[1].a)/Rhill12
        beta23[i] = (ps[3].a - ps[2].a)/Rhill23   
        try:
            sim.integrate(t)
        except:
            break
    
    features = OrderedDict()
    features['t_final_short'] = sim.t/P0
    
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

    return pd.Series(features, index=list(features.keys()))
