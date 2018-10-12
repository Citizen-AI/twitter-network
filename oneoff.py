import pandas as pd
from library import pd_to_csv


df1 = pd.read_csv('output/mps.csv')
df2 = pd.read_csv('output/mps-people-plus-mps.csv')

# for i in df2.index:
#     screen_name = df2.loc[i, 'label']
#     print([screen_name.isin([screen_name]))

df2.loc[df2.label.isin(df1['label']), 'type'] = 'mp'
pd_to_csv(df=df2, filename='mps-people-plus-mps-type.csv')
# print ()
# x = df2.loc[df2.label.isin(df1['label'])]
# print(df2[x])
