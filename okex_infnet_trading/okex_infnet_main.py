"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
介绍择时策略实盘
"""
import ccxt
from time import sleep
import pandas as pd
from datetime import datetime
from okex_infnet_trading.Function import *
from okex_infnet_trading.Config import *

pd.set_option('display.max_rows', 1000)
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
# 设置命令行输出时的列对齐功能
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

# 测试时ccxt版本为1.27.28。若不是此版本，可能会报错，可能性很低。print(ccxt.__version__)可以查看ccxt版本。

# =====配置运行相关参数=====

# =底层数据时间粒度 # MOD
time_interval = '1m'  # 目前支持以m或h为单位,数字须为整数。得okex支持的K线才行。最好不要低于5m。
# 常用：1分钟线1m，5分钟线5m，15分钟线15m，30分钟线30m，小时线60m或1h，4小时线240m或4h，日线1440m或24h，周线10080m或168h。最大值为10080m或168h

# =执行的时间间隔（多长时间执行一次定投） # MOD ADD
execution_interval = '1m'  # 必须和time_interval使用相同单位，即同为m或同为h，最好是time_interval的整数倍数。
# 常用：1分钟投1m，5分钟投5m，15分钟投15m，30分钟投30m，小时投60m或1h，4小时投240m或4h，日投1440m或24h，周投10080m或168h，月投（4周）40320m或672h。

# =钉钉
# 在一个钉钉群中，可以创建多个钉钉机器人。
# 建议单独建立一个报错机器人，该机器人专门发报错信息。请务必将报错机器人在id和secret放到function.send_dingding_msg的默认参数中。
robot_id = ''
secret = ''
robot_id_secret = [robot_id, secret]

account_name = [key for key in api_dict.keys()][0]

# =交易所配置
OKEX_CONFIG = OKEX_CONFIG_dict[account_name]
exchange = ccxt.okex(OKEX_CONFIG)

# =====配置交易相关参数=====
# 更新需要交易的合约、策略参数、下单量等配置信息
symbol_config = symbol_config_dict[account_name]['symbol_config']


def main():
    # =====获取需要交易币种的历史数据=====
    max_len = 1000  # 设定最多收集多少根K线，okex不能超过1440根
    symbol_candle_data = dict()  # 用于存储K线数据
    # 遍历获取币种历史数据
    for symbol in symbol_config.keys():
        # 获取币种的历史数据，会删除最新一行的数据
        symbol_candle_data[symbol] = fetch_okex_symbol_history_candle_data(exchange,
                                                                           symbol_config[symbol]['instrument_id'],
                                                                           time_interval, max_len=max_len)
        time.sleep(medium_sleep_time)

    # ===进入每次的循环
    while True:

        # =获取持仓数据
        # 初始化symbol_info，在每次循环开始时都初始化
        symbol_info_columns = ['计价币种持仓量', '交易币种持仓量']
        symbol_info = pd.DataFrame(index=symbol_config.keys(), columns=symbol_info_columns)  # 转化为dataframe

        # 更新账户信息symbol_info
        symbol_info = update_symbol_info(exchange, symbol_info, symbol_config)
        print('\nsymbol_info:\n', symbol_info, '\n')

        # =获取策略执行时间，并sleep至该时间
        run_time = sleep_until_run_time(execution_interval)

        # =并行获取所有币种最近数据
        exchange.timeout = 1000  # 即将获取最新数据，临时将timeout设置为1s，加快获取数据速度
        candle_num = int(int(execution_interval[:-1]) / int(time_interval[:-1])) + 10  # 获取从上次运行开始未获取的K线
        # 获取数据
        recent_candle_data = single_threading_get_data(exchange, symbol_info, symbol_config, time_interval, run_time,
                                                       candle_num)
        for symbol in symbol_config.keys():
            print(recent_candle_data[symbol].tail(2))

        # 将symbol_candle_data和最新获取的recent_candle_data数据合并
        for symbol in symbol_config.keys():
            df = symbol_candle_data[symbol].append(recent_candle_data[symbol], ignore_index=True)
            df.drop_duplicates(subset=['candle_begin_time_GMT8'], keep='last', inplace=True)
            df.sort_values(by='candle_begin_time_GMT8', inplace=True)  # 排序，理论上这步应该可以省略，加快速度
            df = df.iloc[-max_len:]  # 保持最大K线数量不会超过max_len个
            df.reset_index(drop=True, inplace=True)
            symbol_candle_data[symbol] = df

        # =计算每个币种的交易信号
        symbol_info = calculate_trade_vol(symbol_info, symbol_config, symbol_candle_data)
        print('\n现货持仓与本次定投计划:\n', symbol_info)

        # =下单
        exchange.timeout = exchange_timeout  # 下单时需要增加timeout的时间，将timout恢复正常

        symbol_order = single_threading_place_order(exchange, symbol_info, symbol_config)  # 单线程下单
        print('下单记录：\n', symbol_order)

        # 更新订单信息，查看是否完全成交
        time.sleep(short_sleep_time)  # 休息一段时间再更新订单信息
        symbol_order = update_order_info(exchange, symbol_config, symbol_order)
        print('更新下单记录：', '\n', symbol_order)

        # 重新更新账户信息symbol_info
        time.sleep(long_sleep_time)  # 休息一段时间再更新
        symbol_info = pd.DataFrame(index=symbol_config.keys(), columns=symbol_info_columns)
        symbol_info = update_symbol_info(exchange, symbol_info, symbol_config)
        print('\nsymbol_info:\n', symbol_info, '\n')

        # 发送钉钉
        dingding_report_every_loop(symbol_info, symbol_order, run_time, robot_id_secret, symbol_config)

        # 本次循环结束
        print('\n', '-' * 20, '本次循环结束，%f秒后进入下一次循环' % long_sleep_time, '-' * 20, '\n\n')
        time.sleep(long_sleep_time)


if __name__ == '__main__':
    while True:
        # try:
            main()
        # except Exception as e:
        #     send_dingding_msg('系统出错，10s之后重新运行，出错原因：' + str(e))
        #     print(e)
        #     sleep(long_sleep_time)
