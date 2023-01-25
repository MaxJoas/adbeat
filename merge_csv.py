import pandas as pd
import sys
import glob


def merge_csv(files, outfile):
    """takes a list of csv files, and merges them in specific manner
    ARGS:
        files - list
        outfile - str: name of output file
     RETURNS:
         None

     """
    for f in files:
        print(f)
        cur_df = pd.read_csv(f)
        cur_df.head()
        cur_df
        advertiser_helper = f.split("Advertiser_Profile_Report_-_")
        advertiser_helper2 = advertiser_helper[1].split("Desktop_and_Mobile_")
        adverister = advertiser_helper2[0][:-1]

        advertiser_helper
        helper = f.split("Desktop_and_Mobile_")
        date_helper = helper[1].split("_to_")
        date_helper2 = date_helper[1].split("_")
        device_helper = "-".join(date_helper2[2::])
        startdate = date_helper[0]
        enddate = date_helper2[0]
        device = device_helper.replace(".csv", "")
        cur_df = cur_df.drop(
            ['Share.1', 'Ads By Size', 'Top Creative Phrases'], axis=1, errors='ignore')
        cur_df['advertiser'] = adverister
        cur_df['startdate'] = startdate
        cur_df['enddate'] = enddate
        cur_df['Sub-Kanal2'] = device
        cur_df.to_csv(outfile, mode='a')


# if __name__ == '__main__':
#     data_dir = sys.argv[1]
#     outfile = sys.argv[2]
#     files = glob.glob(data_dir)
#     merge_csv(files, outfile)
### for direct exectution not for start in terminal ###

data_dir = "../Daily_Ad_Spend/*.csv"
outfile = "dailyadspend.csv"
files = glob.glob(data_dir)
merge_csv(files, outfile)

data_dir = "../Top_Networks/*.csv"
outfile = "topnetworks3.csv"
files = glob.glob(data_dir)
files
merge_csv(files, outfile)


data_dir = "../Top_Pub_Categories/*.csv"
outfile = "toppupcat4.csv"
files = glob.glob(data_dir)
merge_csv(files, outfile)


data_dir = "../Desktop_Standard_Ads/*.csv"
outfile = "adverister.csv"
files = glob.glob(data_dir)
merge_csv(files, outfile)


data_dir = "../Creative_Analysis/*.csv"
outfile = "creeativeana3.csv"
files = glob.glob(data_dir)
merge_csv(files, outfile)

### ------------------------------------------------------------------ ###
### SEPERATING SIMILAR AND RECOMMEND IN THREE CSV ###
### ------------------------------------------------------------------ ###
data_dir = "../Similar%20%26%20Recommended/*.csv"
outfile = "similar_recommend.csv"
files = glob.glob(data_dir)
merge_csv(files, outfile)
df = pd.read_csv("./similar_recommend.csv")
df.head()
df_similar = df.iloc[:, 1:4]
df_similar['adveristers'] = df['adverister']
df_similar['startdate'] = df['startdate']
df_similar['enddate'] = df['enddate']
df_similar.to_csv('similaradvertiser.csv')

df_publishers = df.iloc[:, 4:7]
df_publishers['adveristers'] = df['adverister']
df_publishers['startdate'] = df['startdate']
df_publishers['enddate'] = df['enddate']
df_publishers.to_csv('recommendedpublisher.csv')

df_channels = df.iloc[:, 7:10]
df_channels['adveristers'] = df['adverister']
df_channels['startdate'] = df['startdate']
df_channels['enddate'] = df['enddate']
df_channels.to_csv('recommendedchannels.csv')


# ### ---------------------------------------------------------------- ###
# ### cleaning creative analysis tab ####
df_creative = pd.read_csv("./creeativeana3.csv")
df_creative.columns
df_creative2 = df_creative.iloc[:, 1:4]
df_creative2
df_creative2[["startdate", "enddate"]] = df_creative[["startdate", "enddate"]]
df_creative2.dropna(inplace=True)
df_creative2.to_csv("creative_ana2.csv")
df_creative.head()
df_createive.head()
