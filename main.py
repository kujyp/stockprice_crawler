from crawler.upper_price_limit import get_upperpricelimit_histories
from crawler.utils.consts import CORPCODE_KCS, CORPCODE_SAMSUNG_ELECTRONICS


def main():
    print('KCS')
    print(get_upperpricelimit_histories(CORPCODE_KCS))
    print()
    print('삼성전자')
    print(get_upperpricelimit_histories(CORPCODE_SAMSUNG_ELECTRONICS))
    print()
    print('토탈소프트')
    print(get_upperpricelimit_histories('045340'))
    print()


if __name__ == '__main__':
    main()
