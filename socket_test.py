import ccxt
from Function import *

print(ccxt.__version__)  # 检查ccxt版本，需要最新版本，1.44.21以上

# ===参数设定
coin = 'xrp'.upper()  # 要套利的币种
future_date = '210625'  # 要套利的合约到期时间
coin_list = ['BTC', 'BNB', 'DOT',
             'ETH', 'BCH', 'LTC',
             'ADA', 'LINK', 'XRP']

coin_precision = {
    'BTC': 1,  # 小数点后1位
    'BNB': 3,  # 小数点后3位
    'DOT': 3,
    'ETH': 2,
    'BCH': 2,
    'LTC': 2,
    'ADA': 5,
    'LINK': 3,
    'XRP': 4,
}
# 去行情页面上，看下这个币种合约的价格是小数点后几位。如果小数点后有3位，那么coin_precision就是3
execute_amount = 100  # 每次建仓usdt的数量。如果是btc的话，得是100的整数倍。其他币种得是10的整数倍。每次数量不要太多，太多会造成价格波动。建议数量在1000-3000之间。
max_execute_num = 2  # 最大建仓次数。两次后阈值上调千分之一。
r_threshold = 0.0915  # 高于利差就开始入金，0.05代表5%，初始利差阈值
spot_fee_rate = 0  # 根据自己的手续费进行修改。如果是bnb支付，可以修改为0。
future_fee_rate = 0  # 根据自己的手续费进行修改。如果是bnb支付，可以修改为0。
contact_size = {
    'BTC': 100,  # 一张合约代表100美金
    'BNB': 10,  # 一张合约代表10美金
    'DOT': 10,
    'ETH': 10,
    'BCH': 10,
    'LTC': 10,
    'ADA': 10,
    'LINK': 10,
    'XRP': 10,
    }  # 你套利的币种一定要在这个dict里面

# ===创建交易所
exchange = ccxt.binance()
exchange.apiKey = 'YbD6'
exchange.secret = 'HXNW'

# ===开始套利
execute_num = 0  #成交次数
execute_num_not = 0  #未成交次数
# spot_symbol_name = {'type1': coin + 'USDT', 'type2': coin + '/USDT'}
# future_symbol_name = {'type1': coin + 'USD_' + future_date}
while True:
    # ===计算价差
    # 获取现货卖一数据。因为现货是买入，取卖一。
    # noinspection PyUnresolvedReferences
    for coin in coin_list:
        spot_symbol_name = {'type1': coin + 'USDT', 'type2': coin + '/USDT'}
        future_symbol_name = {'type1': coin + 'USD_' + future_date}
        spot_sell1_price = exchange.fapiPublicGetTickerBookTicker(params={'symbol': spot_symbol_name['type1']})['askPrice']
        # 获取期货买一数据。因为期货是卖出，取买一。
        # noinspection PyUnresolvedReferences
        future_buy1_price = exchange.dapiPublicGetTickerBookTicker(params={'symbol': future_symbol_name['type1']})[0][
            'bidPrice']

        # 计算价差
        r = float(future_buy1_price) / float(spot_sell1_price) - 1
        print(coin)
        print('现货价格：%.4f，期货价格：%.4f，价差：%.4f%%' % (float(spot_sell1_price), float(future_buy1_price), r * 100))

    # ===判断价差是否满足要求
        if r < r_threshold:
            print('利差小于目标阀值，不入金')
            execute_num_not += 1
        else:
            print('利差大于目标阀值，开始入金')

            # 计算开空合约的数量、买入现货币的数量
            future_contract_num = int(execute_amount / contact_size[coin])  # 买入合约张数
            future_coin_num = future_contract_num * contact_size[coin] / float(future_buy1_price)  # 合约对应币数量
            future_fee = future_coin_num * future_fee_rate  # 需要取整
            spot_amount = future_coin_num / (1 - spot_fee_rate) + future_fee  # 需要取整
            print('交易计划：开空合约张数：', future_contract_num, '对应币数量', future_coin_num, '合约手续费', future_fee,
                  '需要买入现货数量', spot_amount, '\n')

            # 买币
            price = float(spot_sell1_price) * 1.01
            spot_order_info = binance_spot_place_order(exchange=exchange, symbol=spot_symbol_name['type2'],
                                                       long_or_short='买入', price=price, amount=spot_amount)

            # 做空合约
            price = float(future_buy1_price) * 0.99
            price = round(price, coin_precision[coin])
            future_order_info = binance_future_place_order(exchange=exchange, symbol=future_symbol_name['type1'],
                                                           long_or_short='开空', price=price, amount=future_contract_num)

            # 获取币币账户买入币的数量
            time.sleep(2)
            balance = exchange.fetch_balance()
            num = balance[coin]['free']
            print('待转账的币的数量：', num)

            # 将币币交易所买到的币转到合约账户
            binance_account_transfer(exchange=exchange, currency=coin, amount=num, from_account='币币',
                                     to_account='合约')

            # 计数
            execute_num += 1

            print(spot_order_info['average'])
            print(future_order_info)

        # ===循环结束
        print('*' * 20, '本次循环结束，暂停', '*' * 20, '\n')
        time.sleep(1)

        if execute_num >= max_execute_num:  # 成交次数大于2，价差加0.1%
            r_threshold = r_threshold + 0.001
            execute_num = 0
        print(execute_num)
        if execute_num_not >= 600:       # 未成交次数大于600，十分钟，并且价差大于7.5% 的时候  价差减0.1% 并且重置未成交次数
            if r_threshold > 0.085:  #最低价差
                r_threshold = r_threshold - 0.001
                execute_num_not = 0
        print(r_threshold, execute_num_not)