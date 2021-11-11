
import ccxt
from capital_function import *
from capital_allocate.capital_config import *
# from capital_strategy import *
from capital_allocate import capital_strategy

exchange = ccxt.okex()

pd.set_option('display.max_rows', 1000)
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
# 设置命令行输出时的列对齐功能
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

# =======配置参数======

# 母账户信息配置
OKEX_CONFIG_main = {
    'password': '8uu7yy6',
    'timeout': 3000,
    'rateLimit': 10,
    'hostname': 'okex.com',  # 无法fq的时候启用
    'apiKey': 'f6e246fc-7bc5-4261-ab0a-d671557ef612',
    'secret': '5BB67DA307D636AA71B223A81B3AF30F',
}

allocate_types_default = ['cta', 'autoinvest', 'infnet']  # 整理哪种类型的策略，目前可填项有：cta 择时，autoinvest 定投，infnet 时间无限网格
strategy_name_default = 'allocate_random'  # 执行的资金配置策略
strategy_para_default = ['USDT', {'cta': 0.4, 'autoinvest': 0.2}]  # 资金配置策略的参数
time_interval = '5m'  # 资金配置策略的执行周期，支持按分钟m，和按小时h
offset_minutes = 4  # 执行周期的偏移分钟数，例如周期1h，原8:00执行，offset_minutes=5，则改为8:05执行；offset_minutes=-5，则改为7:55执行
decimal_precision = 4  # 转账的小数点精度
skip_on_position = True  # 是否跳过有合约持仓的资金划转，为防止爆仓，建议为True。

exchange_main = ccxt.okex(OKEX_CONFIG_main)  # 母账户交易所


def capital_allocate_main(strategy_config=None):
    # 获取参数
    if strategy_config is not None:
        allocate_types = strategy_config['allocate_types']
        strategy_name = strategy_config['strategy_name']
        strategy_para = strategy_config['strategy_para']
    else:
        allocate_types = allocate_types_default
        strategy_name = strategy_name_default
        strategy_para = strategy_para_default
    # ===进入每次的循环

    exchange = {}  # 初始化ccxt子账户交易所
    accounts = {}  # 初始化ccxt子账户信息
    equity_curve = {}  # 初始化子账户资金曲线
    symbol_list = []  # 初始化子账户资金曲线
    futures_list = []  # 初始化子账户资金曲线
    swap_list = []  # 初始化子账户资金曲线
    spot_list = []  # 初始化子账户资金曲线
    # OKex market对照
    # market = exchange_main.load_markets()
    # market = pd.DataFrame(market).T
    #
    # # =获取策略执行时间，并sleep至该时间
    # if strategy_config is None:
    #     run_time = sleep_until_run_time(time_interval, offset_minutes=offset_minutes)

    # 循环每种策略的文件
    for allocate_type in allocate_types:
        # 循环执行每种策略的子账户名
        for sub_account_name in eval(allocate_type).api_dict.keys():
            # ===生成子账户交易所信息
            exchange[sub_account_name] = ccxt.okex(eval(allocate_type).OKEX_CONFIG_dict[sub_account_name])

            # ===获取子账户信息
            accounts[sub_account_name] = fetch_all_account_info(exchange[sub_account_name], sub_account_name)
            print(accounts[sub_account_name])

            # ===根据交易信息计算资金曲线
            # 初始化资金曲线
            equity_curve[sub_account_name] = {}
            # 相关代码暂未写

            # ===获取持仓
            get_position_list(exchange[sub_account_name], sub_account_name, futures_list, swap_list, spot_list)

            # ===获取策略涉及symbol信息
            get_symbol_list(allocate_type, sub_account_name, market, symbol_list)

    # ===整理持仓信息
    df_position = concat_position(futures_list, swap_list, spot_list)
    # ===整理策略涉及的symbol
    df_symbol = pd.concat(symbol_list)
    df_symbol.drop_duplicates(inplace=True)
    # 子账户信息整理
    sub_accounts = convert_accounts(accounts)

    # ===合并账户信息/持仓信息/策略涉及账户信息
    sub_accounts = pd.merge(sub_accounts, df_position, how='left',
                            on=['account_name', 'account_type', 'underlying'])
    sub_accounts = pd.merge(sub_accounts, df_symbol, how='outer',
                            on=['account_name', 'account_type', 'underlying', 'currency'])
    sub_accounts['max_withdraw'].fillna(0.0, inplace=True)

    # ===获取母账户的资金账户信息（母账户将只动用资金账户）
    main_account = fetch_wallet_account(exchange_main)

    # ===按照资金配置策略，计算子账户资金分配计划
    plan_sub_accounts = getattr(capital_strategy, strategy_name)(sub_accounts.copy(), main_account, equity_curve,
                                                                 strategy_para)
    # ===按照计划，进行资金划转
    allocate_accounts(exchange_main, sub_accounts, plan_sub_accounts, skip_on_position, decimal_precision=decimal_precision)

    # ===本次循环结束
    if strategy_config is None:
        print('\n', '-' * 20, '本次循环结束，%f秒后进入下一次循环' % 10, '-' * 20, '\n\n')
        time.sleep(10)
    else:
        print('-------资金配置策略执行完毕-------')


if __name__ == '__main__':
    while True:
        # try:
            capital_allocate_main()
        # except Exception as e:
        #     send_dingding_msg('系统出错，10s之后重新运行，出错原因：' + str(e))
        #     print(e)
        #     sleep(10)
