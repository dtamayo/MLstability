from subprocess import call
from collections import OrderedDict
import sys

datapath = '/mnt/ssd/Dropbox/Dropbox (Princeton)/workspace/stability/MLstability/training_data/'

datasets = 'all' # either a list of folders ([resonant, TTVsystems/Kepler-431]) or 'all' or 'ttv' to expand
runfunc = 'ressummaryfeaturesxgb2'#'orbtseries'#'orbsummaryfeaturesxgb'

kwargs = OrderedDict()
kwargs['Norbits'] = 1e4
kwargs['Nout'] = 1000
#kwargs['window'] = 10

foldername = runfunc
for key, val in kwargs.items():
    foldername += '{0}{1}'.format(key, val)

def allsystems():
    return ['random', 'resonant'] + ttvsystems() + nonressystems()

def ttvsystems():
    folders = ['KOI-0115', 'KOI-0168', 'KOI-0085', 'KOI-0156', 'KOI-1576', 'KOI-2086', 'KOI-0314'] 
    return ['TTVsystems/' + folder for folder in folders]

def nonressystems():
    folders = ['Kepler-431', 'EPIC-210897587-2', 'Kepler-446', 'LP-358-499'] 
    return ['nonressystems/' + folder for folder in folders]

if datasets == 'all':
    datasets = allsystems()

if datasets == 'ttv':
    datasets = ttvsystems()

if datasets == 'nonres':
    datasets = nonressystems()

for dataset in list(datasets):
    folder = datapath + dataset + '/'
    #call('rm -f ' + folder + 'labels.csv', shell=True)
    #call('rm -f ' + folder + 'massratios.csv', shell=True)
    #call('rm -f ' + folder + 'runstrings.csv', shell=True)
    call('rm -rf "' + folder + foldername + '"', shell=True)
    call('rm -rf "' + foldername + '"', shell=True)
