import rebound
import numpy as np
import pandas as pd
import dask.dataframe as dd
from collections import OrderedDict
from celmech.poincare import Poincare, PoincareHamiltonian
from celmech import Andoyer, AndoyerHamiltonian
from celmech.resonances import resonant_period_ratios, resonance_intersections_list, resonance_pratio_span
from celmech.transformations import masses_to_jacobi
from celmech.andoyer import get_num_fixed_points
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

    try:
        ret = runfunc(sim, args)
    except:
        print('{0} failed'.format(row['runstring']))
        return None
    try:
        return ret[0]
    except:
        return ret

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

    if isinstance(testres, list):
        metadf = pd.DataFrame([testres[0]]) # make single row dataframe to autodetect meta
        res = ddf.apply(training_data, axis=1, meta=metadf, args=(safolder, runfunc, args)).compute(scheduler='processes')
        # meta autodetect should work for simple functions that return a series
        res.to_csv(outputfolder+'/trainingdata.csv')

from scipy.optimize import brenth
def F(e,alpha,gamma):
    """Equation 35 of Laskar & Petit (2017)"""
    denom = np.sqrt(alpha*(1-e*e)+gamma*gamma*e*e)
    return alpha*e -1 + alpha + gamma*e / denom

### start AMD functions

def AMD_crit(sim, i1, i2): # assumes i1.a < i2.a
    ps = sim.particles
    if ps[i1].m == 0. or ps[i2].m == 0:
        return 0 # if one particle is massless, any amount of AMD can take it to e=1, so AMDcrit = 0 (always AMD unstable)

    mu = sim.G*ps[0].m
    alpha = ps[i1].a / ps[i2].a
    gamma = ps[i1].m / ps[i2].m
    LambdaPrime = ps[i2].m * np.sqrt(mu*ps[i2].a)
    curlyC = critical_relative_AMD(alpha,gamma)
    AMD_crit = curlyC * LmbdaOut # Eq 29 C = curlyC*Lambda'

def critical_relative_AMD(alpha,gamma):
    """Equation 29"""
    e0 = np.min((1,1/alpha-1))
    ec = brenth(F,0,e0,args=(alpha,gamma))
    e1c = np.sin(np.arctan(gamma*ec / np.sqrt(alpha*(1-ec*ec))))
    curlyC = gamma*np.sqrt(alpha) * (1-np.sqrt(1-ec*ec)) + (1 - np.sqrt(1-e1c*e1c))
    return curlyC

def compute_AMD(sim):
    pstar = sim.particles[0]
    Ltot = pstar.m * np.cross(pstar.xyz,pstar.vxyz)
    ps = sim.particles[1:]
    Lmbda=np.zeros(len(ps))
    G = np.zeros(len(ps))
    Lhat = np.zeros((len(ps),3))
    for k,p in enumerate(sim.particles[1:]):
        orb = p.calculate_orbit(primary=pstar)
        Lmbda[k] = p.m * np.sqrt(p.a)
        G[k] = Lmbda[k] * np.sqrt(1-p.e*p.e)
        hvec = np.cross(p.xyz,p.vxyz)
        Lhat[k] = hvec / np.linalg.norm(hvec)
        Ltot = Ltot + p.m * hvec
    cosi = np.array([Lh.dot(Ltot) for Lh in Lhat]) / np.linalg.norm(Ltot)
    return np.sum(Lmbda) - np.sum(G * cosi)

def AMD_stable_Q(sim):
    AMD = compute_AMD(sim)
    pstar = sim.particles[0]
    ps = sim.particles[1:]
    for i in range(len(ps)-1):
        pIn = ps[i]
        pOut = ps[i+1]
        orbIn = pIn.calculate_orbit(pstar)
        orbOut = pOut.calculate_orbit(pstar)
        alpha = orbIn.a / orbOut.a
        gamma = pIn.m / pOut.m
        LmbdaOut = pOut.m * np.sqrt(orbOut.a)
        Ccrit = critical_relative_AMD(alpha,gamma)
        C = AMD / LmbdaOut
        if C>Ccrit:
            return False
    return True

def AMD_stability_coefficients(sim):
    AMD = compute_AMD(sim)
    pstar = sim.particles[0]
    ps = sim.particles[1:]
    coeffs = np.zeros(len(ps)-1)
    for i in range(len(ps)-1):
        pIn = ps[i]
        pOut = ps[i+1]
        orbIn = pIn.calculate_orbit(pstar)
        orbOut = pOut.calculate_orbit(pstar)
        alpha = orbIn.a / orbOut.a
        gamma = pIn.m / pOut.m
        LmbdaOut = pOut.m * np.sqrt(orbOut.a)
        Ccrit = critical_relative_AMD(alpha,gamma)
        C = AMD / LmbdaOut
        coeffs[i] = C / Ccrit
    return coeffs

def AMD_stability_coefficient(sim, i1, i2):
    AMD = compute_AMD(sim)
    ps = sim.particles
    pstar = ps[0]
    
    pIn = ps[i1]
    pOut = ps[i2]
    orbIn = pIn.calculate_orbit(pstar)
    orbOut = pOut.calculate_orbit(pstar)
    alpha = orbIn.a / orbOut.a
    gamma = pIn.m / pOut.m
    LmbdaOut = pOut.m * np.sqrt(orbOut.a)
    Ccrit = critical_relative_AMD(alpha,gamma)
    C = AMD / LmbdaOut
    return C / Ccrit

### end AMD functions
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

    if sim.integrator != "whfast":
        sim.integrator = "whfast"
        sim.dt = 2*np.sqrt(3)/100.*sim.particles[1].P
    
    ###############################
    sim.collision_resolve = collision
    sim.ri_whfast.keep_unsynchronized = 1
    sim.ri_whfast.safe_mode = 0
    ###############################
    
    times = np.linspace(0, Norbits*sim.particles[1].P, Nout) # TTV systems don't have ps[1].P=1, so must multiply!

    ps = sim.particles
    P0 = ps[1].P
    Nout = len(times)
        
    features = OrderedDict()
    AMDcoeffs = AMD_stability_coefficients(sim)
    features["C_AMD12"] = AMDcoeffs[0]
    features["C_AMD23"] = AMDcoeffs[1]
    features["C_AMD_max"] = np.max(AMDcoeffs)

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

def findres(sim, i1, i2):
    delta = 0.03
    maxorder = 2
    ps = Poincare.from_Simulation(sim=sim).particles # get averaged mean motions
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

def findres2(sim, i1, i2):
    maxorder = 2
    ps = Poincare.from_Simulation(sim=sim).particles # get averaged mean motions
    n1 = ps[i1].n
    n2 = ps[i2].n

    m1 = ps[i1].m/ps[i1].M
    m2 = ps[i2].m/ps[i2].M

    Pratio = n2/n1
    if np.isnan(Pratio): # probably due to close encounter where averaging step doesn't converge 
        return np.nan, np.nan, np.nan

    delta = 0.03
    minperiodratio = max(Pratio-delta, 0.)
    maxperiodratio = min(Pratio+delta, 0.999) # too many resonances close to 1
    res = resonant_period_ratios(minperiodratio,maxperiodratio, order=2)
    
    Z = np.sqrt((ps[i1].e*np.cos(ps[i1].pomega) - ps[i2].e*np.cos(ps[i2].pomega))**2 + (ps[i1].e*np.sin(ps[i1].pomega) - ps[i2].e*np.sin(ps[i2].pomega))**2)
    Zcross = (ps[i2].a-ps[i1].a)/ps[i1].a
        
    j, k, i1, i2, maxstrength = -1, -1, -1, -1, -1
    for a, b in res:
        s = np.abs(np.sqrt(m1+m2)*(Z/Zcross)**((b-a)/2.)/((b*n2 - a*n1)/n1))
        #print('{0}:{1}'.format(b, a), (b*n2 - a*n1), s)
        if s > maxstrength:
            j = b
            k = b-a
            maxstrength = s
    
    if maxstrength > -1:
        return j, k, maxstrength
    else:
        return np.nan, np.nan, np.nan

def findresv3(sim, i1, i2):
    maxorder = 2
    ps = Poincare.from_Simulation(sim=sim).particles # get averaged mean motions
    n1 = ps[i1].n
    n2 = ps[i2].n

    m1 = ps[i1].m/ps[i1].M
    m2 = ps[i2].m/ps[i2].M

    Pratio = n2/n1
    if np.isnan(Pratio): # probably due to close encounter where averaging step doesn't converge
        return np.nan, np.nan, np.nan

    delta = 0.03
    minperiodratio = max(Pratio-delta, 0.)
    maxperiodratio = min(Pratio+delta, 0.999) # too many resonances close to 1
    res = resonant_period_ratios(minperiodratio,maxperiodratio, order=2)

    Z = np.sqrt((ps[i1].e*np.cos(ps[i1].pomega) - ps[i2].e*np.cos(ps[i2].pomega))**2 + (ps[i1].e*np.sin(ps[i1].pomega) - ps[i2].e*np.sin(ps[i2].pomega))**2)
    Zcross = (ps[i2].a-ps[i1].a)/ps[i1].a

    j, k, i1, i2, maxstrength = -1, -1, -1, -1, -1
    for a, b in res:
        s = np.abs(np.sqrt(m1+m2)*(Z/Zcross)**((b-a)/2.)/((b*n2 - a*n1)/n1))
        #print('{0}:{1}'.format(b, a), (b*n2 - a*n1), s)
        if s > maxstrength:
            j = b
            k = b-a
            maxstrength = s

    return j, k, maxstrength

