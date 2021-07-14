Scripts to fetch and combine volume data from Hass Avocado Board

# `fetch_historic_data.py`

This downloads the historical data from the Internet Archives Wayback Machine and extracts it into CSVs of the form `{year}_historic_hab_prices.csv`, for the years 2015, 2016, and 2017.

Only US Total market data is available prior to 2015.

These files have been committed for convenience, so this script doesn't need to be run.

# `combine_datasources.py`

This combines the historical data with any recent data from the [Hass Avocado Board](https://hassavocadoboard.com/category-data/), which should be in files named `{year}-plu-total-hab-data.csv`.

The result is output into `../data/avocados.csv`.

