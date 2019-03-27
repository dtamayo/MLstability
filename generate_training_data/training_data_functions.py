import rebound
import numpy as np
import pandas as pd
import dask.dataframe as dd
from collections import OrderedDict
from celmech.poincare import Poincare, PoincareHamiltonian
from celmech import Andoyer, AndoyerHamiltonian
from celmech.resonances import resonant_period_ratios, resonance_intersections_list, resonance_pratio_span
from celmech.transformations import masses_to_jacobi
import itertools

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
            break

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
            sim.integrate(t, exact_finish_time=0)
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

def poincare_from_simulation(sim, average=True):
    ps = sim.particles
    mjac, Mjac = masses_to_jacobi([p.m for p in ps])
    pvars = Poincare(sim.G)
    for i in range(1, sim.N-sim.N_var):
        M = Mjac[i]
        m = mjac[i]
        primary = sim.calculate_com(last=i)
        primary.m = Mjac[i]-ps[i].m
        o = ps[i].calculate_orbit(primary=primary)
        sLambda = np.sqrt(sim.G*M*o.a)
        sGamma = sLambda*(1.-np.sqrt(1.-o.e**2))
        pvars.add(m=m, sLambda=sLambda, l=o.l, sGamma=sGamma, gamma=-o.pomega, M=M)
    if average == True:
        pvars.average_synodic_terms()
    return pvars
    
def findres(sim, i1, i2):
    delta = 0.03
    maxorder = 2
    ps = poincare_from_simulation(sim=sim).particles # get averaged mean motions
    n1 = ps[i1].n
    n2 = ps[i2].n
    
    m1 = ps[i1].m
    m2 = ps[i2].m
    
    Pratio = n2/n1
    if np.isnan(Pratio): # probably due to close encounter where averaging step doesn't converge 
        return np.nan, np.nan, np.nan

    res = resonant_period_ratios(Pratio-delta,Pratio+delta, order=maxorder)
    
    Z = np.sqrt((ps[i1].e*np.cos(ps[i1].pomega) - ps[i2].e*np.cos(ps[i2].pomega))**2 + (ps[i1].e*np.sin(ps[i1].pomega) - ps[i2].e*np.sin(ps[i2].pomega))**2)
    
    maxstrength = 0
    j, k, i1, i2, strength = -1, -1, -1, -1, -1
    for a, b in res:
        s = np.abs(np.sqrt(m1+m2)*Z**((b-a)/2.)/(b*n2 - a*n1))
        #print('{0}:{1}'.format(b, a), (b*n2 - a*n1), s)
        if s > maxstrength:
            j = b
            k = b-a
            i1 = 1
            i2 = 2
            strength=s
            maxstrength = s
            
    return j, k, strength