def normressummaryfeaturesxgb(sim, args):
    ps = sim.particles
    Mstar = ps[0].m
    P1 = ps[1].P

    sim2 = rebound.Simulation()
    sim2.G = 4*np.pi**2
    sim2.add(m=1.)

    for p in ps[1:]: 
        sim2.add(m=p.m/Mstar, P=p.P/P1, e=p.e, inc=p.inc, pomega=p.pomega, Omega=p.Omega, theta=p.theta)

    sim2.move_to_com()
    sim2.integrator="whfast"
    sim2.dt=sim2.particles[1].P*2.*np.sqrt(3)/100.
    return ressummaryfeaturesxgb(sim2, args)

def ressummaryfeaturesxgb(sim, args):
    Norbits = args[0]
    Nout = args[1]
    
    ###############################
    sim.collision_resolve = collision
    sim.ri_whfast.keep_unsynchronized = 1
    sim.ri_whfast.safe_mode = 0
    ##############################

    features = OrderedDict()
    AMDcoeffs = AMD_stability_coefficients(sim)
    features["C_AMD12"] = AMDcoeffs[0]
    features["C_AMD23"] = AMDcoeffs[1]
    features["C_AMD_max"] = np.max(AMDcoeffs)

    ps = sim.particles
    sim.init_megno(seed=0)
    
    N = sim.N - sim.N_var
    a0 = [0] + [sim.particles[i].a for i in range(1, N)]
    Npairs = int((N-1)*(N-2)/2)
    js, ks, strengths = np.zeros(Npairs), np.zeros(Npairs), np.zeros(Npairs)
    maxj, maxk, maxi1, maxi2, maxpairindex, maxstrength = -1, -1, -1, -1, -1, -1

    Zcross = np.zeros(Npairs)
    #print('pairindex, i1, i2, j, k, strength')
    for i, [i1, i2] in enumerate(itertools.combinations(np.arange(1, N), 2)):
        js[i], ks[i], strengths[i] = findresv3(sim, i1, i2)
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
    sortedstrengths.sort() # ascending
    if sortedstrengths[-1] > 0 and sortedstrengths[-2] > 0: # if two strongeest resonances are nonzereo
        features['secondres'] = sortedstrengths[-2]/sortedstrengths[-1] # ratio of strengths
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
                pvars = Poincare.from_Simulation(sim)
                avars = Andoyer.from_Poincare(pvars, j=int(js[j]), k=int(ks[j]), a10=a0[i1], i1=i1, i2=i2)
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

    tlyap = 1./np.abs(sim.calculate_lyapunov())
    if tlyap > Norbits:
        tlyap = Norbits
    features['tlyap'] = tlyap
    features['megno'] = sim.calculate_megno()
    return pd.Series(features, index=list(features.keys()))

def ressummaryfeaturesxgb2(sim, args):
    Norbits = args[0]
    Nout = args[1]
    
    ###############################
    sim.collision_resolve = collision
    sim.ri_whfast.keep_unsynchronized = 1
    sim.ri_whfast.safe_mode = 0
    ##############################

    features = OrderedDict()
    AMDcoeffs = AMD_stability_coefficients(sim)
    features["C_AMD12"] = AMDcoeffs[0]
    features["C_AMD23"] = AMDcoeffs[1]
    features["C_AMD_max"] = np.max(AMDcoeffs)

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
        js[i], ks[i], strengths[i] = findresv3(sim, i1, i2)
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
    P0 = sim.particles[1].P
    times = np.linspace(0, Norbits, Nout)

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
                pvars = Poincare.from_Simulation(sim)
                avars = Andoyer.from_Poincare(pvars, j=js[j], k=ks[j], a10=a0[i1], i1=i1, i2=i2)
                rebound_Z[j, i] = avars.Z
                rebound_phi[j, i] = avars.phi
                rebound_Zcom[j, i] = avars.Zcom
                rebound_phiZcom[j, i] = avars.phiZcom
                rebound_Zstar[j, i] = avars.Zstar
                rebound_dKprime[j, i] = avars.dKprime
        try:
            sim.integrate(t*P0, exact_finish_time=0)
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

    tlyap = 1./np.abs(sim.calculate_lyapunov())/P0
    if tlyap > Norbits:
        tlyap = Norbits
    features['tlyap'] = tlyap
    features['megno'] = sim.calculate_megno()
    return pd.Series(features, index=list(features.keys()))

def fillnan(features, pairs):
    features['tlyap'] = np.nan
    features['megno'] = np.nan

    for i, [label, i1, i2] in enumerate(pairs):
        features['EMmed'+label] = np.nan
        features['EMmax'+label] = np.nan
        features['EMstd'+label] = np.nan
        features['EMslope'+label] = np.nan
        features['cheapEMslope'+label] = np.nan
        features['EMrollingstd'+label] = np.nan
        features['EPmed'+label] = np.nan
        features['EPmax'+label] = np.nan
        features['EPstd'+label] = np.nan
        features['EPslope'+label] = np.nan
        features['cheapEPslope'+label] = np.nan
        features['EProllingstd'+label] = np.nan
        features['Zstarslope'+label] = np.nan
        features['Zstarrollingstd'+label] = np.nan
        features['Zcommed'+label] = np.nan
        features['Zfree'+label] = np.nan
        features['Zstarmed'+label] = np.nan
        features['Zstarstd'+label] = np.nan
        features['Zstarmed'+label] = np.nan
        features['Zstarslope'+label] = np.nan
        features['cheapZstarslope'+label] = np.nan

def fillnanv5(features, pairs):
    features['tlyap'] = np.nan
    features['megno'] = np.nan

    for i, [label, i1, i2] in enumerate(pairs):
        features['EMmed'+label] = np.nan
        features['EMmax'+label] = np.nan
        features['EMstd'+label] = np.nan
        features['EMslope'+label] = np.nan
        features['EMrollingstd'+label] = np.nan
        features['EPmed'+label] = np.nan
        features['EPmax'+label] = np.nan
        features['EPstd'+label] = np.nan
        features['EPslope'+label] = np.nan
        features['EProllingstd'+label] = np.nan
        features['Zstarslope'+label] = np.nan
        features['Zstarrollingstd'+label] = np.nan
        features['Zcommed'+label] = np.nan
        features['Zfree'+label] = np.nan
        features['Zstarmed'+label] = np.nan
        features['Zstarstd'+label] = np.nan
        features['Zstarmed'+label] = np.nan
        features['Zstarslope'+label] = np.nan

def ressummaryfeaturesxgbv4(sim, args):
    Norbits = args[0]
    Nout = args[1]
    ###############################
    sim.collision_resolve = collision
    sim.ri_whfast.keep_unsynchronized = 1
    sim.ri_whfast.safe_mode = 0
    ##############################
    ps = sim.particles
    sim.init_megno()
    N = sim.N - sim.N_var
    a0 = [0] + [sim.particles[i].a for i in range(1, N)]
    Npairs = int((N-1)*(N-2)/2)

    features = resparams(sim, args)
    pairs, nearpair = getpairs(sim)
    
    P0 = ps[1].P
    times = np.linspace(0, Norbits*P0, Nout)
    Z, phi = np.zeros((Npairs,Nout)), np.zeros((Npairs,Nout))
    Zcom, phiZcom = np.zeros((Npairs,Nout)), np.zeros((Npairs,Nout))
    Zstar = np.zeros((Npairs,Nout))
    eminus, eplus = np.zeros((Npairs,Nout)), np.zeros((Npairs, Nout))
    
    features['unstableinNorbits'] = False
    AMD0 = 0
    for p in ps[1:sim.N-sim.N_var]:
        AMD0 += p.m*np.sqrt(sim.G*ps[0].m*p.a)*(1-np.sqrt(1-p.e**2)*np.cos(p.inc))

    AMDerr = np.zeros(Nout)
    for i,t in enumerate(times):
        try:
            sim.integrate(t*P0, exact_finish_time=0)
        except:
            features['unstableinNorbits'] = True
            break
        AMD = 0
        for p in ps[1:sim.N-sim.N_var]:
            AMD += p.m*np.sqrt(sim.G*ps[0].m*p.a)*(1-np.sqrt(1-p.e**2)*np.cos(p.inc))
        AMDerr[i] = np.abs((AMD-AMD0)/AMD0)
        
        for j, [label, i1, i2] in enumerate(pairs):
            #i1 = int(i1); i2 = int(i2)
            eminus[j, i] = np.sqrt((ps[i2].e*np.cos(ps[i2].pomega)-ps[i1].e*np.cos(ps[i1].pomega))**2 + (ps[i2].e*np.sin(ps[i2].pomega)-ps[i1].e*np.sin(ps[i1].pomega))**2) / features['EMcross'+label]
            eplus[j, i] = np.sqrt((ps[i1].m*ps[i1].e*np.cos(ps[i1].pomega) + ps[i2].m*ps[i2].e*np.cos(ps[i2].pomega))**2 + (ps[i1].m*ps[i1].e*np.sin(ps[i1].pomega) + ps[i2].m*ps[i2].e*np.sin(ps[i2].pomega))**2)/(ps[i1].m+ps[i2].m)
            if features['strength'+label] > 0:
                pvars = Poincare.from_Simulation(sim)
                avars = Andoyer.from_Poincare(pvars, j=int(features['j'+label]), k=int(features['k'+label]), a10=a0[i1], i1=i1, i2=i2)
            
                Z[j, i] = avars.Z / features['Zcross'+label]
                phi[j, i] = avars.phi
                Zcom[j, i] = avars.Zcom
                phiZcom[j, i] = avars.phiZcom
                Zstar[j, i] = avars.Zstar / features['Zcross'+label]
            
    fillnan(features, pairs)
    
    Nnonzero = int((eminus[0,:] > 0).sum())
    times = times[:Nnonzero]
    AMDerr = AMDerr[:Nnonzero]
    
    eminus = eminus[:,:Nnonzero]
    eplus = eplus[:,:Nnonzero]
    Z = Z[:,:Nnonzero]
    phi = phi[:,:Nnonzero]
    Zcom = Zcom[:,:Nnonzero]
    phiZcom = phiZcom[:,:Nnonzero]
    Zstar = Zstar[:,:Nnonzero]
    
    # Features with or without resonances:
    tlyap = 1./np.abs(sim.calculate_lyapunov())/P0
    if tlyap > Norbits:
        tlyap = Norbits
    features['tlyap'] = tlyap
    features['megno'] = sim.calculate_megno()
    features['AMDerr'] = AMDerr.max()
    
    for i, [label, i1, i2] in enumerate(pairs):
        EM = eminus[i,:]
        EP = eplus[i,:]
        features['EMmed'+label] = np.median(EM)
        features['EMmax'+label] = EM.max()
        features['EMstd'+label] = EM.std()
        features['EPmed'+label] = np.median(EP)
        features['EPmax'+label] = EP.max()
        features['EPstd'+label] = EP.std()
        
        try:
            m,c  = np.linalg.lstsq(np.vstack([times/P0, np.ones(len(times))]).T, EM)[0]
            features['EMslope'+label] = m # EM/EMcross per orbit so we can compare different length integrations
            last = np.median(EM[-int(Nout/20):])
            features['cheapEMslope'+label] = (last - EM.min())/EM.std() # measure of whether final value of EM is much higher than minimum compared to std to test whether we captured long timescale
        except:
            pass
        
        rollstd = pd.Series(EM).rolling(window=10).std()
        features['EMrollingstd'+label] = rollstd[10:].median()/features['EMmed'+label]
        
        try:
            m,c  = np.linalg.lstsq(np.vstack([times/P0, np.ones(len(times))]).T, EP)[0]
            features['EPslope'+label] = m
            last = np.median(EP[-int(Nout/20):])
            features['cheapEPslope'+label] = (last - EP.min())/EP.std() # measure of whether final value of EM is much higher than minimum compared to std to test whether we captured long timescale
        except:
            pass
            
        rollstd = pd.Series(EP).rolling(window=10).std()
        features['EProllingstd'+label] = rollstd[10:].median()/features['EPmed'+label]
        
        if features['strength'+label] > 0:
            features['Zcommed'+label] = np.median(Zcom[i,:])
            
                
            if np.median(Zstar[i,:]) > 0:
                ZS = Zstar[i,:]
                features['Zstarmed'+label] = np.median(ZS)
                # try this one generically for variation in constants, since all fixed points seem to follow Zstar closely?
                features['Zstarstd'+label] = Zstar[i,:].std()/features['Zstarmed'+label]
                try:
                    m,c  = np.linalg.lstsq(np.vstack([times/P0, np.ones(len(times))]).T, ZS)[0]
                    features['Zstarslope'+label] = m
                    last = np.median(ZS[-int(Nout/20):])
                    features['cheapZstarslope'+label] = (last - ZS.min())/ZS.std() # measure of whether final value of EM is much higher than minimum compared to std to test whether we captured long timescale
                except:
                    pass
    
                rollstd = pd.Series(ZS).rolling(window=10).std()
                features['Zstarrollingstd'+label] = rollstd[10:].median()/features['Zstarmed'+label]
               
                Zx = Z[i,:]*np.cos(phi[i,:])
                Zy = Z[i,:]*np.sin(phi[i,:]) 
                Zfree = np.sqrt((Zx+Zstar)**2 + Zy**2) # Zstar at (-Zstar, 0)
                features['Zfree'+label] = Zfree.std()/features['reshalfwidth'+label] # free Z around Zstar
                
    return pd.Series(features, index=list(features.keys())) 

