# CityU  HACK 2019


## Data Sources
This project use the following datasets for ETF and Indexes:
* “Daily and Intraday Stock Price Data” from Kaggle.com(https://www.kaggle.com/borismarjanovic/daily-and-intraday-stock-price-data). It contains full historical daily (an intraday) price and volume data for all U.S.-based stocks and ETFs trading on the NYSE, NASDAQ, and NYSE MKT (Date, Open, High, Low, Close, Volume, OpenInt). This data set is adjusted for splits and dividends. Specifically, the daily data will be used.

* NASDAQ-100 Technology Index (NDXT) https://finance.yahoo.com/quote/%5ENDXT/history?p=^NDXT
* Volatility Index (VIX) http://www.cboe.com/products/vix-index-volatility/vix-options-and-futures
* NASDAQ Volatility Index (VXN) http://www.cboe.com/products/vix-index-volatility/volatility-on-stock-indexes/cboe-nasdaq-100-volatility-index-vxn

* List of best performing ETFs (http://etfdb.com/etfdb-category/technology-equities/%23etfs&sort_name=ytd_percent_return&sort_order=desc&page=1)

Engineered Features:
* Up_Down: defines whether the stock increased or decreased its price each day
* ETF’s Price Momentum
* ETF’s Price Volatility
* Sector’s Momentum - NDXT
* Sector’s Volatility - NDXT
* Market’s Momentum - VIX
* Market’s Volatility - VIX
* Market’s Momentum - VXN
* Market’s Volatility - VXN

These datasets will be combined into one dataframe for easy training and testing afterwards. This is, data from VIX, NXDT and VXN data sets will be brought in into one dataframe. The dataset contains 38921 rows for 13 “Tickers” with a data range from 2/23/2016 through 11/10/18.

