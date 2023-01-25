import pandas as pd


def f(x):
    d = {}
    d['Impression_Sum'] = x['Impressions'].sum()
    d['AdSpend_Sum'] = x['Ad Spend'].sum()
    d['unique_media_link'] = x['Media Link'].nunique()
    d['medialink_count'] = x['Media Link'].count()
    return pd.Series(d, index=["Impression_Sum", "AdSpend_Sum", "unique_media_link", "medialink_count"])


# Reading in and check -------------------------------------------------------
df = pd.read_csv('./adverister.csv')
df["Sub-Kanal2"]
df["enddate"]
df.shape
df.columns
unique_media_link = df["Media Link"].nunique()

df_uniqe_media = df.groupby('aggregation_helper')['Media Link'].nunique()
unique_media_link_after = df_uniqe_media.sum()
unique_media_link - unique_media_link_after
df["Ad Type"]
df["Media Type"]

# Data Cleaning --------------------------------------------------------------
df["aggregation_helper"] = df["Ad Type"] + "." + df["Network"]
df = df[df["Impressions"] != "Impressions"]
df["Impressions"] = df["Impressions"].str.replace(',', '')
df["Ad Spend"] = df["Ad Spend"].str.replace(',', '')

df["Impressions"] = pd.to_numeric(df["Impressions"])
df["Ad Spend"] = pd.to_numeric(df["Ad Spend"])

# Data Aggregation -----------------------------------------------------------
df_aggr = df.groupby(["aggregation_helper", "Advertiser", "Sub-Kanal2"])[
    ["Impressions", "Ad Spend"]].apply(lambda x: x.sum())
df_aggr = df.groupby(["aggregation_helper", "Advertiser",
                     "Sub-Kanal2", "startdate"]).apply(f)

df_aggr
df_aggr["Media Type", "Network"] = df_aggr.index.str.split(".", 1, expand=True)

df_count_media = df.groupby('aggregation_helper')['Media Link'].count()
df_uniqe_media = df.groupby('aggregation_helper')['Media Link'].nunique()
df_count_media
df_uniqe_media
df_uniqe_media.sum()
df_count_media.sum()
df["Media Link"].count()
df["Media Link"].nunique()

# QUALITY CONTROL ---------------------------------------------------------
df_aggr.shape
df_aggr["Ad Spend"].sum()
df["Ad Spend"].sum()

df["Impressions"].sum()
df_aggr["Impressions"].sum()
df_aggr


#### Save and clean
df_aggr["unique_medialink_count"] = df_uniqe_media
df_aggr["medialink_count"] = df_count_media

df_aggr.to_csv("advertiser_aggregated.csv")