def ressummaryfeaturesxgbv5(sim, args):
    Norbits = args[0]
    Nout = args[1]
    ###############################
    sim.collision_resolve = collision
    sim.ri_whfast.keep_unsynchronized = 1
    sim.ri_whfast.safe_mode = 0
    ##############################
    ps = sim.particles
    sim.init_megno()
    N = sim.N - sim.N_var
    a0 = [0] + [sim.particles[i].a for i in range(1, N)]
    Npairs = int((N-1)*(N-2)/2)

    features = resparamsv5(sim, args)
    pairs = getpairsv5(sim)
    
    P0 = ps[1].P
    times = np.linspace(0, Norbits*P0, Nout)
    Z, phi = np.zeros((Npairs,Nout)), np.zeros((Npairs,Nout))
    Zcom, phiZcom = np.zeros((Npairs,Nout)), np.zeros((Npairs,Nout))
    Zstar = np.zeros((Npairs,Nout))
    eminus, eplus = np.zeros((Npairs,Nout)), np.zeros((Npairs, Nout))
    
    features['unstableinNorbits'] = False
    AMD0 = 0
    for p in ps[1:sim.N-sim.N_var]:
        AMD0 += p.m*np.sqrt(sim.G*ps[0].m*p.a)*(1-np.sqrt(1-p.e**2)*np.cos(p.inc))

    AMDerr = np.zeros(Nout)
    for i,t in enumerate(times):
        try:
            sim.integrate(t*P0, exact_finish_time=0)
        except:
            features['unstableinNorbits'] = True
            break
        AMD = 0
        for p in ps[1:sim.N-sim.N_var]:
            AMD += p.m*np.sqrt(sim.G*ps[0].m*p.a)*(1-np.sqrt(1-p.e**2)*np.cos(p.inc))
        AMDerr[i] = np.abs((AMD-AMD0)/AMD0)
        
        for j, [label, i1, i2] in enumerate(pairs):
            Zcross = features['EMcross'+label]/np.sqrt(2) # important factor of sqrt(2)!
            #i1 = int(i1); i2 = int(i2)
            eminus[j, i] = np.sqrt((ps[i2].e*np.cos(ps[i2].pomega)-ps[i1].e*np.cos(ps[i1].pomega))**2 + (ps[i2].e*np.sin(ps[i2].pomega)-ps[i1].e*np.sin(ps[i1].pomega))**2) / features['EMcross'+label]
            eplus[j, i] = np.sqrt((ps[i1].m*ps[i1].e*np.cos(ps[i1].pomega) + ps[i2].m*ps[i2].e*np.cos(ps[i2].pomega))**2 + (ps[i1].m*ps[i1].e*np.sin(ps[i1].pomega) + ps[i2].m*ps[i2].e*np.sin(ps[i2].pomega))**2)/(ps[i1].m+ps[i2].m)
            if features['strength'+label] > 0:
                pvars = Poincare.from_Simulation(sim)
                avars = Andoyer.from_Poincare(pvars, j=int(features['j'+label]), k=int(features['k'+label]), a10=a0[i1], i1=i1, i2=i2)
            
                Z[j, i] = avars.Z / Zcross
                phi[j, i] = avars.phi
                Zcom[j, i] = avars.Zcom
                phiZcom[j, i] = avars.phiZcom
                Zstar[j, i] = avars.Zstar / Zcross
            
    fillnanv5(features, pairs)
    
    Nnonzero = int((eminus[0,:] > 0).sum())
    times = times[:Nnonzero]
    AMDerr = AMDerr[:Nnonzero]
    
    eminus = eminus[:,:Nnonzero]
    eplus = eplus[:,:Nnonzero]
    Z = Z[:,:Nnonzero]
    phi = phi[:,:Nnonzero]
    Zcom = Zcom[:,:Nnonzero]
    phiZcom = phiZcom[:,:Nnonzero]
    Zstar = Zstar[:,:Nnonzero]
    
    # Features with or without resonances:
    tlyap = 1./sim.calculate_lyapunov()/P0
    if tlyap < 0 or tlyap > Norbits:
        tlyap = Norbits
    features['tlyap'] = tlyap
    features['megno'] = sim.calculate_megno()
    features['AMDerr'] = AMDerr.max()
    
    for i, [label, i1, i2] in enumerate(pairs):
        EM = eminus[i,:]
        EP = eplus[i,:]
        features['EMmed'+label] = np.median(EM)
        features['EMmax'+label] = EM.max()
        features['EMstd'+label] = EM.std()
        features['EPmed'+label] = np.median(EP)
        features['EPmax'+label] = EP.max()
        features['EPstd'+label] = EP.std()
        
        last = np.median(EM[-int(Nout/20):])
        features['EMslope'+label] = (last - EM.min())/EM.std() # measure of whether final value of EM is much higher than minimum compared to std to test whether we captured long timescale
        
        rollstd = pd.Series(EM).rolling(window=10).std()
        features['EMrollingstd'+label] = rollstd[10:].median()/features['EMmed'+label]
        
        last = np.median(EP[-int(Nout/20):])
        features['EPslope'+label] = (last - EP.min())/EP.std() # measure of whether final value of EM is much higher than minimum compared to std to test whether we captured long timescale
            
        rollstd = pd.Series(EP).rolling(window=10).std()
        features['EProllingstd'+label] = rollstd[10:].median()/features['EPmed'+label]
        
        if features['strength'+label] > 0:
            features['Zcommed'+label] = np.median(Zcom[i,:])
            
                
            if np.median(Zstar[i,:]) > 0:
                ZS = Zstar[i,:]
                features['Zstarmed'+label] = np.median(ZS)
                # try this one generically for variation in constants, since all fixed points seem to follow Zstar closely?
                features['Zstarstd'+label] = Zstar[i,:].std()/features['Zstarmed'+label]
                last = np.median(ZS[-int(Nout/20):])
                features['Zstarslope'+label] = (last - ZS.min())/ZS.std() # measure of whether final value of EM is much higher than minimum compared to std to test whether we captured long timescale
    
                rollstd = pd.Series(ZS).rolling(window=10).std()
                features['Zstarrollingstd'+label] = rollstd[10:].median()/features['Zstarmed'+label]
               
                Zx = Z[i,:]*np.cos(phi[i,:])
                Zy = Z[i,:]*np.sin(phi[i,:]) 
                Zfree = np.sqrt((Zx+Zstar)**2 + Zy**2) # Zstar at (-Zstar, 0)
                features['Zfree'+label] = Zfree.std()#/features['reshalfwidth'+label] # free Z around Zstar
                #For k=1 can always define a Zstar, even w/o separatrix, but here reshalfwidth is nan. So don't  normalize
                
    return pd.Series(features, index=list(features.keys())) 

