import pandas as pd
import subprocess
import sys
import os


def download_csv(url_df, tab_list):
    """ takes a list of file spreadsheets ids and downloads specidied tabs
        as csv file
    ARGS:
        url_df - pd.DataFrame: df with names and ids of spreadsheets
        tab_list - list: list with string of tabnames in excel sheet
    RETRUNS:
        none

    """
    # relevant tabs we want to download

    for index, row in url_df.iterrows():
        dir_name = tab_list[0]
        dir_name = dir_name.replace(" ", "_").replace("&", "_")
        if not os.path.isdir("../"+dir_name):
            subprocess.call(["mkdir", "../" + dir_name])
        # subprocess.call(["cd", dir_name])

        for tab in tab_list:
            base_url = "https://docs.google.com/spreadsheets/d/"
            file_id = row["File-Id"]
            url_part1 = "/gviz/tq?tqx=out:csv&sheet="  # query structure
            sheet_name = tab
            end_url = "&tq"  # query structure
            whole_url = base_url + file_id + url_part1 + sheet_name + end_url
            outfile = row["Name"].replace(
                " ", "_") + "_" + tab.replace(" ", "_").replace("&", "_") + ".csv"
            logfile = "log." + outfile
            subprocess.call(["wget", "--output-file", logfile,
                            whole_url, "-O", outfile], cwd="../"+dir_name)
            print(whole_url)
        # subprocess.call(["cd", "../"])


if __name__ == "__main__":

    infile = sys.argv[1]
    url_df = pd.read_csv(infile)
    # infile = "./urlsTest.csv"
    tabs = "Desktop Standard Ads, Desktop Native Ads, Desktop Video Ads, Mobile Standard Ads, Mobile Native Ads, Mobile Video Ads"
    tab_list = tabs.split(", ")
    download_csv(url_df, tab_list)
    tab_list = ["Daily Ad Spend"]
    download_csv(url_df, tab_list)
    tab_list = ["Top Networks"]
    download_csv(url_df, tab_list)
    tab_list = ["Top Pub Categories"]
    download_csv(url_df, tab_list)
    tab_list = ['Similar%20%26%20Recommended']
    print(tab_list[0])
    download_csv(url_df, tab_list)
    tab_list = ["Creative Analysis"]
    download_csv(url_df, tab_list)
