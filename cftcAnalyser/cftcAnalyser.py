#!/usr/bin/env python

from datetime import datetime
from dateutil.relativedelta import relativedelta
import math
import matplotlib.pyplot as plt
import yaml
import os
import pandas as pd
from zipfile import ZipFile

import cftcAnalyserUtils as utils

DATA_DIR = "data"

NAME = "Market_and_Exchange_Names"
DATE = "Report_Date_as_MM_DD_YYYY"
INTEREST = "Open_Interest_All"
LONG = "NonComm_Positions_Long_All"
SHORT = "NonComm_Positions_Short_All"

name_list = []
date_list = []
interest_list = []
long_list = []
short_list = []

num_of_entries = 0

three_years_ago = datetime.now() - relativedelta(years=3)
one_year_ago = datetime.now() - relativedelta(years=1)
three_months_ago = datetime.now() - relativedelta(months=3)
six_months_ago = datetime.now() - relativedelta(months=6)

extract_zip_files = True

def sortOnTime(val):
    return val[1]

def get_list_of_i_and_date_for_metric(expected_row_names):
    the_list = []
    for expected_row_name in expected_row_names:
        for i in range(0, num_of_entries):
            row_name = name_list[i]
            if row_name == expected_row_name:
                the_list.append((i, date_list[i]))
    the_list.sort(key=sortOnTime)
    return the_list

def get_latest_i(list_of_i_and_date, end_date=datetime.now()):
    latest_i = list_of_i_and_date[-1][0]
    for i, date in reversed(list_of_i_and_date):
        if date < end_date:
            latest_i = i
            break
    return latest_i

def get_second_latest_i(list_of_i_and_date, latest_i):
    previous_i = 0
    second_latest_i = 0
    for i, date in list_of_i_and_date:
        if i == latest_i:
            second_latest_i = previous_i
        else:
            previous_i = i
    return second_latest_i

def get_x_year_min_max(list_of_i_and_date, begin_date, end_date=datetime.now()):
    minimum = float('inf')
    maximum = float('-inf')
    for i, date in list_of_i_and_date:
        if date > begin_date:
            current = long_list[i] - short_list[i]
            if current < minimum:
                minimum = current
            if current > maximum:
                maximum = current
    return minimum, maximum

def calculate_x_year_avg(list_of_i_and_date, begin_date, end_date=datetime.now()):
    x_year_avg = 0
    entry_count = 0
    for i, date in list_of_i_and_date:
        if date >= begin_date and date <= end_date:
            x_year_avg += (long_list[i] - short_list[i])
            entry_count += 1
    if entry_count != 0:
        x_year_avg /= entry_count
    return x_year_avg

def calculate_z_score(list_of_i_and_date, begin_date, end_date=datetime.now()):
    z_score = 0
    entry_count = 0
    latest_i = get_latest_i(list_of_i_and_date, end_date)
    latest = long_list[latest_i] - short_list[latest_i]
    x_year_avg = calculate_x_year_avg(list_of_i_and_date, begin_date, end_date)
    for i, date in list_of_i_and_date:
        if date >= begin_date and date <= end_date:
            z_score += pow(((long_list[i] - short_list[i]) - x_year_avg), 2)
            entry_count += 1
    if entry_count != 0:
        z_score /= entry_count
        z_score = math.sqrt(z_score)
        if z_score != 0:
            z_score = (latest - x_year_avg) / z_score
    return z_score

def get_list_of_z_scores(list_of_i_and_date, year_count):
    the_list = []
    for i in range(0, 156):
        begin_date = datetime.now() - relativedelta(years=year_count, weeks=i)
        end_date = datetime.now() - relativedelta(weeks=i)
        the_list.append(calculate_z_score(list_of_i_and_date, begin_date, end_date))
    return the_list

def create_z_score_plot(list_of_i_and_date, path_to_figure):
    weeks = []
    for i in range(0,156):
        weeks.append(datetime.now() - relativedelta(weeks=i))
    weeks.reverse()

    z_score_list_one_year = get_list_of_z_scores(list_of_i_and_date, 1)
    z_score_list_three_year = get_list_of_z_scores(list_of_i_and_date, 3)
    z_score_list_one_year.reverse()
    z_score_list_three_year.reverse()

    plt.figure(figsize=[16,8], dpi=150)

    plt.plot(weeks, z_score_list_one_year, label = "Z-Score 1Y")
    plt.plot(weeks, z_score_list_three_year, label = "Z-Score 3Y")
    plt.xlabel('Date')
    plt.ylabel('Z-Score')
    plt.title('Historical Z-Scores for %s' % metric)
    plt.legend()
    plt.grid(axis='y')


    plt.savefig(path_to_figure)
    plt.close()

if not os.path.exists('html'):
    os.makedirs('html')

with open("metrics.yaml", 'r') as yf:
    metrics = yaml.safe_load(yf)

data_files = os.listdir(DATA_DIR)
for data_file in data_files:
    if ".zip" in data_file:
        data_file_name = data_file[:-4]

        if extract_zip_files:
            with ZipFile("%s/%s" % (DATA_DIR, data_file), 'r') as zipObj:
                listOfFileNames = zipObj.namelist()
                fileName = listOfFileNames[0]
                zipObj.extractall("/tmp")
                os.replace("/tmp/%s" % fileName, "/tmp/%s.xls" % data_file_name)

        xl = pd.ExcelFile("/tmp/%s.xls" % data_file_name)
        sheet_name = xl.sheet_names[0]
        df = pd.read_excel(xl, sheet_name, usecols=[NAME, DATE, INTEREST, LONG, SHORT])

        name_list += list(df[NAME])
        date_list += list(df[DATE])
        interest_list += list(df[INTEREST])
        long_list += list(df[LONG])
        short_list += list(df[SHORT])

num_of_entries = len(name_list)

z_scores_one_year = []
z_scores_three_year = []

cwd = os.getcwd()

with open('metrics.html', 'w') as f:
    utils.write_start_of_metric_html_file(f)

    for asset_class in metrics:
        for metric in metrics[asset_class]:
            list_of_i_and_date = get_list_of_i_and_date_for_metric(metrics[asset_class][metric])
            latest_i = get_latest_i(list_of_i_and_date)
            second_latest_i = get_second_latest_i(list_of_i_and_date, latest_i)
            latest = (long_list[latest_i] - short_list[latest_i])
            second_latest =  (long_list[second_latest_i] - short_list[second_latest_i])
            ww_change = latest - second_latest
            minimum, maximum = get_x_year_min_max(list_of_i_and_date, three_years_ago)
            three_month_avg = calculate_x_year_avg(list_of_i_and_date, three_months_ago)
            six_month_avg = calculate_x_year_avg(list_of_i_and_date, six_months_ago)
            one_year_avg = calculate_x_year_avg(list_of_i_and_date, one_year_ago)
            three_year_avg = calculate_x_year_avg(list_of_i_and_date, three_years_ago)
            z_score_one_year = calculate_z_score(list_of_i_and_date, one_year_ago)
            z_score_three_years = calculate_z_score(list_of_i_and_date, three_years_ago)
            
            path_to_figure = '%s/html/%s.png' % (cwd, metric)
            create_z_score_plot(list_of_i_and_date, path_to_figure)

            utils.write_line_in_metric_html_file(f, metric, latest, ww_change, three_month_avg, six_month_avg, one_year_avg,\
                maximum, minimum, z_score_one_year, z_score_three_years, path_to_figure)

    utils.write_end_of_metric_html_file(f)
