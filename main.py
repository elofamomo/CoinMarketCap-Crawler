import argparse
from crawler import Crawler

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="CoinMarketCap crawler")
    parser.add_argument('-n', '--number', default=400, help="number of rows queried. Default = 400 (max 5000)", type=int)
    parser.add_argument('-l', '--live', default=False, help="live data or no. If yes, data is captured each 5 minutes.",
                        type=bool)
    parser.add_argument('-his', '--historical', default="latest", help="capture historical data. Default = latest", type=str)
    args = parser.parse_args()
    crawler = Crawler(args.number, args.live, args.historical)
    crawler.run()
