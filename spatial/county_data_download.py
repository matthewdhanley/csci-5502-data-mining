#!/usr/bin/env python3
# -*-coding: utf-8 -*-
"""Download US census business patterns data by county"""

import numpy as np
from urllib.request import urlretrieve
import zipfile
import pandas as pd
import os


zipcode_target_file = './data/zipcodes/zip_list.csv'
target_state_fip = 32 # Nevada
year_list = range(4,17)

cbp_base = 'https://www2.census.gov/programs-surveys/cbp/datasets/'

def filter_state(basename, target_fip):
    df = pd.read_csv(basename, compression='zip')
    df.columns = [x.lower() for x in df.columns]
    filter_df = df.loc[df['fipstate'] == target_state_fip]
    out_path = 'data/{}'.format(basename.replace('.zip', '.csv'))
    filter_df.to_csv(out_path, index=False)
    os.remove(basename)

    return

def filter_zipcodes(basename, zipcode_target_file):
    df = pd.read_csv(basename, compression='zip')
    df.columns = [x.lower() for x in df.columns]
    with open(zipcode_target_file) as f:
        target_zipcodes = f.read().splitlines()
    print(target_zipcodes)
    filter_df = df.loc[df['zip'].isin(target_zipcodes)]
    out_path = 'data/{}'.format(basename.replace('.zip', '.csv'))
    filter_df.to_csv(out_path, index=False)
    os.remove(basename)

    return

def dload_filter_data(year, target_fip, zipcode_target_file):
    yr_str = str(year).zfill(2)
    yr_full = '20{}'.format(yr_str)
#     cbp_co_basename = 'cbp{}co.zip'.format(yr_str)
    cbp_zip_basename = 'zbp{}detail.zip'.format(yr_str)
#     cbp_co_remote = '{}{}/{}'.format(cbp_base, yr_full, cbp_co_basename)
    cbp_zip_remote = '{}{}/{}'.format(cbp_base, yr_full, cbp_zip_basename)

#     urlretrieve(cbp_co_remote, cbp_co_basename)
#     filter_state(cbp_co_basename, target_fip)
    urlretrieve(cbp_zip_remote, cbp_zip_basename)
    filter_zipcodes(cbp_zip_basename, zipcode_target_file)

    return


def main():
    for y in year_list:
        dload_filter_data(y, target_state_fip, zipcode_target_file)

if __name__ == '__main__':
    main()