def getpairs(sim):
    N = sim.N - sim.N_var
    Npairs = int((N-1)*(N-2)/2)
    EMcross = np.zeros(Npairs)
    ps = sim.particles
    #print('pairindex, i1, i2, j, k, strength')
    for i, [i1, i2] in enumerate(itertools.combinations(np.arange(1, N), 2)):
        i1 = int(i1); i2 = int(i2)
        EMcross[i] = (ps[int(i2)].a-ps[int(i1)].a)/ps[int(i1)].a
        
    if EMcross[0] < EMcross[2]: # 0 = '1-2', 2='2-3'
        nearpair = 12 # for visualization and debugging
        pairs = [['near', 1,2], ['far', 2, 3], ['outer', 1, 3]]
    else:
        nearpair = 23
        pairs = [['near', 2, 3], ['far', 1, 2], ['outer', 1, 3]]

    return pairs, nearpair 

def getpairsv5(sim):
    N = sim.N - sim.N_var
    Npairs = int((N-1)*(N-2)/2)
    EMcross = np.zeros(Npairs)
    ps = sim.particles
    #print('pairindex, i1, i2, j, k, strength')
    for i, [i1, i2] in enumerate(itertools.combinations(np.arange(1, N), 2)):
        i1 = int(i1); i2 = int(i2)
        EMcross[i] = (ps[int(i2)].a-ps[int(i1)].a)/ps[int(i1)].a
        
    if EMcross[0] < EMcross[2]: # 0 = '1-2', 2='2-3'
        pairs = [['near', 1,2], ['far', 2, 3], ['outer', 1, 3]]
    else:
        pairs = [['near', 2, 3], ['far', 1, 2], ['outer', 1, 3]]

    return pairs

def resparams(sim, args):
    Norbits = args[0]
    Nout = args[1]

    features = OrderedDict()
    ps = sim.particles
    N = sim.N - sim.N_var
    a0 = [0] + [sim.particles[i].a for i in range(1, N)]
    Npairs = int((N-1)*(N-2)/2)

    pairs, features['nearpair'] = getpairs(sim)
    maxj, maxk, maxi1, maxi2, maxpairindex, maxstrength = -1, -1, -1, -1, -1, -1
    for i, [label, i1, i2] in enumerate(pairs):
        # recalculate with new ordering
        RH = ps[i1].a*((ps[i1].m + ps[i2].m)/ps[0].m)**(1./3.)
        features['beta'+label] = (ps[i2].a-ps[i1].a)/RH
        features['EMcross'+label] = (ps[int(i2)].a-ps[int(i1)].a)/ps[int(i1)].a
        features['Zcross'+label] = features['EMcross'+label] / np.sqrt(2) # IMPORTANT FACTOR OF SQRT(2)! Z = EM/sqrt(2)
        
        features['j'+label], features['k'+label], features['strength'+label] = findresv3(sim, i1, i2) # returns -1s if no res found
        if features['strength'+label] > maxstrength:
            maxj, maxk, maxi1, maxi2, maxpairindex, maxstrength = features['j'+label], features['k'+label], i1, i2, i, features['strength'+label]
        features["C_AMD"+label] = AMD_stability_coefficient(sim, i1, i2)
        
        features['reshalfwidth'+label] = np.nan # so we always populate in case there's no  separatrix
        if features['strength'+label] > 0:
            pvars = Poincare.from_Simulation(sim)
            avars = Andoyer.from_Poincare(pvars, j=int(features['j'+label]), k=int(features['k'+label]), a10=a0[i1], i1=i1, i2=i2)
            Zsepinner = avars.Zsep_inner # always positive, location at (-Zsepinner, 0)
            Zsepouter = avars.Zsep_outer
            Zstar = avars.Zstar
            features['reshalfwidth'+label] = min(Zsepouter-Zstar, Zstar-Zsepinner)
    
    features['maxj'] = maxj
    features['maxk'] = maxk
    features['maxi1'] = maxi1
    features['maxi2'] = maxi2
    features['maxstrength'] = maxstrength
    sortedstrengths = np.array([features['strength'+label] for label in ['near', 'far', 'outer']])
    sortedstrengths.sort() # ascending
    
    if sortedstrengths[-1] > 0 and sortedstrengths[-2] > 0: # if two strongeest resonances are nonzereo
        features['secondres'] = sortedstrengths[-2]/sortedstrengths[-1] # ratio of second largest strength to largest
    else:
        features['secondres'] = -1
            
    return pd.Series(features, index=list(features.keys())) 

def resparamsv5(sim, args):
    Norbits = args[0]
    Nout = args[1]

    features = OrderedDict()
    ps = sim.particles
    N = sim.N - sim.N_var
    a0 = [0] + [sim.particles[i].a for i in range(1, N)]
    Npairs = int((N-1)*(N-2)/2)

    pairs = getpairsv5(sim)
    for i, [label, i1, i2] in enumerate(pairs):
        # recalculate with new ordering
        RH = ps[i1].a*((ps[i1].m + ps[i2].m)/ps[0].m)**(1./3.)
        features['beta'+label] = (ps[i2].a-ps[i1].a)/RH
        features['EMcross'+label] = (ps[int(i2)].a-ps[int(i1)].a)/ps[int(i1)].a
        features['j'+label], features['k'+label], features['strength'+label] = findresv3(sim, i1, i2) # returns -1s if no res found
        features["C_AMD"+label] = AMD_stability_coefficient(sim, i1, i2)
        features['reshalfwidth'+label] = np.nan # so we always populate in case there's no  separatrix
        if features['strength'+label] > 0:
            pvars = Poincare.from_Simulation(sim)
            avars = Andoyer.from_Poincare(pvars, j=int(features['j'+label]), k=int(features['k'+label]), a10=a0[i1], i1=i1, i2=i2)
            Zsepinner = avars.Zsep_inner # always positive, location at (-Zsepinner, 0)
            Zsepouter = avars.Zsep_outer
            Zstar = avars.Zstar
            features['reshalfwidth'+label] = min(Zsepouter-Zstar, Zstar-Zsepinner)
    
    sortedstrengths = np.array([features['strength'+label] for label in ['near', 'far', 'outer']])
    sortedstrengths.sort() # ascending
    
    if sortedstrengths[-1] > 0 and sortedstrengths[-2] > 0: # if two strongeest resonances are nonzereo
        features['secondres'] = sortedstrengths[-2]/sortedstrengths[-1] # ratio of second largest strength to largest
    else:
        features['secondres'] = -1
            
    return pd.Series(features, index=list(features.keys())) 

def restseriesv5(sim, args): # corresponds to ressummaryfeaturesxgbv5
    Norbits = args[0]
    Nout = args[1]
    ###############################
    sim.collision_resolve = collision
    sim.ri_whfast.keep_unsynchronized = 1
    sim.ri_whfast.safe_mode = 0
    ##############################
    ps = sim.particles
    sim.init_megno()
    
    P0 = ps[1].P
    times = np.linspace(0, Norbits*P0, Nout)
   
    features = resparamsv5(sim, args)
    pairs = getpairsv5(sim)

    AMD0 = 0
    N = sim.N - sim.N_var
    a0 = [0] + [ps[i].a for i in range(1, N)]
    for p in ps[1:sim.N-sim.N_var]:
        AMD0 += p.m*np.sqrt(sim.G*ps[0].m*p.a)*(1-np.sqrt(1-p.e**2)*np.cos(p.inc))

    val = np.zeros((Nout, 27))
    for i, time in enumerate(times):
        try:
            sim.integrate(time, exact_finish_time=0)
        except:
            break
        AMD = 0
        for p in ps[1:sim.N-sim.N_var]:
            AMD += p.m*np.sqrt(sim.G*ps[0].m*p.a)*(1-np.sqrt(1-p.e**2)*np.cos(p.inc))
        
        val[i,0] = sim.t  # time

        Ns = 8
        for j, [label, i1, i2] in enumerate(pairs):
            Zcross = features['EMcross'+label]/np.sqrt(2)
            #i1 = int(i1); i2 = int(i2)
            val[i,Ns*j+1] = np.sqrt((ps[i2].e*np.cos(ps[i2].pomega)-ps[i1].e*np.cos(ps[i1].pomega))**2 + (ps[i2].e*np.sin(ps[i2].pomega)-ps[i1].e*np.sin(ps[i1].pomega))**2) / features['EMcross'+label]# eminus
            val[i,Ns*j+2] = np.sqrt((ps[i1].m*ps[i1].e*np.cos(ps[i1].pomega) + ps[i2].m*ps[i2].e*np.cos(ps[i2].pomega))**2 + (ps[i1].m*ps[i1].e*np.sin(ps[i1].pomega) + ps[i2].m*ps[i2].e*np.sin(ps[i2].pomega))**2)/(ps[i1].m+ps[i2].m) # eeplus
            if features['strength'+label] > 0:
                pvars = Poincare.from_Simulation(sim)
                avars = Andoyer.from_Poincare(pvars, j=int(features['j'+label]), k=int(features['k'+label]), a10=a0[i1], i1=i1, i2=i2)
           
                Z = avars.Z
                phi = avars.phi
                Zstar = avars.Zstar
                val[i, Ns*j+3] = Z/Zcross
                val[i, Ns*j+4] = phi
                val[i, Ns*j+5] = avars.Zcom
                val[i, Ns*j+6] = avars.phiZcom
                val[i, Ns*j+7] = Zstar/Zcross
                if not np.isnan(Zstar):
                    Zx = Z*np.cos(phi)
                    Zy = Z*np.sin(phi) 
                    Zfree = np.sqrt((Zx+Zstar)**2 + Zy**2) # Zstar at (-Zstar, 0)
                    val[i, Ns*j+8]= Zfree# features['reshalfwidth'+label] # free Z around Zstar
                    #For k=1 can always define a Zstar, even w/o separatrix, but here reshalfwidth is nan. So don't  normalize

        val[i,25] = np.abs((AMD-AMD0)/AMD0) # AMDerr
        val[i,26] = sim.calculate_megno() # megno

    return val

