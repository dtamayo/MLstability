import rebound
import numpy as np
import pandas as pd
import os
from subprocess import call
import warnings
warnings.filterwarnings('ignore') # filter REBOUND warnings about version that I've already tested

datapath = '/mnt/ssd/workspace/stability/stabilitydataset/data/'
repopath = '/mnt/ssd/workspace/stability/MLstability/'

if rebound.__githash__ != '25f856dc2f79e0ad17b2f6bd604225f550593376': # can run all with this commit
    print('Should checkout commit above to ensure this runs correctly')

call('cp ' + repopath + 'generate_training_data/inputresonantparams.csv ' + repopath + 'training_data/resonant/', shell=True)

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


datasets = ['resonant', 'random'] + ttvsystems() + nonressystems()

for dataset in datasets:
    print(dataset)
    pathtosa = datapath + dataset + '/simulation_archives/runs/'
    pathtossa = datapath + dataset + '/simulation_archives/shadowruns/'
    pathtotraining = repopath + 'training_data/' + dataset + '/'

    root, dirs, files = next(os.walk(pathtosa))
    runstrings = [file[2:] for file in files if file[-3:] == 'bin']
    df = pd.DataFrame(runstrings, columns=['runstring'])
    df = df.sort_values(by='runstring')
    df = df.reset_index(drop=True)
    df.to_csv(pathtotraining+'runstrings.csv', encoding='ascii')

    df['instability_time'] = -1
    df['shadow_instability_time'] = -1
    df['Stable'] = -1

    df = df.apply(labels, axis=1)
    df.to_csv(pathtotraining+'labels.csv', encoding='ascii')

    df = pd.read_csv(pathtotraining+'runstrings.csv', index_col=0)
    df['m1'] = -1
    df['m2'] = -1
    df['m3'] = -1

    df = df.apply(massratios, axis=1)
    df.to_csv(pathtotraining+'massratios.csv', encoding='ascii')
