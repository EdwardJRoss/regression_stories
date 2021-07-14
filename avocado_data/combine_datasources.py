#!/usr/bin/env python
"""Combine old and new datasources to output dataset in ../data"""
from math import nan
from pathlib import Path
from typing import List

import pandas as pd

def historical_data_to_new_format(old_df: pd.DataFrame, new_columns: List[str]) -> pd.DataFrame:
    # Convert from $ to number
    old_df['ASP Current Year'] = old_df['ASP*'].str.replace(r'^\$([0-9.]+)$', r'\1', regex=True).apply(float)
    # Geography in Title case
    old_df['Geography'] = old_df['region'].str.title()
    # Convert to new date formatting
    old_df['Current Year Week Ending'] = pd.to_datetime(old_df['Week']).dt.strftime('%F 00:00:00')
    # Additional fields
    old_df['Timeframe'] = 'Weekly'
    old_df['Bulk GTIN'] = nan

    # Remaining columns
    col_mapping = {
        'type': 'Type',
        'Total Volume': 'Total Bulk and Bags Units',
        '4046': '4046 Units',
        '4225': '4225 Units',
        '4770': '4770 Units',
        'Total Bagged': 'TotalBagged Units',
        'Sml Bagged': 'SmlBagged Units',
        'Lrg Bagged': 'LrgBagged Units',
        'XLrg Bagged': 'X-LrgBagged Units',
    }

    return old_df.rename(columns=col_mapping)[new_columns]
    

if __name__ == '__main__':
    outpath = Path('../data/avocados.csv')
    outpath.parent.mkdir(exist_ok=True)

    new_df = pd.concat([pd.read_csv(path) for path in Path().glob('*-plu-total-hab-data.csv')])
    old_df = pd.concat([pd.read_csv(path) for path in Path().glob('*historic_hab_prices.csv')])

    df = pd.concat([new_df, historical_data_to_new_format(old_df, new_df.columns)])

    # Fixup issue with whitespace in new data
    df['Type'] = df['Type'].str.strip()

    # Add year column I assume is upstream
    df['Year'] = df['Current Year Week Ending'].apply(lambda x: x[:4])

    df.to_csv(outpath, index=False)



