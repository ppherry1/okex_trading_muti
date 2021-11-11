import ccxt
import pandas as pd

# OKEX_CONFIG = {
#     'apiKey': '3ff63842-c363-49c2-afd4-7af13e52ec98',
#     'secret': 'DA07AD847B22C9D4FC76FDEDE4A07353',
#     'password': '8uu7yy6',
#     'timeout': 3000,
#     'rateLimit': 10,
#     # 'hostname': 'ouyi.fit',  # 无法fq的时候启用
#     'enableRateLimit': False}
# exchange = ccxt.okex5(OKEX_CONFIG)
#
# df = pd.DataFrame(exchange.private_get_account_positions()['data'], dtype=float)
# df2 = pd.DataFrame(exchange.private_get_account_balance()['data'][0]['details'])
#
# exchange.private_post_asset_withdrawal(params={
#     "amt": "1",
#     "fee": "0",
#     "pwd": "Aa123098",
#     "dest": "3",
#     "ccy": "USDT",
#     "toAddr": "glasssquirrel@yeah.net"
# }
# )
#
# df1 = pd.read_excel('d://TEST1.xlsx')
# df2 = pd.read_excel('d://TEST2.xlsx')
# df1.set_index('symbol', inplace=True)
# df2.set_index('symbol', inplace=True)
# #
# # df1.loc[df2['dy'] <= 2, 'sy'] = 1
#
# class A:
#     def __init__(self):
#         self.a = 1
#
# class B(A):
#     def __init__(self):
#         super().__init__()
#         self.b = 2
#
#
# asd = B()
# print(asd.b)

import sys


def test_func_name2():
	print(sys._getframe().f_code.co_name)


test_func_name2()  # test_func_name2