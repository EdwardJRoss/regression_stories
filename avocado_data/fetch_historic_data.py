#!/usr/bin/env python
"""Fetch 2015-2018 US Avocado Price Data from Hass Avocado Board via Wayback Machine"""
from io import StringIO
import logging
from pathlib import Path

import pandas as pd
import parsel
import requests

# Internet Arhcive Wayback Machine URLS for the data
# Don't use 2018 because we can get it from new source
YEAR_URLS = {
#    2018: 'https://web.archive.org/web/20180702225144/http://www.hassavocadoboard.com/retail/volume-and-price-data',
    2017: 'https://web.archive.org/web/20181019025120/http://www.hassavocadoboard.com/retail/volume-and-price-data/historical-volume-and-price-data/2017',
    2016: 'https://web.archive.org/web/20181019024959/http://www.hassavocadoboard.com/retail/volume-and-price-data/historical-volume-and-price-data/2016',
    2015: 'https://web.archive.org/web/20180621015746/http://www.hassavocadoboard.com/retail/volume-and-price-data/historical-volume-and-price-data/2015',
}

def extract_hass_table(region_table: parsel.SelectorList) -> pd.DataFrame:
    region = region_table.css('.rvpMarketTitle::text').get()
    table_header = [r.strip() for r in region_table.css('table.retailVolumePriceNew')[0].css('td::text').getall() if r.strip()]
    
    tables = region_table.css('table.retailVolumePriceNew')[1].get()
    # The first extracted table contains all the data concatenated as a string
    pd_tables = pd.read_html(StringIO(tables))[1:]
    
    df = pd.concat([table.T for table in pd_tables])
    df.columns = table_header
    df['region'] = region
    
    return df

def extract_hass_tables(html: str) -> pd.DataFrame:
    sel = parsel.Selector(html)
    
    tables = []
    for region_table in sel.css('div.retailVolumeNew'):
        df = extract_hass_table(region_table)
        df['type'] = 'Conventional'
        tables.append(df)
        
    for region_table in sel.css('div.retailVolumeOrg'):
        df = extract_hass_table(region_table)
        df['type'] = 'Organic'
        tables.append(df)
        
    return pd.concat(tables)

def main(outfile_pattern, year_urls) -> None:
    for year, url in year_urls.items():
        outfile = f'{year}_{outfile_pattern}'
        if Path(outfile).exists():
            continue

        logging.info(f'Fetching {year} from {url}')
        r = requests.get(url)

        logging.info(f'Parsing {year}')
        df_year = extract_hass_tables(r.text)
        df_year['year'] = year

        logging.info(f'Writing {year} to {outfile}')
        df_year.to_csv(outfile, index=False)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    main('historic_hab_prices.csv', YEAR_URLS)
