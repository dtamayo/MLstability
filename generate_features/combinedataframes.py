import pandas as pd
simIDmax = 15000
Nnodes = 10
Npernode = simIDmax // Nnodes
starts = [i*Npernode for i in range(Nnodes)]
dfs = []
for start in starts:
    dfs.append(pd.read_csv('../csvs/tmp/short_integration_features'+str(start)+'.csv', index_col=0))
df = pd.concat(dfs)
df.to_csv('../csvs/short_integration_features.csv', encoding='ascii')
