"""
邢不行2020策略分享会
0607OKEx合约择时策略【多账户】实盘交易框架，版本1.0
邢不行微信：xbx9025
"""
import ccxt
import os
import sys
from time import sleep
import pandas as pd
from datetime import datetime
from okex_cta_trading.Config import *
from okex_cta_trading.Function import *
pd.set_option('display.max_rows', 1000)
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
# 设置命令行输出时的列对齐功能
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)


"""
程序思路：

整体思路仍然和原来的单账户程序没有太大变化。

只不过原来单账户程序在获取最新数据时，是从okex服务器获取，现在多账户程序是从本地获取。
"""


# 测试时ccxt版本为1.27.28。若不是此版本，可能会报错，可能性很低。print(ccxt.__version__)可以查看ccxt版本。



# ===读取程序运行所需的子账号相关参数
if len(sys.argv) > 1:
    account_name = sys.argv[1]
else:
    print('未指定account_name参数，程序exit')
    exit()
print('子账户id：', account_name)

# ===配置运行相关参数
# =从config中读取相关配置信息
exchange = ccxt.okex(OKEX_CONFIG_dict[account_name])
symbol_config = symbol_config_dict[account_name]['symbol_config']
print('交易信息：', symbol_config)
# =执行的时间间隔
time_interval = symbol_config_dict[account_name]['time_interval']
print('时间周期：', time_interval)

# =程序是否并行获取数据、下单等。并行速度较快，串行较慢。(但在windows上，因为代码原因，可能反而串行会快一点，特别是在交易币种不是很多的时候，请自行测试)
if_multi_thread = False  # 若为False，则为串行。建议使用串行。
# MOD 配置逐仓OR全仓

# =钉钉
# 在一个钉钉群中，可以创建多个钉钉机器人。
# 建议单独建立一个报错机器人，该机器人专门发报错信息。请务必将报错机器人在id和secret放到function.send_dingding_msg的默认参数中。
# 当我们运行多策略时，会运行多个python程序，建议不同的程序使用不同的钉钉机器人发送相关消息。每个程序的开始部分加上该机器人的id和secret
robot_id = ''
secret = ''
robot_id_secret = [robot_id, secret]


def main():

    # ===首次运行时获取持仓数据
    # 初始化symbol_info，在每次循环开始时都初始化
    symbol_info_columns = ['账户权益', '持仓方向', '持仓量', '持仓收益率', '持仓收益', '持仓均价', '当前价格', '最大杠杆']  # MOD 还需with_draw
    symbol_info = pd.DataFrame(index=symbol_config.keys(), columns=symbol_info_columns)  # 转化为dataframe

    # 更新账户信息symbol_info
    symbol_info = update_symbol_info(exchange, symbol_info, symbol_config)
    print('\nsymbol_info:\n', symbol_info, '\n')

    # ===进入每次的循环
    while True:
        print('子账户id：', account_name, '时间周期：', time_interval)

        # =获取策略执行时间，并sleep至该时间
        run_time = sleep_until_run_time(time_interval)

        # =获取所有币种最近数据（可以根据需要，改成并行）
        symbol_candle_data = {}
        for symbol in symbol_config.keys():
            p = os.path.join(data_save_dir, 'data_ready_%s_%s_%s' % (symbol, time_interval, str(run_time).replace(':', '-')))
            print('获取数据地址：', p)
            while True:
                if os.path.exists(p):
                    print('数据已经存在：', datetime.now())
                    break
                if datetime.now() > run_time + timedelta(minutes=1):
                    print('时间超过1分钟，放弃从文件读取数据，返回空数据')
                    break
            symbol_candle_data[symbol] = pd.read_csv(os.path.join(data_save_dir, '%s_%s.csv' % (symbol, time_interval)))
            symbol_info.loc[symbol, '信号价格'] = symbol_candle_data[symbol].iloc[-1]['close']  # 该品种的最新价格
            print(symbol_candle_data[symbol].tail(5))

        # =计算每个币种的交易信号
        symbol_signal = calculate_signal(symbol_info, symbol_config, symbol_candle_data)
        print('\nsymbol_info:\n', symbol_info)
        print('本周期交易计划:', symbol_signal)

        # =下单
        symbol_order = pd.DataFrame()
        if symbol_signal:
            if if_multi_thread:  # 并行
                symbol_order = multi_threading_place_order(exchange, symbol_info, symbol_config, symbol_signal)  # 多线程下单
            else:
                symbol_order = single_threading_place_order(exchange, symbol_info, symbol_config, symbol_signal)  # 单线程下单
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
        dingding_report_every_loop(symbol_info, symbol_signal, symbol_order, run_time, robot_id_secret)

        # 本次循环结束
        print('\n', '-' * 20, '本次循环结束，%f秒后进入下一次循环' % long_sleep_time, '-' * 20, '\n\n')
        time.sleep(long_sleep_time)


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            send_dingding_msg('系统出错，10s之后重新运行，出错原因：' + str(e))
            print(e)
            sleep(long_sleep_time)
