from typing import List, Dict

import pandas as pd


def get_krx_corplist() -> List[Dict[str, str]]:
    ret = []
    ret.append({'name': '삼성전자우', 'code': '005935'})

    code_df = pd.read_html(
        'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13',
        header=0)[0]
    code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)
    code_df = code_df[['회사명', '종목코드']]
    for idx, each in code_df.회사명.items():
        ret.append({
            'name': each,
            'code': code_df.종목코드[idx],
        })

    return ret
