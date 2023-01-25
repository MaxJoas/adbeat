from selenium import webdriver
import time
import random
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import sys
from datetime import datetime, date
import time


def sleep():
    """ helper function to mimic human browser behaviour """
    sleep_sec = 0.8 + max(0, random.gauss(2, 1))
    time.sleep(sleep_sec)


def prepare_data(infile):
    """ reads in csv and generates a column with all detail URLs
    ARGS:
        infile - str: name of csv file with advertisers and start/end dates
    RETURNS:
        df - pd.DataFrame: dataframe with urls for each advertisers

    """
    df = pd.read_csv(infile)
    advertiser_list = df["Advertiser"].to_list()
    URL_DETAIL_PAGE_EASE = "https://app.adbeat.com/advertiser/de/all/"
    # generate url list for all advertisers
    url_detail_pages = [URL_DETAIL_PAGE_EASE +
                        advertiser for advertiser in advertiser_list]
    # add url detail page to df
    df["url_detail_page"] = url_detail_pages
    df["status"] = np.nan  # iniate empty column for logging
    return df


def navigate_to_datepicker(url_detail_page):
    """ opens selenium driver and navigates to date picker for given advertiser
    ARGS:
        url_detail_page - str: url of advertiser
    RETURNS:
        driver - selenium.webdriver: instave of webdriver opened date picker

    """
    driver.get(url_detail_page)
    # waits until page has loaded
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH,  "//*[@data-tip='Click to generate your report']"))).click()
    # click on Excel
    driver.find_element_by_xpath("//h2[@class='buttons']/div[3]").click()
    sleep()
    # open date picker in order to select all time
    driver.find_element_by_xpath(
        "//div[@class='date-range property no-border']").click()
    sleep()
    # select all time afet that date picker will close, so we neet to re-open
    driver.find_element_by_xpath("//li[contains(text(),'All time')]").click()
    driver.find_element_by_xpath(
        "//div[@class='date-range property no-border']").click()
    sleep()
    return driver


def count_end_date(endate, element_list):
    counter = 0
    for e in element_list:
        if e.text == endate:
            counter += 1
    return counter


def select_date_and_generate_report(df):
    """ iterartes over all advertisers and selects dates and generates report
    ARGS:
        df - pandas.DataFrame: df with advertiser and dates
    RETURNS:
        df - pandas.DataFrame: df with log column

    """
    log_list = []
    for index, row in df.iterrows():
        if df['Advertiser'][index] == 'searchstratnow.de':
            continue
        cur_status = "generated"
        url_detail_page = df["url_detail_page"][index]
        driver = navigate_to_datepicker(url_detail_page)
        start_year = str(df["start_year"][index])
        start_month = str(df["start_month"][index])
        start_day = str(df["start_day"][index])

        end_year = str(df["end_year"][index])
        end_month = str(df["end_month"][index])
        end_day = str(df["end_day"][index])
        start_date_helper = start_month + " " + start_year
        end_date_helper = end_month + " " + end_year
        print(df['Advertiser'][index])

        dates = driver.find_elements_by_xpath(
            "//div[@class='capitalized font-bold left']")
        start_date = dates[0].text
        end_date = dates[1].text
        i = 0
        while i < 200:
            i += 1
            dates = driver.find_elements_by_xpath(
                "//div[@class='capitalized font-bold left']")
            end_date = dates[1].text
            if end_date_helper == end_date:
                break
            try:
                driver.find_element_by_xpath(
                    "//span[@class='pointer back-one-month']").click()
            except:
                cur_status = "failed"
                break
        i = 0
        while i < 200:  # to click max 200 times
            i += 1
            dates = driver.find_elements_by_xpath(
                "//div[@class='capitalized font-bold left']")
            start_date = dates[0].text
            if start_date_helper == start_date:
                break
            try:
                driver.find_element_by_xpath(
                    "//span[@class='pointer forward-one-month']").click()
            except:
                cur_status = "failed"
                break

        dates_days = driver.find_elements_by_xpath(
            "//table[@class='month-view-table']/tbody/tr/td")
        end_date_count = count_end_date(end_day, dates_days)
        # find start day
        for d in dates_days:
            if d.text == start_day:
                try:
                    d.click()
                except:
                    cur_status = 'failed'
                    pass
                break

        # find end day
        counter = 1
        print(end_date_count)
        for d in dates_days:
            # first dates are the start dates so whe need this check
            if d.text == end_day and counter == end_date_count:
                counter += 1
                try:
                    print('endclick')
                    d.click()
                except:
                    cur_status = 'failed'
                    pass
                break
            if d.text == end_day:
                counter += 1
                pass

        # apply date range
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (By.XPATH,   "//*[contains(text(), 'Apply')]"))).click()
        except:
            cur_status = 'failed'
            pass
        driver.implicitly_wait(10)
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (By.XPATH,   "//*[contains(text(), 'Generate Report')]"))).click()
        except:
            print('failed')
            cur_status = 'failed'
            pass

        # log_list.append(cur_status)
        print(cur_status)

    df["status"] = log_list
    return df


if __name__ == '__main__':
infile = "./year_in.csv"
infile = './Postbank.csv'
infile = r"C:\Users\anna\OneDrive\Dokumente\Python\Download - CSVInput_Python.csv"
df = prepare_data(infile)
x = 341

df.iloc[x]["Advertiser"]
df.shape
# TODO ANNA x =
if not x == 0:
    df = df.iloc[x:]
    print(df.iloc[0]["Advertiser"])
### ---- maybe useful later --- ####
# options = webdriver.ChromeOptions()
# chrome_profile = "/home/max/.config/google-chrome/Default"
# options.add_argument(chrome_profile)
# --------------------------------------------------------------------

# initiate driver (may need to login manually)
driver = webdriver.Chrome('/usr/bin/chromedriver')
# driver = webdriver.Chrome(executable_path=driver_path)

# Aufrufen Seite adbeat
driver.get("https://app.adbeat.com/")
df = select_date_and_generate_report(df)
timestr = time.strftime("%Y%m%d-%H%M%S")
filename = 'outfile' + timestr + '.csv'
df.to_csv(filename)
df['start_day']
# searchstratnow 2019 fehlt
# braun.de wieder starten