def fillnanv6(features, pairs):
    features['tlyap'] = np.nan
    features['megno'] = np.nan

    for i, [label, i1, i2] in enumerate(pairs):
        features['EMmed'+label] = np.nan
        features['EMmax'+label] = np.nan
        features['EMstd'+label] = np.nan
        features['EMslope'+label] = np.nan
        features['EMrollingstd'+label] = np.nan
        features['EPmed'+label] = np.nan
        features['EPmax'+label] = np.nan
        features['EPstd'+label] = np.nan
        features['EPslope'+label] = np.nan
        features['EProllingstd'+label] = np.nan

def ressummaryfeaturesxgbv6(sim, args): # don't use features that require transform to res variables in tseries
    Norbits = args[0]
    Nout = args[1]
    if sim.integrator != "whfast":
        sim.integrator = "whfast"
        sim.dt = 2*np.sqrt(3)/100.*sim.particles[1].P
    ###############################
    sim.collision_resolve = collision
    sim.ri_whfast.keep_unsynchronized = 1
    sim.ri_whfast.safe_mode = 0
    ##############################
    ps = sim.particles
    sim.init_megno()
    N = sim.N - sim.N_var
    a0 = [0] + [sim.particles[i].a for i in range(1, N)]
    Npairs = int((N-1)*(N-2)/2)

    features = resparamsv5(sim, args)
    pairs = getpairsv5(sim)
    
    P0 = ps[1].P
    times = np.linspace(0, Norbits*P0, Nout)
    Z, phi = np.zeros((Npairs,Nout)), np.zeros((Npairs,Nout))
    Zcom, phiZcom = np.zeros((Npairs,Nout)), np.zeros((Npairs,Nout))
    Zstar = np.zeros((Npairs,Nout))
    eminus, eplus = np.zeros((Npairs,Nout)), np.zeros((Npairs, Nout))
    
    features['unstableinNorbits'] = False
    AMD0 = 0
    for p in ps[1:sim.N-sim.N_var]:
        AMD0 += p.m*np.sqrt(sim.G*ps[0].m*p.a)*(1-np.sqrt(1-p.e**2)*np.cos(p.inc))

    AMDerr = np.zeros(Nout)
    for i,t in enumerate(times):
        try:
            sim.integrate(t*P0, exact_finish_time=0)
        except:
            features['unstableinNorbits'] = True
            break
        AMD = 0
        for p in ps[1:sim.N-sim.N_var]:
            AMD += p.m*np.sqrt(sim.G*ps[0].m*p.a)*(1-np.sqrt(1-p.e**2)*np.cos(p.inc))
        AMDerr[i] = np.abs((AMD-AMD0)/AMD0)
        
        for j, [label, i1, i2] in enumerate(pairs):
            eminus[j, i] = np.sqrt((ps[i2].e*np.cos(ps[i2].pomega)-ps[i1].e*np.cos(ps[i1].pomega))**2 + (ps[i2].e*np.sin(ps[i2].pomega)-ps[i1].e*np.sin(ps[i1].pomega))**2) / features['EMcross'+label]
            eplus[j, i] = np.sqrt((ps[i1].m*ps[i1].e*np.cos(ps[i1].pomega) + ps[i2].m*ps[i2].e*np.cos(ps[i2].pomega))**2 + (ps[i1].m*ps[i1].e*np.sin(ps[i1].pomega) + ps[i2].m*ps[i2].e*np.sin(ps[i2].pomega))**2)/(ps[i1].m+ps[i2].m)
            
    fillnanv6(features, pairs)
    
    Nnonzero = int((eminus[0,:] > 0).sum())
    times = times[:Nnonzero]
    AMDerr = AMDerr[:Nnonzero]
    
    eminus = eminus[:,:Nnonzero]
    eplus = eplus[:,:Nnonzero]
    
    # Features with or without resonances:
    tlyap = 1./sim.calculate_lyapunov()/P0
    if tlyap < 0 or tlyap > Norbits:
        tlyap = Norbits
    features['tlyap'] = tlyap
    features['megno'] = sim.calculate_megno()
    features['AMDerr'] = AMDerr.max()
    
    for i, [label, i1, i2] in enumerate(pairs):
        EM = eminus[i,:]
        EP = eplus[i,:]
        features['EMmed'+label] = np.median(EM)
        features['EMmax'+label] = EM.max()
        features['EMstd'+label] = EM.std()
        features['EPmed'+label] = np.median(EP)
        features['EPmax'+label] = EP.max()
        features['EPstd'+label] = EP.std()
        
        last = np.median(EM[-int(Nout/20):])
        features['EMslope'+label] = (last - EM.min())/EM.std() # measure of whether final value of EM is much higher than minimum compared to std to test whether we captured long timescale
        
        rollstd = pd.Series(EM).rolling(window=10).std()
        features['EMrollingstd'+label] = rollstd[10:].median()/features['EMmed'+label]
        
        last = np.median(EP[-int(Nout/20):])
        features['EPslope'+label] = (last - EP.min())/EP.std() # measure of whether final value of EM is much higher than minimum compared to std to test whether we captured long timescale
            
        rollstd = pd.Series(EP).rolling(window=10).std()
        features['EProllingstd'+label] = rollstd[10:].median()/features['EPmed'+label]
        
    return pd.Series(features, index=list(features.keys())) 

def spock_features_test(sim, args): # final cut down list
    Norbits = args[0]
    Nout = args[1]
    i1 = 1
    i2 = 2
    i3 = 3
    ps  = sim.particles

    spock_error_check(sim, Norbits, Nout,  i1, i2, i3)
    features = OrderedDict()
    pairs = spock_3p_pairs(sim, [i1, i2, i3])
    for i, [label, i1, i2] in enumerate(pairs):
        features['EMstd'+label] = np.nan
        features['EPstd'+label] = np.nan
        features['AMDcrit'+label] = np.nan
        features['EMcross'+label] = np.nan
        features['MMRhalfwidth'+label] = np.nan
        features['MMRstrength'+label] = np.nan
    features['MEGNOmed'] = np.nan
    features['MEGNOstd'] = np.nan
    features['AMDmed'] = np.nan
    features['AMDstd'] = np.nan
    features['MMRstrengthratio'] = np.nan
    features['unstableinshortintegration'] = 0

    for i, [label, i1, i2] in enumerate(pairs):
        features['EMcross'+label] = (ps[i2].a-ps[i1].a)/ps[i1].a
        features["AMDcrit"+label] = spock_AMD_crit(sim, i1, i2)

        j, k, features['MMRstrength'+label] = spock_find_strongest_MMR(sim, i1, i2) 
        if not np.isnan(j): # a resonance  was  found. If no strong res nearby, MMRhalfwidth will be nan
            pvars = Poincare.from_Simulation(sim)
            avars = Andoyer.from_Poincare(pvars, j=j, k=k, a10=ps[i1].a, i1=i1, i2=i2)
            features['MMRhalfwidth'+label] = (avars.Zsep_outer-avars.Zstar)*np.sqrt(2) # Want EM half width. Z approx EM/sqrt(2)
  
    if features['MMRstrengthnear'] > 0:
        features['MMRstrengthratio'] = features['MMRstrengthfar']/features['MMRstrengthnear']
    
    tseries = spock_3p_tseries(sim, args)
    if np.isnan(tseries[0,0]) == True:
        features['unstableinshortintegration'] = 1
        return # particles collided in short integration, return all nan

    EMnear = tseries[:, 1]
    EPnear = tseries[:, 2]
    EMfar = tseries[:, 3]
    EPfar = tseries[:, 4]
    AMD = tseries[:, 5]
    MEGNO = tseries[:, 6]

    features['MEGNOmed'] = np.median(MEGNO)
    features['MEGNOstd'] = MEGNO.std()
    features['AMDmed'] = np.median(AMD)
    features['AMDstd'] = AMD.std()
    features['EMstdnear'] = EMnear.std() 
    features['EPstdnear'] = EPnear.std() 
    features['EMstdfar'] = EMfar.std() 
    features['EPstdfar'] = EPfar.std() 

    return pd.Series(features, index=list(features.keys())) 


def spock_AMD_crit(sim, i1, i2): # assumes i1.a < i2.a
    ps = sim.particles
    if ps[i1].m == 0. or ps[i2].m == 0:
        return 0 # if one particle is massless, any amount of AMD can take it to e=1, so AMDcrit = 0 (always AMD unstable)

    mu = sim.G*ps[0].m
    alpha = ps[i1].a / ps[i2].a
    gamma = ps[i1].m / ps[i2].m
    LambdaPrime = ps[i2].m * np.sqrt(mu*ps[i2].a)
    curlyC = critical_relative_AMD(alpha,gamma)
    AMD_crit = curlyC * LambdaPrime # Eq 29 AMD_crit = C = curlyC*Lambda'

    return AMD_crit

def spock_relative_AMD_crit(alpha,gamma):
    """Equation 29"""
    e0 = np.min((1,1/alpha-1))
    ec = brenth(F,0,e0,args=(alpha,gamma))
    e1c = np.sin(np.arctan(gamma*ec / np.sqrt(alpha*(1-ec*ec))))
    curlyC = gamma*np.sqrt(alpha) * (1-np.sqrt(1-ec*ec)) + (1 - np.sqrt(1-e1c*e1c))
    return curlyC

