"""
邢不行2020策略分享会
0607OKEx合约择时策略【多账户】实盘交易框架，版本1.0
邢不行微信：xbx9025
"""
import os


# =====常规config信息
# 获取项目根目录
_ = os.path.abspath(os.path.dirname(__file__))  # 返回当前文件路径
root_path = os.path.abspath(os.path.join(_, '..'))  # 返回根目录文件夹
data_save_dir = os.path.join(root_path, 'data', 'okex_future_trading_multi')

# 订单对照表
okex_order_type = {
    '1': '开多',
    '2': '开空',
    '3': '平多',
    '4': '平空',
}

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

# 币种面值对照表
coin_value_table = {
    "btc-usdt": 0.01,
    "eos-usdt": 10,
    "eth-usdt": 0.1,
    "ltc-usdt": 1,
    "bch-usdt": 0.1,
    "xrp-usdt": 100,
    "etc-usdt": 10,
    "bsv-usdt": 1,
    "trx-usdt": 1000}

# sleep时间配置
short_sleep_time = 1  # 用于和交易所交互时比较紧急的时间sleep，例如获取数据、下单
medium_sleep_time = 2  # 用于和交易所交互时不是很紧急的时间sleep，例如获取持仓
long_sleep_time = 10  # 用于较长的时间sleep

# timeout时间
exchange_timeout = 3000  # 3s


