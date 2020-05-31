from crawler.upper_price_limit import get_upperpricelimit_histories


def main():
    eachcorp = {
        'name': '모헨즈',
        'corpcode': '006920',
    }
    upperlimithistories_str = [eachdate.strftime('%y%m%d') for eachdate in get_upperpricelimit_histories(eachcorp['corpcode'])]
    print("{0:{1}}".format(f"[{eachcorp['name']}]", 20)
          + "\t" + "{0:{1}}".format(f"[{len(upperlimithistories_str)}]", 4)
          + f" [{' '.join(upperlimithistories_str)}]")
    print()


if __name__ == '__main__':
    main()