def spock_AMD(sim): 
    ps = sim.particles
    Lx, Ly, Lz = sim.calculate_angular_momentum()
    L = np.sqrt(Lx**2 + Ly**2 + Lz**2)
    Lcirc = 0
    Mint = ps[0].m
    for p in ps[1:sim.N_real]: # the exact choice of which a and masses to use doesn't matter for closely packed systems (only hierarchical)
        mred = p.m*Mint/(p.m+Mint)
        Lcirc += mred * np.sqrt(sim.G*(p.m + Mint)*p.a)
        Mint += p.m
    return Lcirc - L

# sorts out which pair of planets has a smaller EMcross, labels that pair inner, other adjacent pair outer
# returns a list of two lists, with [label (near or far), i1, i2], where i1 and i2 are the indices, with i1 
# having the smaller semimajor axis
def spock_3p_pairs(sim, indices):
    ps = sim.particles
    sortedindices = sorted(indices, key=lambda i: ps[i].a) # sort from inner to outer
    EMcrossInner = (ps[sortedindices[1]].a-ps[sortedindices[0]].a)/ps[sortedindices[0]].a
    EMcrossOuter = (ps[sortedindices[2]].a-ps[sortedindices[1]].a)/ps[sortedindices[1]].a

    if EMcrossInner < EMcrossOuter:
        return [['near', sortedindices[0], sortedindices[1]], ['far', sortedindices[1], sortedindices[2]]]
    else:
        return [['near', sortedindices[1], sortedindices[2]], ['far', sortedindices[0], sortedindices[1]]]

def spock_find_strongest_MMR(sim, i1, i2):
    maxorder = 2
    ps = Poincare.from_Simulation(sim=sim).particles # get averaged mean motions
    n1 = ps[i1].n
    n2 = ps[i2].n

    m1 = ps[i1].m/ps[i1].M
    m2 = ps[i2].m/ps[i2].M

    Pratio = n2/n1
    if np.isnan(Pratio): # probably due to close encounter where averaging step doesn't converge
        return np.nan, np.nan, np.nan

    delta = 0.03
    minperiodratio = max(Pratio-delta, 0.)
    maxperiodratio = min(Pratio+delta, 0.999) # too many resonances close to 1
    res = resonant_period_ratios(minperiodratio,maxperiodratio, order=2)

    Z = np.sqrt((ps[i1].e*np.cos(ps[i1].pomega) - ps[i2].e*np.cos(ps[i2].pomega))**2 + (ps[i1].e*np.sin(ps[i1].pomega) - ps[i2].e*np.sin(ps[i2].pomega))**2)
    Zcross = (ps[i2].a-ps[i1].a)/ps[i1].a

    j, k, maxstrength = np.nan, np.nan, 0 
    for a, b in res:
        s = np.abs(np.sqrt(m1+m2)*(Z/Zcross)**((b-a)/2.)/((b*n2 - a*n1)/n1))
        if s > maxstrength:
            j = b
            k = b-a
            maxstrength = s
    if maxstrength == 0:
        maxstrength = np.nan

    return j, k, maxstrength

def spock_error_check(sim, Norbits, Nout, i1, i2, i3):
    if not isinstance(i1, int) or not isinstance(i2, int) or not isinstance(i3, int):
        raise AttributeError("SPOCK  Error: Particle indices passed to spock_features were not integers")
    ps = sim.particles
    if ps[0].m < 0 or ps[1].m < 0 or ps[2].m < 0 or ps[3].m < 0: 
        raise AttributeError("SPOCK Error: Particles in sim passed to spock_features had negative masses")

    if ps[1].r == 0 or ps[2].r == 0 or ps[3].r == 0.:
        for  p in ps[1:]:
            rH = p.a*(p.m/3./ps[0].m)**(1./3.)
            p.r = rH
    return

# First value in each time series will be np.nan if planets collide within the first Norbits
def spock_3p_tseries(sim, args):
    Norbits = args[0]
    Nout = args[1]
    i1 = 1
    i2 = 2
    i3 = 3

    # AMD calculation is easiest in canonical heliocentric coordiantes, so velocities need to be in barycentric frame
    # Don't want to move_to_com() unless we have to so that we get same chaotic trajectory as user passes
    com = sim.calculate_com()
    if com.x**2 + com.y**2 + com.z**2 + com.vx**2 + com.vy**2 + com.vz**2 > 1.e-16:
        sim.move_to_com()
    
    ###############################
    try:
        sim.collision = 'line' # use line if using newer version of REBOUND
    except:
        sim.collision = 'direct'# fall back for older versions
    sim.collision_resolve = collision
    sim.ri_whfast.keep_unsynchronized = 1
    sim.ri_whfast.safe_mode = 0
    ##############################
    ps = sim.particles
    sim.init_megno()
    
    P0 = ps[1].P
    times = np.linspace(0, Norbits*P0, Nout)
    
    if sim.integrator != "whfast":
        sim.integrator = "whfast"
        sim.dt = 2*np.sqrt(3)/100.*P0
   
    pairs = spock_3p_pairs(sim, [i1, i2, i3])

    val = np.zeros((Nout, 7))
    for i, time in enumerate(times):
        try:
            sim.integrate(time, exact_finish_time=0)
        except:
            val[0,0] = np.nan
            return val

        val[i,0] = sim.t/P0  # time

        Ns = 2
        for j, [label, i1, i2] in enumerate(pairs):
            val[i,Ns*j+1] = np.sqrt((ps[i2].e*np.cos(ps[i2].pomega)-ps[i1].e*np.cos(ps[i1].pomega))**2 + (ps[i2].e*np.sin(ps[i2].pomega)-ps[i1].e*np.sin(ps[i1].pomega))**2) # eminus
            val[i,Ns*j+2] = np.sqrt((ps[i1].m*ps[i1].e*np.cos(ps[i1].pomega) + ps[i2].m*ps[i2].e*np.cos(ps[i2].pomega))**2 + (ps[i1].m*ps[i1].e*np.sin(ps[i1].pomega) + ps[i2].m*ps[i2].e*np.sin(ps[i2].pomega))**2)/(ps[i1].m+ps[i2].m) # eplus

        val[i,5] = spock_AMD(sim)
        val[i,6] = sim.calculate_megno() # megno

    return val

def spock_3p_tseriesv2(sim, args):
    Norbits = args[0]
    Nout = args[1]
    i1 = 1
    i2 = 2
    i3 = 3

    # AMD calculation is easiest in canonical heliocentric coordiantes, so velocities need to be in barycentric frame
    # Don't want to move_to_com() unless we have to so that we get same chaotic trajectory as user passes
    com = sim.calculate_com()
    if com.x**2 + com.y**2 + com.z**2 + com.vx**2 + com.vy**2 + com.vz**2 > 1.e-16:
        sim.move_to_com()
    
    ###############################
    try:
        sim.collision = 'line' # use line if using newer version of REBOUND
    except:
        sim.collision = 'direct'# fall back for older versions
    sim.collision_resolve = collision
    sim.ri_whfast.keep_unsynchronized = 1
    sim.ri_whfast.safe_mode = 0
    ##############################
    ps = sim.particles
    sim.init_megno()
    
    P0 = ps[1].P
    times = np.linspace(0, Norbits*P0, Nout)
    
    if sim.integrator != "whfast":
        sim.integrator = "whfast"
        sim.dt = 2*np.sqrt(3)/100.*P0
   
    pairs = spock_3p_pairs(sim, [i1, i2, i3])
    jk = {}
    a10 = {}
    for [label, i1, i2] in pairs:
        j, k, _ = spock_find_strongest_MMR(sim, i1, i2) 
        if np.isnan(j) == False:
            jk[label] = (j,k)
            a10[label] = ps[i1].a

    val = np.zeros((Nout, 15))
    for i, time in enumerate(times):
        try:
            sim.integrate(time, exact_finish_time=0)
        except:
            val[0,0] = np.nan
            return val

        val[i,0] = sim.t/P0  # time

        Ns = 6
        for q, [label, i1, i2] in enumerate(pairs):
            e1x, e1y = ps[i1].e*np.cos(ps[i1].pomega), -ps[i1].e*np.sin(ps[i1].pomega)
            e2x, e2y = ps[i2].e*np.cos(ps[i2].pomega), -ps[i2].e*np.sin(ps[i2].pomega)
            val[i,Ns*q+1] = np.sqrt((e2x-e1x)**2 + (e2y-e1y)**2)
            val[i,Ns*q+2] = np.sqrt((ps[i1].m*e1x + ps[i2].m*e2x)**2 + (ps[i1].m*e1y + ps[i2].m*e2y)**2)/(ps[i1].m+ps[i2].m)
            try: # it's unlikely but possible for bodies to land nearly on top of  each other midtimestep and get a big kick that doesn't get caught by collisions  post timestep. All these cases are unstable, so flag them as above
                try:
                    j,k = jk[label]
                    # average only affects a (Lambda) Z and I think  Zcom  don't depend on a. Zsep and Zstar slightly, but several sig figs in even when close at conjunction
                    avars = Andoyer.from_Simulation(sim, a10=a10[label], j=j, k=k, i1=i1, i2=i2, average=False)
                    val[i,Ns*q+3] = avars.Z*np.sqrt(2) # EM = Z*sqrt(2)
                    val[i,Ns*q+4] = avars.Zcom # no sqrt(2) factor
                    val[i,Ns*q+5] = (avars.Zsep_outer-avars.Zstar)*np.sqrt(2)
                except: # no nearby resonance, use EM and ecom
                    val[i,Ns*q+3] = np.sqrt((e2x-e1x)**2 + (e2y-e1y)**2)
                    val[i,Ns*q+4] = np.sqrt((ps[i1].m*e1x + ps[i2].m*e2x)**2 + (ps[i1].m*e1y + ps[i2].m*e2y)**2)/(ps[i1].m+ps[i2].m)
                    val[i,Ns*q+5] = np.nan
                j, k, val[i,Ns*q+6] = spock_find_strongest_MMR(sim, i1, i2)
            except:
                val[0,0] = np.nan
                return val

        val[i,13] = spock_AMD(sim)
        val[i,14] = sim.calculate_megno() # megno
    
    return val
    

