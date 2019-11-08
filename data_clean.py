import pandas as pd
import numpy as np

STATES = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
  "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
  "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
  "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
  "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
  "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
  "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
  "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]



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

    houseVoteshare = pd.DataFrame(columns=["year", "state", "dem_voteshare", "rep_voteshare"])
    index = 0
    for year in range(1976, 2018, 2):
        for state in STATES:
            share_dem, share_rep = voteShare(df, year, state)
            houseVoteshare.loc[index] = [year, state, share_dem, share_rep]
            index += 1

    return houseVoteshare

def voteShare(df, year, state):
    candidate_total_dem = df["candidatevotes"].where((df["party"] == "democrat") & (df["year"] == year) & (df["state"] == state)).sum()
    total_dem = df["totalvotes"].where((df.year == year) & (df.state == state) & (df.party == "democrat")).sum()
    candidate_total_rep = df["candidatevotes"].where((df["party"] == "republican") & (df["year"] == year) & (df["state"] == state)).sum()
    total_rep = df["totalvotes"].where((df.year == year) & (df.state == state) & (df.party == "republican")).sum()

    # print("Dem voteshare %s in %s in %s" % (candidate_total_dem / total_dem, state, year))
    # print("Rep voteshare %s in %s in %s" % (candidate_total_rep / total_rep, state, year))
    
    return (candidate_total_dem/total_dem), (candidate_total_rep/total_rep)


pres_df = PresClean()
senate_df = SenateClean()
house_df = HouseClean()