# ===各个子账户的api配置
# 手工输入每个子账户的api
api_dict = {
    'son1': {
        'apiKey': "5853f926-",
        'secret': "",
    },
    'son2': {
        'apiKey': "159f77be-",
        'secret': "",
    },
    'son3': {
        'apiKey': "53dba3e5-",
        'secret': "",
    },
    # 'son4': {
    #     'apiKey': "56739d25-",
    #     'secret': "",
    # },
    # 'son5': {
    #     'apiKey': "670aad81-",
    #     'secret': "",
    # },
    # 'son6': {
    #     'apiKey': "0ecf49a7-",
    #     'secret': "",
    # },
    # 'son7': {
    #     'apiKey': "b0c088ee-",
    #     'secret': "",
    # },
    # 'son8': {
    #     'apiKey': "2f7e6278-",
    #     'secret': "",
    # },
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


# ===配置每个子账户的交易相关参数symbol_config：
# 更新需要交易的合约、策略参数、下单量等配置信息
CONTRACT_NUM = '210625'
symbol_config_dict = {
    'glasssquirrel@yeah.net': {
        'symbol_config':
            {
                'eth-usdt': {'instrument_id': 'FIL-USDT-SWAP',  # 合约代码，当更换合约的时候需要手工修改
                             'leverage': '3',  # 控制实际交易的杠杆倍数，在实际交易中可以自己修改。此处杠杆数，必须小于页面上的最大杠杆数限制
                             'strategy_name': 'real_signal_random',  # 使用的策略的名称
                             'para': [20, 2],
                             },  # 策略参数
                # 'link-usdt': {'instrument_id': 'LINK-USDT-' + CONTRACT_NUM,
                #               'leverage': '3',
                #               'strategy_name': 'real_signal_random',  # 不同币种可以使用不同的策略
                #               'para': [20, 2],
                #               '},
                'btc-usdt': {'instrument_id': 'FIL-USDT',
                             'leverage': '3',
                             'strategy_name': 'real_signal_random',  # 不同币种可以使用不同的策略
                             'para': [20, 2],
                             },
                # 'xrp-usdt': {'instrument_id': 'XRP-USDT-' + CONTRACT_NUM,
                #              'leverage': '3',
                #              'strategy_name': 'real_signal_random',  # 不同币种可以使用不同的策略
                #              'para': [20, 2],
                #              },
            },
        'time_interval': '15m',
    },

    'ppherry@yeah.net': {
        'symbol_config':
            {
                'eth-usdt': {'instrument_id': 'ETH-USDT-' + CONTRACT_NUM,  # 合约代码，当更换合约的时候需要手工修改
                             'leverage': '3',  # 控制实际交易的杠杆倍数，在实际交易中可以自己修改。此处杠杆数，必须小于页面上的最大杠杆数限制
                             'strategy_name': 'real_signal_random',  # 使用的策略的名称
                             'para': [20, 2],
                             },  # 策略参数
                'eos-usdt': {'instrument_id': 'EOS-USDT-' + CONTRACT_NUM,
                             'leverage': '3',
                             'strategy_name': 'real_signal_random',  # 不同币种可以使用不同的策略
                             'para': [20, 2],
                             },
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

    # 'son3': {
    #     'symbol_config':
    #         {
    #             'eth-usdt': {'instrument_id': 'ETH-USDT-' + CONTRACT_NUM,  # 合约代码，当更换合约的时候需要手工修改
    #                          'leverage': '3',  # 控制实际交易的杠杆倍数，在实际交易中可以自己修改。此处杠杆数，必须小于页面上的最大杠杆数限制
    #                          'strategy_name': 'real_signal_random',  # 使用的策略的名称
    #                          'para': [20, 2],
    #                          },  # 策略参数
    #             'eos-usdt': {'instrument_id': 'EOS-USDT-' + CONTRACT_NUM,
    #                          'leverage': '3',
    #                          'strategy_name': 'real_signal_random',  # 不同币种可以使用不同的策略
    #                          'para': [20, 2],
    #                          },
    #             'ltc-usdt': {'instrument_id': 'LTC-USDT-' + CONTRACT_NUM,
    #                          'leverage': '3',
    #                          'strategy_name': 'real_signal_random',  # 不同币种可以使用不同的策略
    #                          'para': [20, 2],
    #                          },
    #             'xrp-usdt': {'instrument_id': 'XRP-USDT-' + CONTRACT_NUM,
    #                          'leverage': '3',
    #                          'strategy_name': 'real_signal_random',  # 不同币种可以使用不同的策略
    #                          'para': [20, 2],
    #                          },
    #         },
    #     'time_interval': '1h',
    # },
    #
    # 'son4': {
    #     'symbol_config':
    #         {
    #             'eth-usdt': {'instrument_id': 'ETH-USDT-' + CONTRACT_NUM,  # 合约代码，当更换合约的时候需要手工修改
    #                          'leverage': '3',  # 控制实际交易的杠杆倍数，在实际交易中可以自己修改。此处杠杆数，必须小于页面上的最大杠杆数限制
    #                          'strategy_name': 'real_signal_random',  # 使用的策略的名称
    #                          'para': [20, 2],
    #                          },  # 策略参数
    #             'eos-usdt': {'instrument_id': 'EOS-USDT-' + CONTRACT_NUM,
    #                          'leverage': '3',
    #                          'strategy_name': 'real_signal_random',  # 不同币种可以使用不同的策略
    #                          'para': [20, 2],
    #                          },
    #             'ltc-usdt': {'instrument_id': 'LTC-USDT-' + CONTRACT_NUM,
    #                          'leverage': '3',
    #                          'strategy_name': 'real_signal_random',  # 不同币种可以使用不同的策略
    #                          'para': [20, 2],
    #                          },
    #             'xrp-usdt': {'instrument_id': 'XRP-USDT-' + CONTRACT_NUM,
    #                          'leverage': '3',
    #                          'strategy_name': 'real_signal_random',  # 不同币种可以使用不同的策略
    #                          'para': [20, 2],
    #                          },
    #         },
    #     'time_interval': '2h',
    # },
    #
    # 'son5': {
    #     'symbol_config':
    #         {
    #             'eth-usdt': {'instrument_id': 'ETH-USDT-' + CONTRACT_NUM,  # 合约代码，当更换合约的时候需要手工修改
    #                          'leverage': '3',  # 控制实际交易的杠杆倍数，在实际交易中可以自己修改。此处杠杆数，必须小于页面上的最大杠杆数限制
    #                          'strategy_name': 'real_signal_simple_bolling',  # 使用的策略的名称
    #                          'para': [20, 2],
    #                          },  # 策略参数
    #             'eos-usdt': {'instrument_id': 'EOS-USDT-' + CONTRACT_NUM,
    #                          'leverage': '3',
    #                          'strategy_name': 'real_signal_simple_bolling',  # 不同币种可以使用不同的策略
    #                          'para': [20, 2],
    #                          },
    #             'ltc-usdt': {'instrument_id': 'LTC-USDT-' + CONTRACT_NUM,
    #                          'leverage': '3',
    #                          'strategy_name': 'real_signal_simple_bolling',  # 不同币种可以使用不同的策略
    #                          'para': [20, 2],
    #                          },
    #             'xrp-usdt': {'instrument_id': 'XRP-USDT-' + CONTRACT_NUM,
    #                          'leverage': '3',
    #                          'strategy_name': 'real_signal_simple_bolling',  # 不同币种可以使用不同的策略
    #                          'para': [20, 2],
    #                          },
    #         },
    #     'time_interval': '5m',
    # },
    #
    # 'son6': {
    #     'symbol_config':
    #         {
    #             'eth-usdt': {'instrument_id': 'ETH-USDT-' + CONTRACT_NUM,  # 合约代码，当更换合约的时候需要手工修改
    #                          'leverage': '3',  # 控制实际交易的杠杆倍数，在实际交易中可以自己修改。此处杠杆数，必须小于页面上的最大杠杆数限制
    #                          'strategy_name': 'real_signal_simple_bolling',  # 使用的策略的名称
    #                          'para': [20, 2],
    #                          },  # 策略参数
    #             'eos-usdt': {'instrument_id': 'EOS-USDT-' + CONTRACT_NUM,
    #                          'leverage': '3',
    #                          'strategy_name': 'real_signal_simple_bolling',  # 不同币种可以使用不同的策略
    #                          'para': [20, 2],
    #                          },
    #             'ltc-usdt': {'instrument_id': 'LTC-USDT-' + CONTRACT_NUM,
    #                          'leverage': '3',
    #                          'strategy_name': 'real_signal_simple_bolling',  # 不同币种可以使用不同的策略
    #                          'para': [20, 2],
    #                          },
    #             'xrp-usdt': {'instrument_id': 'XRP-USDT-' + CONTRACT_NUM,
    #                          'leverage': '3',
    #                          'strategy_name': 'real_signal_simple_bolling',  # 不同币种可以使用不同的策略
    #                          'para': [20, 2],
    #                          },
    #         },
    #     'time_interval': '15m',
    # },
    #
    # 'son7': {
    #     'symbol_config':
    #         {
    #             'eth-usdt': {'instrument_id': 'ETH-USDT-' + CONTRACT_NUM,  # 合约代码，当更换合约的时候需要手工修改
    #                          'leverage': '3',  # 控制实际交易的杠杆倍数，在实际交易中可以自己修改。此处杠杆数，必须小于页面上的最大杠杆数限制
    #                          'strategy_name': 'real_signal_simple_bolling',  # 使用的策略的名称
    #                          'para': [20, 2],
    #                          },  # 策略参数
    #             'eos-usdt': {'instrument_id': 'EOS-USDT-' + CONTRACT_NUM,
    #                          'leverage': '3',
    #                          'strategy_name': 'real_signal_simple_bolling',  # 不同币种可以使用不同的策略
    #                          'para': [20, 2],
    #                          },
    #             'ltc-usdt': {'instrument_id': 'LTC-USDT-' + CONTRACT_NUM,
    #                          'leverage': '3',
    #                          'strategy_name': 'real_signal_simple_bolling',  # 不同币种可以使用不同的策略
    #                          'para': [20, 2],
    #                          },
    #             'xrp-usdt': {'instrument_id': 'XRP-USDT-' + CONTRACT_NUM,
    #                          'leverage': '3',
    #                          'strategy_name': 'real_signal_simple_bolling',  # 不同币种可以使用不同的策略
    #                          'para': [20, 2],
    #                          },
    #         },
    #     'time_interval': '30m',
    # },
    #
    # 'son8': {
    #     'symbol_config':
    #         {
    #             'eth-usdt': {'instrument_id': 'ETH-USDT-' + CONTRACT_NUM,  # 合约代码，当更换合约的时候需要手工修改
    #                          'leverage': '3',  # 控制实际交易的杠杆倍数，在实际交易中可以自己修改。此处杠杆数，必须小于页面上的最大杠杆数限制
    #                          'strategy_name': 'real_signal_simple_bolling',  # 使用的策略的名称
    #                          'para': [20, 2],
    #                          },  # 策略参数
    #             'eos-usdt': {'instrument_id': 'EOS-USDT-' + CONTRACT_NUM,
    #                          'leverage': '3',
    #                          'strategy_name': 'real_signal_simple_bolling',  # 不同币种可以使用不同的策略
    #                          'para': [20, 2],
    #                          },
    #             'ltc-usdt': {'instrument_id': 'LTC-USDT-' + CONTRACT_NUM,
    #                          'leverage': '3',
    #                          'strategy_name': 'real_signal_simple_bolling',  # 不同币种可以使用不同的策略
    #                          'para': [20, 2],
    #                          },
    #             'xrp-usdt': {'instrument_id': 'XRP-USDT-' + CONTRACT_NUM,
    #                          'leverage': '3',
    #                          'strategy_name': 'real_signal_simple_bolling',  # 不同币种可以使用不同的策略
    #                          'para': [20, 2],
    #                          },
    #         },
    #     'time_interval': '1h',
    # },
}

# # =============新增配置================
# 资金平衡相关配置
# 母账户配置
main_config = {
    'apiKey': '',
    'secret': '',
    'password': '',
    'timeout': exchange_timeout,
    'rateLimit': 10,
    'hostname': HOST_NAME,  # 无法fq的时候启用
    'enableRateLimit': False
}
# 是否需要在订单完成之后rebalance资金
if_rebalance_amount = True
# rebalance 需要保留的资金
rebalance_amount = 250
# 子账户币币账户usdt阈值，超出这个阈值，把超出的资金转到母账户
rebalance_threshold = 1000
# 各个子账户注册的账户名称
account_alias = {
    'son1': '注册的子账户名称',
    'son2': '',
    'son3': '',
    'son4': '',
    'son5': ''
}
# 合约账户盈利超过这个比例，再平衡资金
future_profit_to_percent = '0'
# 合约账户亏损超过这个比例，再平衡资金
future_loss_to_percent = '0'