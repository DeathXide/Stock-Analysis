import pandas as pd

df1 = pd.read_csv('Stocksorting.csv')


df1["RankR"] = df1["ROCE"].rank(method ='min',ascending=False)
df1["RankE"] = df1["Earningsyield"].rank(method ='min',ascending=False)


df1['Rank'] = df1['RankR']+df1['RankE']

df1.sort_values('Rank',inplace=True, ignore_index=True )

df1.to_csv('MAGIC.csv',columns=["Issuer Name" , "Security Id" ,"Security Name","Rank"])



# df3 = pd.read_csv('Stocksorting.csv', usecols={"Issuer Name" , "Security Id" ,"Security Name" })
# df3["Rank"] = df1['Rank'] + df2['Rank']
# print(df3)
# df3.sort_values("Rank", axis = 0, ascending = True, inplace = True,)
# print(df3)
