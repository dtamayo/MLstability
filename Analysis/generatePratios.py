import rebound
import pandas as pd

datapath = '../../stabilitydataset/'

randompath = 'data/random/simulation_archives/runs/'
respath = 'data/resonant/simulation_archives/runs/'

dfrand = pd.read_csv('../training_data/random/labels.csv', index_col=0)
dfres = pd.read_csv('../training_data/resonant/labels.csv', index_col=0)

def randPratios(row):
    sa = rebound.SimulationArchive(datapath+randompath+'sa{0}'.format(row['runstring']))
    sim = sa[0]
    ps = sim.particles
    row['Pratio21'] = ps[2].P/ps[1].P
    row['Pratio32'] = ps[3].P/ps[2].P
    return row

def resPratios(row):
    sa = rebound.SimulationArchive(datapath+respath+'sa{0}'.format(row['runstring']))
    sim = sa[0]
    ps = sim.particles
    row['Pratio21'] = ps[2].P/ps[1].P
    row['Pratio32'] = ps[3].P/ps[2].P
    return row

dfrand = dfrand.apply(randPratios, axis=1)
dfres = dfres.apply(resPratios, axis=1)

dfres.to_csv('../csvs/resPratios.csv')
dfrand.to_csv('../csvs/randomPratios.csv')
