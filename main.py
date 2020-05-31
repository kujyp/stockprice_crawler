from crawler.corp import get_krx_corplist
from crawler.upper_price_limit import get_upperpricelimit_histories


def main():
    corplist = get_krx_corplist()
    upperlimithistories_dict = {}
    for eachcorp in corplist:
        upperlimithistories = get_upperpricelimit_histories(eachcorp['code'])
        upperlimithistories_dict[eachcorp['name']] = upperlimithistories
        upperlimithistories_str = [eachdate.strftime('%y%m%d') for eachdate in upperlimithistories]
        print("{0:{1}}".format(f"[{eachcorp['name']}]", 20)
              + "\t" + "{0:{1}}".format(f"[{len(upperlimithistories_str)}]", 4)
              + f" [{' '.join(upperlimithistories_str)}]")


if __name__ == '__main__':
    main()
