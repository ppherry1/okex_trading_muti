# 公共参数及策略配置

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

# 账户列表API
api_dict = {
    'ppherry@126.com': {
        'apiKey': "",
        'secret': "",
    },
    'ppherry@163.com': {
        'apiKey': "",
        'secret': "",
    },
    'glasssquirrel@yeah.net': {
        'apiKey': "",
        'secret': "",
    },
    'ppherry@yeah.net': {
        'apiKey': "",
        'secret': "",
    },
}

# 设置主账户
main_account = 'ppherry@126.com'  # 主账户为资金储存和调度账户，不参与交易，建议为自己实名认证账户

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

CONTRACT_NUM = '211231'
symbol_config_dict = {
    'infnet': {
        'glasssquirrel@yeah.net': {
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
        }
    },
    'cta': {
        'ppherry@163.com': {
            'symbol_config':
                {
                    'fil-usdt': {'instrument_id': 'ETH-USDT-' + CONTRACT_NUM,  # 合约代码，当更换合约的时候需要手工修改
                                 'leverage': '3',  # 控制实际交易的杠杆倍数，在实际交易中可以自己修改。此处杠杆数，必须小于页面上的最大杠杆数限制
                                 'strategy_name': 'real_signal_random',  # 使用的策略的名称
                                 'para': [20, 2],
                                 },  # 策略参数
                    'link-usdt': {'instrument_id': 'LINK-USDT-' + CONTRACT_NUM,
                                  'leverage': '3',
                                  'strategy_name': 'real_signal_random',  # 不同币种可以使用不同的策略
                                  'para': [20, 2],
                                  },
                },
            'time_interval': '1h',
        },

        'ppherry@yeah.net': {
            'symbol_config':
                {
                    'ltc-usdt': {'instrument_id': 'LTC-USDT-' + CONTRACT_NUM,
                                 'leverage': '3',
                                 'strategy_name': 'real_signal_random',  # 不同币种可以使用不同的策略
                                 'para': [20, 2],
                                 },
                    'xrp-usdt': {'instrument_id': 'XRP-USDT-' + CONTRACT_NUM,
                                 'leverage': '3',
                                 'strategy_name': 'real_signal_random',  # 不同币种可以使用不同的策略
                                 'para': [20, 2],
                                 },
                },
            'time_interval': '30m',
        },
    },
}
