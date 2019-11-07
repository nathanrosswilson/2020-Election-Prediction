import pandas as pd
import numpy as np


def PresClean():
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

    # add a column that is "incumbent: true, false"

    # df.to_csv("data/pres_clean.csv", index=False)

    return df


def SenateClean():
    df = pd.read_csv("data/1976-2018-senate.csv")
    df = df.drop(
        [
            "state_po",
            "state_fips",
            "state_cen",
            "state_ic",
            "office",
            "district",
            "stage",
            "special",
            "writein",
            "mode",
            "unofficial",
            "version",
        ],
        axis=1,
    )

    df = df.drop(df[(df.party != "democrat") & (df.party != "republican")].index)

    df["voteshare"] = df["candidatevotes"] / df["totalvotes"]
    df = df.reset_index(drop=True)

    return df


def HouseClean():
    df = pd.read_csv("data/1976-2018-house.csv")
    df = df.drop(
        [
            "state_po",
            "state_fips",
            "state_cen",
            "state_ic",
            "office",
            "district",
            "stage",
            "runoff",
            "special",
            "writein",
            "mode",
            "unofficial",
            "version",
        ],
        axis=1,
    )
    df = df.drop(df[(df.party != "democrat") & (df.party != "republican")].index)

    total_AL_dem_1976 = df["candidatevotes"].where(df["candidate"] == "Bill Davenport").sum()
    
    print(total_AL_dem_1976)
    print(df[(df["party"] =="democrat") & (df["year"] == 1976)] )
    return df


pres_df = PresClean()
senate_df = SenateClean()
house_df = HouseClean()

