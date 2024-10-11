# COINMARKETCAP CRAWLER
Main feature: 
* Capture coinmarketcap.com data and write to csv file
* Using aiohttp, orjson, pandas for fast crawling and saving.
## Usage
### Prerequisites
```
pip install -r requirement.txt
```

### Quick start
```
python main.py -h
```

```
usage: CoinMarketCap crawler [-h] [-n NUMBER] [-l LIVE] [-his HISTORICAL]

optional arguments:
  -h, --help            show this help message and exit
  -n NUMBER, --number NUMBER
                        number of rows queried. Default = 400
  -l LIVE, --live LIVE  live data or no. If yes, data is captured each 5 minutes.
  -his HISTORICAL, --historical HISTORICAL
                        capture historical data. Default = latest

```

Example:

Query first 400 row by rank in latest data
```
python main.py
```
Equal to
```
python main.py -n 400 -his latest
```

Query first 100 row in 20210627
```
python main.py -n 100 -his 20210627
```

All data stored in `/YYYY/MM/DD/HH/MM.csv` in `data_dir` direction. You can format it.

Data field queried

```python
['cmc_rank', 'name', 'symbol', 'circulating_supply', 'USD.market_cap',
       'USD.price', 'USD.volume_24h', 'USD.percent_change_7d'],
```

### Performance

Uncomment the below code in line 66,67 in `crawler.py`
```python
execute_time = timeit.timeit(lambda: self.to_csv(data), number=number_of_repeat) / number_of_repeat
print(f"Average time for writing {self.no_of_row} records is {execute_time}")
```

```
Writing to csv file...
Average time for writing 400 records for 5 times is 0.01031728000000003
```

Average time is 0.01 for writing 400 records.


See more [orjson](https://github.com/ijl/orjson/tree/master) is best lib for parsing json response now.

| Library    |   compact (ms) |   pretty (ms) |   vs. orjson |
|------------|----------------|---------------|--------------|
| orjson     |           0.03 |          0.04 |          1   |
| ujson      |           0.18 |          0.19 |          4.6 |
| rapidjson  |           0.1  |          0.12 |          2.9 |
| simplejson |           0.25 |          0.89 |         21.4 |
| json       |           0.18 |          0.71 |         17   |

Beside `aiohttp` also a good lib for handling http request by leveraging asynchronous mechanism.