"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
根据定投策略，计算每次的定投金额
"""
import pandas as pd
import random


# 0定投
def real_auto_invest_0(df, now_pos, base_invest_val, invested_times, para):
    """
    每次定投0，做测试用。
    :param df:  原始数据
    :param para: 策略参数
    :return:
    """

    invest_val = 0.0

    return invest_val


# 一般等值定投
def real_auto_invest_equivalent_value(df, now_pos, base_invest_val, invested_times, para):
    """
    每次定投相同的预设本金。
    :param df:  原始数据
    :param para: 策略参数
    :return:
    """

    invest_val = base_invest_val

    return invest_val


# 邢大定投策略
def real_auto_invest_by_xbx(df, now_pos, base_invest_val, invested_times, para=[250, 2.0]):
    """
    以下思路假设按日K线描述，其实也支持按其他周期。
    邢大思路：收盘价高于x日均线，则按高出的比例，降低定投量；收盘价低于n日均线，则按低出的比例，增加定投量；
    收盘价偏离N日均线的比例，设定最大偏离度m。偏离度高于m则，定投降低比例按-m计；偏离度低于-m则，定投增加比例按m计。
    设：时间窗为n的均线值为median，基础定投量为x，最大偏离度为m，最近一次收盘价close。
    即，每次定投额 = x * (1 + max(min(1 - close / median, m), -m))
    返回值volume为正数，则买入；为负数，则卖出；为0，则本次不交易。
    :param invested_times:  已经定投的次数
    :param now_pos:  交易币种持仓量
    :param base_invest_val:  作为基准值的每次定投的基础币种量
    :param df:  原始数据
    :param para:  策略参数
    :return:
    """

    # ===策略参数
    n = int(para[0])  # 计算均线的时间窗
    m = para[1]  # 最大偏离度

    df['median'] = df['close'].rolling(n).mean()  # 计算均线
    median = df.iloc[-1]['median']  # 最近均线
    close = df.iloc[-1]['close']  # 最近收盘价
    invest_val = base_invest_val * (1 + max(min(1 - close / median, m), -m))

    return invest_val


# yi番茄定投策略
def real_auto_invest_by_yi_tomato(df, now_pos, base_invest_val, invested_times, para=[]):
    """
    以下思路假设按使用usdt交易btc描述，其实也支持其他币币交易。
    yi大大和番茄大大思路：基本思路为每次定投固定等usdt价值的btc，假设为10usdt，让第k次定投时持有的btc价值永远等于10 * k usdt。
    设：持仓量为now_pos，已经定投次数为invested_times，基础定投价值为base_invest_val，最近一次收盘价close。
    即，每次定投额 = base_invest_val * (invested_times + 1) - now_pos * close
    返回值volume为正数，则买入；为负数，则卖出；为0，则本次不交易。
    :param base_invest_val: 作为基准值的每次定投的基础币种量
    :param invested_times: 已经定投的次数
    :param now_pos: 交易币种持仓量
    :param df:  原始数据
    :param para:  策略参数
    :return:
    """

    close = df.iloc[-1]['close']  # 最近收盘价
    invest_val = base_invest_val * (invested_times + 1) - now_pos * close

    return invest_val


# 番茄大佬时间网格策略（仅网格）
def real_tomato_net(df, now_pos, base_invest_val, invested_times, para):
    """
    以下思路假设按使用usdt交易btc描述，其实也支持其他币币交易。
    番茄大大的时间网格思路：基本思路为维持固定以usdt计价的btc，多了就卖，少了就买，以达到高抛低吸的时间网格效果。
    策略操作为：第一次一次性投入作基准usdt计价的btc，然后定期检查btc的价值。
    设：现有btc持仓量为now_pos，目标的投资价值为target_val，最近一次收盘价close。
    即，每次定投额 = target_val - now_pos * close
    返回值volume为正数，则买入；为负数，则卖出；为0，则本次不交易。
    :param base_invest_val: 作为基准值的每次定投的基础币种量
    :param invested_times: 已经定投的次数
    :param now_pos: 交易币种持仓量
    :param df:  原始数据
    :param para:  策略参数
    :return:
    """
    target_val = float(para[0])  # 目标维持的价值量

    close = df.iloc[-1]['close']  # 最近收盘价
    invest_val = target_val - now_pos * close  # 本次交易量

    return invest_val


# 番茄大佬定投+时间网格策略（定投 + 网格）
def real_tomato_net_with_auto_invest(df, now_pos, base_invest_val, invested_times, para):
    """
    以下思路假设按使用usdt交易btc描述，其实也支持其他币币交易。
    番茄大大的定投+时间网格思路：基本思路为先定投一段时间，维持固定以usdt计价的btc，多了就卖，少了就买，以达到高抛低吸的时间网格效果。
    策略操作为：定投，然后每次检查持仓的btc的价值与目标价值的差额。
    设：现有btc持仓量为now_pos，基础定投金额为base_invest_val，目标的投资价值为target_val，最近一次收盘价close。
    即，每次定投额 = min(target_val - now_pos * close, base_invest_val)
    返回值volume为正数，则买入；为负数，则卖出；为0，则本次不交易。
    :param base_invest_val: 作为基准值的每次定投的基础币种量
    :param invested_times: 已经定投的次数
    :param now_pos: 交易币种持仓量
    :param df:  原始数据
    :param para:  策略参数
    :return:
    """

    target_val = float(para[0])  # 目标维持的价值量

    close = df.iloc[-1]['close']  # 最近收盘价
    invest_val = min(target_val - now_pos * close, base_invest_val)  # 比较定投量 与 目标价值量和实际持仓量 的差额，取二者较小值

    return invest_val



