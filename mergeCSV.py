import pandas as pd
import os

os.chdir("C:\\Users\\1\\Desktop\\CA675\\Assignment 1")
list = ["QueryResults2.csv","QueryResults3.csv","QueryResults4.csv","QueryResults5.csv"]
df = pd.read_csv("QueryResults.csv")
#print(df)

for filename in list:
    df_new = pd.read_csv(filename)
    df = df.append(df_new)

df = df[["Id","Score","ViewCount","Title","Body","OwnerUserId"]]

df["Title"] = df["Title"].str.replace(","," ")
df["Title"] = df["Title"].str.replace("\n"," ")
df["Title"] = df["Title"].str.replace("\r"," ")
df["Body"] = df["Body"].str.replace(","," ")
df["Body"] = df["Body"].str.replace("\n"," ")
df["Body"] = df["Body"].str.replace("\r"," ")
print(df)

df.to_csv("QueryResultsAll.csv",index=False)