def spock_3p_tseriesmanual(sim, args):
    Norbits = args[0]
    Nout = args[1]
    i1 = 1
    i2 = 2
    i3 = 3

    # AMD calculation is easiest in canonical heliocentric coordiantes, so velocities need to be in barycentric frame
    # Don't want to move_to_com() unless we have to so that we get same chaotic trajectory as user passes
    com = sim.calculate_com()
    if com.x**2 + com.y**2 + com.z**2 + com.vx**2 + com.vy**2 + com.vz**2 > 1.e-16:
        sim.move_to_com()
    
    ###############################
    try:
        sim.collision = 'line' # use line if using newer version of REBOUND
    except:
        sim.collision = 'direct'# fall back for older versions
    sim.collision_resolve = collision
    sim.ri_whfast.keep_unsynchronized = 1
    sim.ri_whfast.safe_mode = 0
    ##############################
    ps = sim.particles
    sim.init_megno()
    
    P0 = ps[1].P
    times = np.linspace(0, Norbits*P0, Nout)
    
    if sim.integrator != "whfast":
        sim.integrator = "whfast"
        sim.dt = 2*np.sqrt(3)/100.*P0
   
    pairs = spock_3p_pairs(sim, [i1, i2, i3])
    fg = {}
    for [label, i1, i2] in pairs:
        j, k, _ = spock_find_strongest_MMR(sim, i1, i2) 
        if np.isnan(j):
            fgtilde[label] = (-1, 1) # same as below with f=g=1
        else:
            f, g = get_fg_coeffs(j,k) # gives exact values for first order res
            norm = np.sqrt(2)/np.sqrt(f**2 + g**2) # calculating EM \equiv sqrt(2)*Z
            fgtilde[label] = (norm*f, norm*g)

    val = np.zeros((Nout, 8))
    for i, time in enumerate(times):
        try:
            sim.integrate(time, exact_finish_time=0)
        except:
            val[0,0] = np.nan
            return val

        val[i,0] = sim.t/P0  # time

        Ns = 2
        for j, [label, i1, i2] in enumerate(pairs):
            e1x, e1y = ps[i1].e*np.cos(ps[i1].pomega), -ps[i1].e*np.sin(ps[i1].pomega)
            e2x, e2y = ps[i2].e*np.cos(ps[i2].pomega), -ps[i2].e*np.sin(ps[i2].pomega)
            val[i,Ns*j+1] = np.sqrt((e2x-e1x)**2 + (e2y-e1y)**2)
            val[i,Ns*j+2] = np.sqrt((ps[i1].m*e1x + ps[i2].m*e2x)**2 + (ps[i1].m*e1y + ps[i2].m*e2y)**2)/(ps[i1].m+ps[i2].m)
            ft, gt = fgtilde[label]
            val[i,Ns*j+7] = np.sqrt((ft*e1x + gt*e2x)**2+(ft*e1y + gt*e2y)**2) 

        val[i,5] = spock_AMD(sim)
        val[i,6] = sim.calculate_megno() # megno

    return val
    

def spock_featuresv2(sim, args): # final cut down list
    Norbits = args[0]
    Nout = args[1]
    i1 = 1
    i2 = 2
    i3 = 3
    ps  = sim.particles

    spock_error_check(sim, Norbits, Nout,  i1, i2, i3)
    features = OrderedDict()
    pairs = spock_3p_pairs(sim, [i1, i2, i3])
    for i, [label, i1, i2] in enumerate(pairs):
        features['EMfracstd'+label] = np.nan
        features['EPstd'+label] = np.nan
        features['EMfreestdmed'+label] = np.nan
        features['EMfreestd0'+label] = np.nan
        features['EMfracstdE'+label] = np.nan  # E = exact (celmech)
        features['EPstdE'+label] = np.nan
        features['EMfreestdEmed'+label] = np.nan
        features['EMfreestdE0'+label] = np.nan
        features['AMDcrit'+label] = np.nan
        features['AMDfrac'+label] = np.nan
        features['AMDstd'+label] = np.nan
        features['EMcross'+label] = np.nan
        features['MMRhalfwidthmed'+label] = np.nan
        features['MMRhalfwidth0'+label] = np.nan
        features['MMRstrengthmed'+label] = np.nan
        features['MMRstrength0'+label] = np.nan
        features['j'+label] = np.nan
        features['k'+label] = np.nan

    features['MEGNOmed'] = np.nan
    features['MEGNO'] = np.nan
    features['MEGNOstd'] = np.nan
    features['unstableinshortintegration'] = 0.

    for i, [label, i1, i2] in enumerate(pairs):
        features["AMDcrit"+label] = spock_AMD_crit(sim, i1, i2)
        features["EMcross"+label] = (ps[i2].a-ps[i1].a)/ps[i1].a       
        features["j"+label], features["k"+label], _ = spock_find_strongest_MMR(sim, i1, i2)

    tseries = spock_3p_tseriesv2(sim, args)
    if np.isnan(tseries[0,0]) == True:
        features['unstableinshortintegration'] = 1.
        return pd.Series(features, index=list(features.keys())) # particles collided in short integration, return all nan

    EMnear = tseries[:, 1]
    EPnear = tseries[:, 2]
    EMnearE = tseries[:, 3]
    EPnearE = tseries[:, 4]
    MMRhalfwidthnear = tseries[:,5]
    MMRstrengthnear = tseries[:,6]
    EMfar = tseries[:, 7]
    EPfar = tseries[:, 8]
    EMfarE = tseries[:, 9]
    EPfarE = tseries[:, 10]
    MMRhalfwidthfar = tseries[:,11]
    MMRstrengthfar = tseries[:,12]
    AMD = tseries[:, 13]
    MEGNO = tseries[:, 14]

    features['MEGNOmed'] = np.median(MEGNO)
    features['MEGNO'] = MEGNO[-1]
    features['MEGNOstd'] = MEGNO.std()
    features['AMDfracnear'] = np.median(AMD) / features['AMDcritnear']
    features['AMDfracfar'] = np.median(AMD) / features['AMDcritfar']
    features['AMDstdnear'] = AMD.std() / features['AMDcritnear']
    features['AMDstdfar'] = AMD.std() / features['AMDcritfar']
    features['MMRstrengthmednear'] = np.median(MMRstrengthnear)
    features['MMRstrength0near'] = MMRstrengthnear[0]
    features['MMRhalfwidthmednear'] = np.median(MMRhalfwidthnear)
    features['MMRhalfwidth0near'] = MMRhalfwidthnear[0]
    features['MMRstrengthmedfar'] = np.median(MMRstrengthfar)
    features['MMRstrength0far'] = MMRstrengthfar[0]
    features['MMRhalfwidthmedfar'] = np.median(MMRhalfwidthfar)
    features['MMRhalfwidth0far'] = MMRhalfwidthfar[0]
    
    features['EMfracstdnear'] = EMnear.std() / features['EMcrossnear']
    features['EMfracstdfar'] = EMfar.std() / features['EMcrossfar']
    features['EMfreestdmednear'] = EMnear.std() / features['MMRhalfwidthmednear']
    features['EMfreestdmedfar'] = EMfar.std() / features['MMRhalfwidthmedfar']
    features['EMfreestd0near'] = EMnear.std() / features['MMRhalfwidth0near']
    features['EMfreestd0far'] = EMfar.std() / features['MMRhalfwidth0far']
    features['EPstdnear'] = EPnear.std() 
    features['EPstdfar'] = EPfar.std() 

    features['EMfracstdEnear'] = EMnearE.std() / features['EMcrossnear']
    features['EMfracstdEfar'] = EMfarE.std() / features['EMcrossfar']
    features['EMfreestdEmednear'] = EMnearE.std() / features['MMRhalfwidthmednear']
    features['EMfreestdEmedfar'] = EMnearE.std() / features['MMRhalfwidthmedfar']
    features['EMfreestdE0near'] = EMnearE.std() / features['MMRhalfwidth0near']
    features['EMfreestdE0far'] = EMnearE.std() / features['MMRhalfwidth0far']
    features['EPstdEnear'] = EPnearE.std() 
    features['EPstdEfar'] = EPfarE.std() 
    
    return pd.Series(features, index=list(features.keys())) 

