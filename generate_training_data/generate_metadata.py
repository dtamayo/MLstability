import rebound
import numpy as np
import pandas as pd
import os
from subprocess import call
from dask import dataframe as dd 
import warnings
from icecream import ic
warnings.filterwarnings('ignore') # filter REBOUND warnings about version that I've already tested

datapath = "/mnt/ceph/users/mcranmer/general_data/orbital_integrations/"
#datapath = "/mnt/home/mcranmer/running_rebound/stabilitydataset/data/"#'/mnt/ssd/Dropbox/Dropbox (Princeton)/workspace/stability/stabilitydataset/data/'
repopath = '/mnt/ceph/users/mcranmer/MLstability/'
#datapath = '/mnt/ssd/workspace/stability/stabilitydataset/data/'
#repopath = '/mnt/ssd/workspace/stability/MLstability/'

if rebound.__githash__ != '06c95e2a69d319de3b077d92f2541cdcdf68a8fa':
    print('Should checkout commit above to ensure this runs correctly')

ic()
call('cp ' + repopath + 'generate_training_data/inputresonantparams.csv ' + repopath + 'training_data/resonant/', shell=True)
ic()

def labels(row):
    try:
        sa = rebound.SimulationArchive(pathtosa+'sa'+row['runstring'])
        sim = sa[0]
        P1 = sim.particles[1].P # Need initial orbital period for TTVsystems, where P1 != 1

        try: # Needed for old integrations (random and Naireen) because no snapshot on end
            sim = rebound.Simulation(pathtosa+'../../final_conditions/runs/fc'+row['runstring'])
        except: # New runs (resonant and Ari) have snapshots at collision
            sa = rebound.SimulationArchive(pathtosa+'sa'+row['runstring'])
            sim = sa[-1]
        row['instability_time'] = sim.t/P1
        try:
            ssim = rebound.Simulation(pathtossa+'../../final_conditions/shadowruns/fc'+row['runstring'])
        except:
            ssa = rebound.SimulationArchive(pathtossa+'sa'+row['runstring'])
            ssim = ssa[-1]
        row['shadow_instability_time'] = ssim.t/P1
        row['Stable'] = row['instability_time'] > 9.99e8
    except:
        print(pathtosa+'sa'+row['runstring'])
    return row

def massratios(row):
    try:
        sa = rebound.SimulationArchive(pathtosa+'sa'+row['runstring'])
        sim = sa[0]
        row['m1'] = sim.particles[1].m/sim.particles[0].m
        row['m2'] = sim.particles[2].m/sim.particles[0].m
        row['m3'] = sim.particles[3].m/sim.particles[0].m
    except:
        print(pathtosa+'sa'+row['runstring'])
    return row

def ttvsystems():
    folders = ['KOI-0115', 'KOI-0168', 'KOI-0085', 'KOI-0156', 'KOI-1576', 'KOI-2086', 'KOI-0314'] 
    return ['TTVsystems/' + folder for folder in folders]

def nonressystems():
    folders = ['Kepler-431', 'EPIC-210897587-2', 'Kepler-446', 'LP-358-499'] 
    return ['nonressystems/' + folder for folder in folders]



step_size = 100*1000
steps = 0
start = steps * step_size
cdataset = 'short_resonant_%.12d_bkup' % (start,)
ic()
datasets = [cdataset] #'all' # either a list of folders ([resonant, TTVsystems/Kepler-431]) or 'all' or 'ttv' to expand
#datasets = ['resonant', 'random'] + ttvsystems() + nonressystems()
ic()
for dataset in datasets:
    print(dataset)
    pathtosa = datapath + dataset + '/simulation_archives/runs/'
    pathtossa = datapath + dataset + '/simulation_archives/shadowruns/'
    pathtotraining = repopath + 'training_data/' + dataset + '/'

    ic()
    root, dirs, files = next(os.walk(pathtosa))
    runstrings = [file[2:] for file in files if file[-3:] == 'bin']
    ic()
    df = pd.DataFrame(runstrings, columns=['runstring'])
    df = df.sort_values(by='runstring')
    df = df.reset_index(drop=True)
    ic()
    df.to_csv(pathtotraining+'runstrings.csv', encoding='ascii')

    df['instability_time'] = -1
    df['shadow_instability_time'] = -1
    df['Stable'] = -1

    ic()
    df = dd.from_pandas(df, npartitions=24)
    df = df.apply(labels, axis=1)
    df = df.compute()
    df.to_csv(pathtotraining+'labels.csv', encoding='ascii')
    df = pd.DataFrame(df['shadow_instability_time'])
    call('mkdir ' + pathtotraining + 'shadowtimes', shell=True)
    call('cp ' + pathtotraining + 'labels.csv ' + pathtotraining + 'shadowtimes/', shell=True)
    df.to_csv(pathtotraining+'shadowtimes/trainingdata.csv', encoding='ascii')

    df = pd.read_csv(pathtotraining+'runstrings.csv', index_col=0)
    df['m1'] = -1
    df['m2'] = -1
    df['m3'] = -1

    ic()
    df = dd.from_pandas(df, npartitions=24)
    df = df.apply(massratios, axis=1)
    df = df.compute()
    df.to_csv(pathtotraining+'massratios.csv', encoding='ascii')

    call('cp ' + pathtotraining + 'massratios.csv ' + pathtotraining + 'shadowtimes/', shell=True)
    call('cp ' + pathtotraining + 'runstrings.csv ' + pathtotraining + 'shadowtimes/', shell=True)
    ic()
