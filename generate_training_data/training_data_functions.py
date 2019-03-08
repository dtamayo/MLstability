import rebound
import numpy as np
import pandas as pd
import dask.dataframe as dd

def collision(reb_sim, col):
    reb_sim.contents._status = 5
    return 0

def training_data(row, times, safolder, runfunc):
    try:
        sa = rebound.SimulationArchive(safolder+'sa'+row['runstring'])
        sim = sa[0]
    except:
        print("Error reading " + row['runstring'])
        sim = None
    val = runfunc(sim, times)
    return val

def daskapply(df, times, safolder, runfunc):
    return df.apply(training_data, args=(times, safolder, runfunc), axis=1) 

def gen_training_data(times, tseriesfolder, safolder, runfunc):
    df = pd.read_csv(tseriesfolder+"/labels.csv", index_col = 0)
    ddf = dd.from_pandas(df, npartitions=24)
    res = ddf.map_partitions(daskapply, times, safolder, runfunc, meta = (None, 'i8')).compute(scheduler='processes') 
    
    Nsys = df.shape[0]
    Nvals = res[0].shape[1] # Number of values at each time (18 for orbtseries, 6 per planet + 1 for time)
    matrix = np.concatenate(res.values).ravel().reshape((Nsys, len(times), Nvals)) 
    np.save(tseriesfolder+'/trainingdata.npy', matrix)

def runorbtseries(sim, times):
    val = np.zeros((len(times), 19))

    ###############################
    if sim == None:
        return val
    sim.collision_resolve = collision
    sim.ri_whfast.keep_unsynchronized = 1
    
    for i, time in enumerate(times):
        sim.integrate(time, exact_finish_time=0)
    ###############################
    # Chunk above should be the same in all runfuncs we write in order to match simarchives
    # Fill in values below

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