def spock_features(sim, args): # final cut down list
    Norbits = args[0]
    Nout = args[1]
    i1 = 1
    i2 = 2
    i3 = 3
    ps  = sim.particles

    spock_error_check(sim, Norbits, Nout,  i1, i2, i3)
    features = OrderedDict()
    pairs = spock_3p_pairs(sim, [i1, i2, i3])
    for i, [label, i1, i2] in enumerate(pairs):
        features['EMfracstd'+label] = np.nan
        features['EPstd'+label] = np.nan
        features['EMfreestd'+label] = np.nan
        features['AMDcrit'+label] = np.nan
        features['AMDfrac'+label] = np.nan
        features['AMDstd'+label] = np.nan
        features['EMcross'+label] = np.nan
        features['MMRhalfwidth'+label] = np.nan
        features['MMRstrength'+label] = np.nan
    features['MEGNO'] = np.nan
    features['megno'] = np.nan
    features['MEGNOstd'] = np.nan
    features['unstableinshortintegration'] = 0.

    for i, [label, i1, i2] in enumerate(pairs):
        features['EMcross'+label] = (ps[i2].a-ps[i1].a)/ps[i1].a
        features["AMDcrit"+label] = spock_AMD_crit(sim, i1, i2)
        
        j, k, features['MMRstrength'+label] = spock_find_strongest_MMR(sim, i1, i2) 
        if not np.isnan(j): # a resonance  was  found. If no strong res nearby, MMRhalfwidth will be nan
            pvars = Poincare.from_Simulation(sim)
            avars = Andoyer.from_Poincare(pvars, j=j, k=k, a10=ps[i1].a, i1=i1, i2=i2)
            features['MMRhalfwidth'+label] = (avars.Zsep_outer-avars.Zstar)*np.sqrt(2) # Want EM half width. Z approx EM/sqrt(2)
  
    tseries = spock_3p_tseries(sim, args)
    if np.isnan(tseries[0,0]) == True:
        features['unstableinshortintegration'] = 1.
        return pd.Series(features, index=list(features.keys())) # particles collided in short integration, return all nan

    EMnear = tseries[:, 1]
    EPnear = tseries[:, 2]
    EMfar = tseries[:, 3]
    EPfar = tseries[:, 4]
    AMD = tseries[:, 5]
    MEGNO = tseries[:, 6]

    features['MEGNOmed'] = np.median(MEGNO)
    features['MEGNOstd'] = MEGNO.std()
    features['AMDfracnear'] = np.median(AMD) / features['AMDcritnear']
    features['AMDfracfar'] = np.median(AMD) / features['AMDcritfar']
    features['AMDstdnear'] = AMD.std() / features['AMDcritnear']
    features['AMDstdfar'] = AMD.std() / features['AMDcritfar']
    features['EMfracstdnear'] = EMnear.std() / features['EMcrossnear']
    features['EMfracstdfar'] = EMfar.std() / features['EMcrossfar']
    features['EMfreestdnear'] = EMnear.std() / features['MMRhalfwidthnear']
    features['EMfreestdfar'] = EMnear.std() / features['MMRhalfwidthfar']
    features['EPstdnear'] = EPnear.std() 
    features['EPstdfar'] = EPfar.std() 

    return pd.Series(features, index=list(features.keys())) 


def spock_regressor_tseries(sim, args): # final cut down list
    Norbits = args[0]
    Nout = args[1]
    i1 = 1
    i2 = 2
    i3 = 3
    ps  = sim.particles

    spock_error_check(sim, Norbits, Nout,  i1, i2, i3)
    features = OrderedDict()
    pairs = spock_3p_pairs(sim, [i1, i2, i3])

    for i, [label, i1, i2] in enumerate(pairs):
        features['EMcross'+label] = (ps[i2].a-ps[i1].a)/ps[i1].a
        features["AMDcrit"+label] = spock_AMD_crit(sim, i1, i2)

    tseries = spock_3p_tseries(sim, args)
    if np.isnan(tseries[0,0]) is True:
        features['unstableinshortintegration'] = 1
        return tseries

    tseries[:, 1] /= features['EMcrossnear'] # EMnear
    tseries[:, 3] /= features['EMcrossfar'] # EMfar
    tseries[:, 5] /= features['AMDcritnear'] # AMD
    MEGNO = tseries[:, 6]

    return tseries

def spock_3p_tseriesv3(sim, args):
    Norbits = args[0]
    Nout = args[1]
    i1 = args[2] 
    i2 = args[3] 
    i3 = args[4] 

    # AMD calculation is easiest in canonical heliocentric coordiantes, so velocities need to be in barycentric frame
    # Don't want to move_to_com() unless we have to so that we get same chaotic trajectory as user passes
    com = sim.calculate_com()
    if com.x**2 + com.y**2 + com.z**2 + com.vx**2 + com.vy**2 + com.vz**2 > 1.e-16:
        sim.move_to_com()
    
    ###############################
    try:
        sim.collision = 'line' # use line if using newer version of REBOUND
    except:
        sim.collision = 'direct'# fall back for older versions
    sim.collision_resolve = collision
    sim.ri_whfast.keep_unsynchronized = 1
    sim.ri_whfast.safe_mode = 0
    ##############################
    ps = sim.particles
    sim.init_megno()
    
    P0 = ps[1].P
    times = np.linspace(0, Norbits*P0, Nout)
    
    if sim.integrator != "whfast":
        sim.integrator = "whfast"
        sim.dt = 2*np.sqrt(3)/100.*P0
   
    pairs = spock_3p_pairs(sim, [i1, i2, i3])
    jk = {}
    a10 = {}
    for [label, i1, i2] in pairs:
        j, k, _ = spock_find_strongest_MMR(sim, i1, i2) 
        if np.isnan(j) == False:
            jk[label] = (j,k)
            a10[label] = ps[i1].a

    val = np.zeros((Nout, 15))
    for i, time in enumerate(times):
        try:
            sim.integrate(time, exact_finish_time=0)
        except:
            val[0,0] = np.nan
            return val

        val[i,0] = sim.t/P0  # time

        Ns = 4
        for q, [label, i1, i2] in enumerate(pairs):
            e1x, e1y = ps[i1].e*np.cos(ps[i1].pomega), -ps[i1].e*np.sin(ps[i1].pomega)
            e2x, e2y = ps[i2].e*np.cos(ps[i2].pomega), -ps[i2].e*np.sin(ps[i2].pomega)
            try: # it's unlikely but possible for bodies to land nearly on top of  each other midtimestep and get a big kick that doesn't get caught by collisions  post timestep. All these cases are unstable, so flag them as above
                try:
                    j,k = jk[label]
                    # average only affects a (Lambda) Z and I think  Zcom  don't depend on a. Zsep and Zstar slightly, but several sig figs in even when close at conjunction
                    avars = Andoyer.from_Simulation(sim, a10=a10[label], j=j, k=k, i1=i1, i2=i2, average=False)
                    val[i,Ns*q+1] = avars.Z*np.sqrt(2) # EM = Z*sqrt(2)
                    val[i,Ns*q+2] = avars.Zcom # no sqrt(2) factor
                    val[i,Ns*q+3] = (avars.Zsep_outer-avars.Zstar)*np.sqrt(2)
                except: # no nearby resonance, use EM and ecom
                    val[i,Ns*q+1] = np.sqrt((e2x-e1x)**2 + (e2y-e1y)**2)
                    val[i,Ns*q+2] = np.sqrt((ps[i1].m*e1x + ps[i2].m*e2x)**2 + (ps[i1].m*e1y + ps[i2].m*e2y)**2)/(ps[i1].m+ps[i2].m)
                    val[i,Ns*q+3] = np.nan
                j, k, val[i,Ns*q+4] = spock_find_strongest_MMR(sim, i1, i2)
            except:
                val[0,0] = np.nan
                return val

        val[i,9] = spock_AMD(sim)
        val[i,10] = sim.calculate_megno() # megno
    
    return val
    
def spock_featuresv3(sim, args): # final cut down list
    Norbits = args[0]
    Nout = args[1]
    i1 = args[2] 
    i2 = args[3] 
    i3 = args[4] 
    ps  = sim.particles

    spock_error_check(sim, Norbits, Nout,  i1, i2, i3)
    features = OrderedDict()
    pairs = spock_3p_pairs(sim, [i1, i2, i3])
    for i, [label, i1, i2] in enumerate(pairs):
        features['EMfracstd'+label] = np.nan
        features['EMfracstdE'+label] = np.nan  # E = exact (celmech)
        features['EPstdE'+label] = np.nan
        features['EMfreestdEmed'+label] = np.nan
        features['AMDcrit'+label] = np.nan
        features['AMDfrac'+label] = np.nan
        features['AMDstd'+label] = np.nan
        features['EMcross'+label] = np.nan
        features['MMRhalfwidthmed'+label] = np.nan
        features['MMRstrengthmed'+label] = np.nan
        features['j'+label] = np.nan
        features['k'+label] = np.nan

    features['MEGNO'] = np.nan
    features['MEGNOstd'] = np.nan
    features['unstableinshortintegration'] = 0.

    for i, [label, i1, i2] in enumerate(pairs):
        features["AMDcrit"+label] = spock_AMD_crit(sim, i1, i2)
        features["EMcross"+label] = (ps[i2].a-ps[i1].a)/ps[i1].a       
        features["j"+label], features["k"+label], _ = spock_find_strongest_MMR(sim, i1, i2)

    tseries = spock_3p_tseriesv3(sim, args)
    if np.isnan(tseries[0,0]) == True:
        features['unstableinshortintegration'] = 1.
        return pd.Series(features, index=list(features.keys())) # particles collided in short integration, return all nan

    EMnearE = tseries[:, 1]
    EPnearE = tseries[:, 2]
    MMRhalfwidthnear = tseries[:,3]
    MMRstrengthnear = tseries[:,4]
    EMfarE = tseries[:, 5]
    EPfarE = tseries[:, 6]
    MMRhalfwidthfar = tseries[:,7]
    MMRstrengthfar = tseries[:,8]
    AMD = tseries[:, 9]
    MEGNO = tseries[:, 10]

    features['MEGNO'] = MEGNO[-1]
    features['MEGNOstd'] = MEGNO.std()
    features['AMDfracnear'] = np.median(AMD) / features['AMDcritnear']
    features['AMDfracfar'] = np.median(AMD) / features['AMDcritfar']
    features['AMDstdnear'] = AMD.std() / features['AMDcritnear']
    features['AMDstdfar'] = AMD.std() / features['AMDcritfar']
    features['MMRstrengthmednear'] = np.median(MMRstrengthnear)
    features['MMRhalfwidthmednear'] = np.median(MMRhalfwidthnear)
    
    features['EMfracstdEnear'] = EMnearE.std() / features['EMcrossnear']
    features['EMfracstdEfar'] = EMfarE.std() / features['EMcrossfar']
    features['EMfreestdEmednear'] = EMnearE.std() / features['MMRhalfwidthmednear']
    features['EMfreestdEmedfar'] = EMnearE.std() / features['MMRhalfwidthmedfar']
    features['EPstdEnear'] = EPnearE.std() 
    features['EPstdEfar'] = EPfarE.std() 
    
    return pd.Series(features, index=list(features.keys())) 