def ressummaryfeaturesxgb(sim, args):
    Norbits = args[0]
    Nout = args[1]
    
    ###############################
    sim.collision_resolve = collision
    sim.ri_whfast.keep_unsynchronized = 1
    ##############################

    features = OrderedDict()
    ps = sim.particles
    sim.init_megno()
    
    N = sim.N - sim.N_var
    a0 = [0] + [sim.particles[i].a for i in range(1, N)]
    Npairs = int((N-1)*(N-2)/2)
    js, ks, strengths = np.zeros(Npairs, dtype=np.int), np.zeros(Npairs, dtype=np.int), np.zeros(Npairs)
    maxj, maxk, maxi1, maxi2, maxpairindex, maxstrength = -1, -1, -1, -1, -1, -1

    Zcross = np.zeros(Npairs)
    #print('pairindex, i1, i2, j, k, strength')
    for i, [i1, i2] in enumerate(itertools.combinations(np.arange(1, N), 2)):
        js[i], ks[i], strengths[i] = findres(sim, i1, i2)
        Zcross[i] = (ps[int(i2)].a-ps[int(i1)].a)/ps[int(i1)].a
        #print(i, i1, i2, js[i], ks[i], strengths[i])
        if strengths[i] > maxstrength:
            maxj, maxk, maxi1, maxi2, maxpairindex, maxstrength = js[i], ks[i], i1, i2, i, strengths[i]
    
    features['Zcross12'] = Zcross[0]
    features['Zcross13'] = Zcross[1]
    features['Zcross23'] = Zcross[2]
    features['maxj'] = maxj
    features['maxk'] = maxk
    features['maxi1'] = maxi1
    features['maxi2'] = maxi2
    features['maxstrength'] = maxstrength
    
    sortedstrengths = strengths.copy()
    sortedstrengths.sort()
    if sortedstrengths[-1] > 0 and sortedstrengths[-2] > 0:
        features['secondres'] = sortedstrengths[-2]/sortedstrengths[-1]
    else:
        features['secondres'] = -1
        
    #print('max', maxi1, maxi2, maxj, maxk, maxpairindex, maxstrength)
    #print('df (j, k, pairindex):', features['j'], features['k'], features['pairindex'])

    times = np.linspace(0, Norbits*sim.particles[1].P, Nout)

    eminus = np.zeros((Npairs, Nout))
    rebound_Z, rebound_phi = np.zeros((Npairs,Nout)), np.zeros((Npairs,Nout))
    rebound_Zcom, rebound_phiZcom = np.zeros((Npairs,Nout)), np.zeros((Npairs,Nout))
    rebound_Zstar, rebound_dKprime = np.zeros((Npairs,Nout)), np.zeros((Npairs,Nout))
    celmech_Z, celmech_phi = np.zeros(Nout), np.zeros(Nout)
    celmech_Zcom, celmech_phiZcom = np.zeros(Nout), np.zeros(Nout)
    celmech_Zstar, celmech_dKprime = np.zeros(Nout), np.zeros(Nout)

    for i,t in enumerate(times):
        for j, [i1, i2] in enumerate(itertools.combinations(np.arange(1, N), 2)):
            i1, i2 = int(i1), int(i2)
            eminus[j, i] = np.sqrt((ps[i2].e*np.cos(ps[i2].pomega)-ps[i1].e*np.cos(ps[i1].pomega))**2 + (ps[i2].e*np.sin(ps[i2].pomega)-ps[i1].e*np.sin(ps[i1].pomega))**2)
            if js[j] != -1:
                pvars = poincare_from_simulation(sim)
                avars = Andoyer.from_Poincare(pvars, j=js[j], k=ks[j], a10=a0[i1], i1=i1, i2=i2)
                rebound_Z[j, i] = avars.Z
                rebound_phi[j, i] = avars.phi
                rebound_Zcom[j, i] = avars.Zcom
                rebound_phiZcom[j, i] = avars.phiZcom
                rebound_Zstar[j, i] = avars.Zstar
                rebound_dKprime[j, i] = avars.dKprime
        try:
            sim.integrate(t, exact_finish_time=0)
        except:
            break
        
    mask = eminus[0] > 0 # where there are data points in case sim ends early
    times = times[mask]
    eminus = eminus[:, mask]
    rebound_Z, rebound_phi = rebound_Z[:, mask], rebound_phi[:, mask]
    rebound_Zcom, rebound_phiZcom =  rebound_Zcom[:, mask], rebound_phiZcom[:, mask]
    rebound_Zstar, rebound_dKprime = rebound_Zstar[:, mask], rebound_dKprime[:, mask]
    celmech_Z, celmech_phi, celmech_Zcom, celmech_phiZcom = celmech_Z[mask], celmech_phi[mask], celmech_Zcom[mask], celmech_phiZcom[mask]
    celmech_Zstar, celmech_dKprime = celmech_Zstar[mask], celmech_dKprime[mask]
    
    for i, s in zip([0,2], ['12', '23']): # take adjacent ones
        EM = eminus[i]
        Zc = Zcross[i]
        features['EMmed'+s] = np.median(EM)/Zc
        features['EMmax'+s] = EM.max()/Zc
        try:
            p = np.poly1d(np.polyfit(times, EM, 3))
            m = p(times)
            EMdrift = np.abs((m[-1]-m[0])/m[0])
            features['EMdrift'+s] = EMdrift
        except:
            features['EMdrift'+s] = np.nan
        maxindex = (m == m.max()).nonzero()[0][0] # index where cubic polynomial fit to EM reaches max to track long wavelength variations (secular?)
        if EMdrift > 0.1 and (maxindex < 0.01*Nout or maxindex > 0.99*Nout): # don't flag as not capturing secular if Z isn't varying significantly in first place
            features['capseculartscale'+s] = 0
        else:
            features['capseculartscale'+s] = 1
        features['EMdetrendedstd'+s] = pd.Series(EM-m).std()/EM[0]
        rollstd = pd.Series(EM).rolling(window=100).std()
        features['EMrollingstd'+s] = rollstd[100:].median()/EM[0]
        var = [EM[:j].var() for j in range(len(EM))]
        try:
            p = np.poly1d(np.polyfit(times[len(var)//2:], var[len(var)//2:], 1)) # fit only second half to get rid of transient
            features['DiffcoeffEM'+s] = p[1]/Zc**2
        except:
            features['DiffcoeffEM'+s] = np.nan
        features['medvarEM'+s] = np.median(var[len(var)//2:])/Zc**2
        if strengths[i] != -1:
            Z = rebound_Z[i]
            features['Zmed'+s] = np.median(Z)/Zc
            features['Zmax'+s] = rebound_Z[i].max()/Zc
            try:
                p = np.poly1d(np.polyfit(times, Z, 3))
                m = p(times)
                features['Zdetrendedstd'+s] = pd.Series(Z-m).std()/Z[0]
            except:
                features['Zdetrendedstd'+s] = np.nan
            rollstd = pd.Series(Z).rolling(window=100).std()
            features['Zrollingstd'+s] = rollstd[100:].median()/Z[0]
            var = [Z[:j].var() for j in range(len(Z))]
            try:
                p = np.poly1d(np.polyfit(times[len(var)//2:], var[len(var)//2:], 1)) # fit only second half to get rid of transient
                features['DiffcoeffZ'+s] = p[1]/Zc**2
            except:
                features['DiffcoeffZ'+s] = np.nan
            features['medvarZ'+s] = np.median(var[len(var)//2:])/Zc**2
            features['Zcomdrift'+s] = np.max(np.abs(rebound_Zcom[i]-rebound_Zcom[i, 0])/rebound_Zcom[i, 0])
            rollstd = pd.Series(rebound_Zcom[i]).rolling(window=100).std()
            features['Zcomrollingstd'+s] = rollstd[100:].median()/rebound_Zcom[i,0]
            features['phiZcomdrift'+s] = np.max(np.abs(rebound_phiZcom[i]-rebound_phiZcom[i, 0]))
            rollstd = pd.Series(rebound_phiZcom[i]).rolling(window=100).std()
            features['phiZcomrollingstd'+s] = rollstd[100:].median()
            features['Zstardrift'+s] = np.max(np.abs(rebound_Zstar[i]-rebound_Zstar[i, 0])/rebound_Zstar[i, 0])
            rollstd = pd.Series(rebound_Zstar[i]).rolling(window=100).std()
            features['Zstarrollingstd'+s] = rollstd[100:].median()/rebound_Zstar[i,0]
            Zcosphi = Z*np.cos(rebound_phi[i])
            features['Zcosphistd'+s] = Zcosphi.std()/Zc
            features['medZcosphi'+s] = np.median(Zcosphi)/Zc
        else:
            features['Zmed'+s] = -1
            features['Zmax'+s] = -1
            features['Zdetrendedstd'+s] = -1
            features['Zrollingstd'+s] = -1
            features['DiffcoeffZ'+s] = -1
            features['medvarZ'+s] = -1
            features['Zcomdrift'+s] = -1
            features['Zcomrollingstd'+s] = -1
            features['phiZcomdrift'+s] = -1
            features['phiZcomrollingstd'+s] = -1
            features['Zstardrift'+s] = -1
            features['Zstarrollingstd'+s] = -1
            features['Zcosphistd'+s] = -1
            features['medZcosphi'+s] = -1

    features['tlyap'] = 1/sim.calculate_lyapunov()
    return pd.Series(features, index=list(features.keys()))
