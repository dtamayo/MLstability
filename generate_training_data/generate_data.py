import rebound
import numpy as np
from subprocess import call
import sys
import warnings
warnings.filterwarnings('ignore') # to suppress warnings about REBOUND versions that I've already tested
from collections import OrderedDict

datapath = '/mnt/ssd/Dropbox/Dropbox (Princeton)/workspace/stability/stabilitydataset/data/'
repopath = '/mnt/ssd/Dropbox/Dropbox (Princeton)/workspace/stability/MLstability/'
sys.path.append(repopath + 'generate_training_data/')
from training_data_functions import gen_training_data, orbtseries, orbsummaryfeaturesxgb, ressummaryfeaturesxgb, normressummaryfeaturesxgb, ressummaryfeaturesxgb2, ressummaryfeaturesxgbv4, restseriesv5, resparamsv5, ressummaryfeaturesxgbv5

datasets = ['resonant'] # either a list of folders ([resonant, TTVsystems/Kepler-431]) or 'all' or 'ttv' to expand
runfunc = ressummaryfeaturesxgbv5# Look at top of func to use in training_data_functions.py to figure out what kwargs we have to set

kwargs = OrderedDict()
kwargs['Norbits'] = 1e4
kwargs['Nout'] = 1000
#kwargs['window'] = 10

foldername = runfunc.__name__
for key, val in kwargs.items():
    foldername += '{0}{1}'.format(key, val)

gendatafolder = repopath + 'generate_training_data/'

already_exists = call('mkdir "' + gendatafolder + foldername + '"', shell=True)
if not already_exists: # store a copy of this script in generate_data so we can always regenerate what we had
    call('cp "' + gendatafolder + '/generate_data.py" "' + gendatafolder + foldername + '"', shell=True)
    call('python "' + gendatafolder + foldername + '/generate_data.py"' , shell=True)
    exit()
    # we always run the copied script so that we do the same thing whether we're running for first time or regenerating
# if it does exist don't overwrite since we don't want to overwrite history

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
    if dataset == 'random':
        if rebound.__githash__ != '48feb327f90611a5569682578980b5604aa6102a':
            print('random dataset not run. Check out rebound commit 48feb327f90611a5569682578980b5604aa6102a and rerun script if needed')
            continue 
    else:
        if rebound.__githash__ != '6fb912f615ca542b670ab591375191d1ed914672':
            print('{0} dataset not run. Check out rebound commit 6fb912f615ca542b670ab591375191d1ed914672 and rerun script if needed'.format(dataset))
            continue 

    safolder = datapath + dataset + '/simulation_archives/runs/'
    trainingdatafolder = repopath + 'training_data/' + dataset + '/'

    already_exists = call('mkdir "' + trainingdatafolder + foldername + '"', shell=True)
    if already_exists:
        print('output folder already exists at {0}. Remove it if you want to regenerate'.format(trainingdatafolder+foldername))
        continue
    call('cp "' + trainingdatafolder + 'labels.csv" "' + trainingdatafolder + foldername + '"', shell=True)
    call('cp "' + trainingdatafolder + 'massratios.csv" "' + trainingdatafolder + foldername + '"', shell=True)
    call('cp "' + trainingdatafolder + 'runstrings.csv" "' + trainingdatafolder + foldername + '"', shell=True)

    print(trainingdatafolder + foldername)
    gen_training_data(trainingdatafolder + foldername, safolder, runfunc, list(kwargs.values()))
