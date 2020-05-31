from datetime import date, timedelta

from crawler.upper_price_limit import get_upperpricelimit_stocks, get_upperpricelimit_histories


def main():
    curr_date = date(2020, 5, 29)
    while True:
        if curr_date < date(2019, 4, 1):
            break
        upperlimit_stocks = get_upperpricelimit_stocks(curr_date)
        if len(upperlimit_stocks) > 0:
            print(curr_date.strftime('%y%m%d'))
            for each in upperlimit_stocks:
                print(f"{each['name']} "
                      f"{[eachdate.strftime('%y%m%d') for eachdate in get_upperpricelimit_histories(each['code'])]}")
            print()
        curr_date -= timedelta(days=1)


if __name__ == '__main__':
    main()
