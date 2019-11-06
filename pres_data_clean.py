import pandas as pd
import numpy as np

df = pd.read_csv("data/1976-2016-president.csv")
df = df.drop(
    [
        "state_po",
        "state_fips",
        "state_cen",
        "state_ic",
        "office",
        "writein",
        "version",
        "notes",
    ],
    axis=1,
)
df = df.drop(df[(df.party != "democrat") & (df.party != "republican")].index)

df["voteshare"] = df["candidatevotes"] / df["totalvotes"]

df = df.reset_index(drop=True)

losers = []
for i in range(0, df.shape[0] - 1):
    if df.iloc[i]["state"] == df.iloc[i + 1]["state"]:
        if df.iloc[i]["voteshare"] < df.iloc[i + 1]["voteshare"]:
            losers.append(i)
        else:
            losers.append(i + 1)

df = df.drop(df.index[losers])

df = df.reset_index(drop=True)

print(df)
