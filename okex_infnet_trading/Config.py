"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
择时策略实盘需要的配置参数
"""

# 订单状态对照表
okex_order_state = {
    '-2': '失败',
    '-1': '撤单成功',
    '0': '等待成交',
    '1': '部分成交',
    '2': '完全成交',
    '3': '下单中',
    '4': '撤单中',
}

# sleep时间配置
short_sleep_time = 1  # 用于和交易所交互时比较紧急的时间sleep，例如获取数据、下单
medium_sleep_time = 2  # 用于和交易所交互时不是很紧急的时间sleep，例如获取持仓
long_sleep_time = 10  # 用于较长的时间sleep
long_long_sleep_time = 30  # 用于较长的时间sleep

# timeout时间
exchange_timeout = 3000  # 3s

# 本策略目前只能设置一个子账户
api_dict = {
    'son1': {
        'apiKey': "",
        'secret': "",
    },
}

# 形成exchange_config
OKEX_CONFIG_dict = {}
HOST_NAME = 'okex.com'
for account_name in api_dict.keys():
    OKEX_CONFIG_dict[account_name] = {
        'password': '',
        'timeout': exchange_timeout,
        'rateLimit': 10,
        'hostname': HOST_NAME,  # 无法fq的时候启用
        'enableRateLimit': False}
    OKEX_CONFIG_dict[account_name]['apiKey'] = api_dict[account_name]['apiKey']
    OKEX_CONFIG_dict[account_name]['secret'] = api_dict[account_name]['secret']

symbol_config_dict = {
    'ppherry@yeah.net': {
        'symbol_config':
            {
                'EOS-USDT': {'instrument_id': 'EOS-USDT',  # 现货币对，-前是交易币，-后是计价币
                             'strategy_name': 'real_tomato_net',  # 定投策略
                             'base_invest_val': 1.0,  # 以计价货币计的基础定投额
                             'invested_times': 0,  # 策略开始时的已投资次数，请准确设定，否则会导致意外交易（不涉及投资次数的策略可随意设）
                             'para': [1.0],
                             },  # 策略参数，对于不涉及参数的策略可不设置
                'ETH-USDT': {'instrument_id': 'ETH-USDT',
                             'strategy_name': 'real_tomato_net',  # 不同币种可以使用不同的策略
                             'base_invest_val': 1.0,
                             'invested_times': 0,
                             'para': [1.0],
                             },
            },
    },
}
