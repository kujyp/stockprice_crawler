from crawler.corp import get_krx_corplist


def main():
    corplist = get_krx_corplist()
    print(f'corplist length: [{len(corplist)}]')
    for eachcorp in corplist:
        print(eachcorp['name'])


if __name__ == '__main__':
    main()
