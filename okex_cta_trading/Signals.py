import pandas as pd
import random
import talib as ta
import numpy as np


# 将None作为信号返回
def real_signal_none(df, now_pos, avg_price, para):
    """
    发出空交易信号
    :param df:
    :param now_pos:
    :param avg_price:
    :param para:
    :return:
    """
    return None


# 随机生成交易信号
def real_signal_random(df, now_pos, avg_price, para):
    """
    随机发出交易信号
    :param df:
    :param now_pos:
    :param avg_price:
    :param para:
    :return:
    """
    r = random.random()
    if r <= 0.25:
        return 1
    elif r <= 0.5:
        return -1
    elif r <= 0.75:
        return 0
    else:
        return None


# 布林策略
def real_signal_simple_bolling_ww(df, now_pos, avg_price, para=[200, 2]):
    """
    平均差布林+均线回归W+PC平仓+AR过滤
    """
    # ===策略参数
    n = int(para[0])
    m = para[1]
    # 固定参数
    a = 13
    # ===计算指标
    # 计算均线
    df['median'] = ta.LINEARREG(df['close'], timeperiod=a)
    df['median'] = ta.WMA(df['median'], timeperiod=n)
    # 平仓均线
    df['pc'] = ta.TEMA(df['close'], timeperiod=a)
    # ar过滤
    df['arh'] = ta.WMA(df['high'], timeperiod=a) - ta.WMA(df['open'], timeperiod=a)
    df['arl'] = ta.WMA(df['open'], timeperiod=a) - ta.WMA(df['low'], timeperiod=a)
    df['ar'] = df['arh'] / df['arl']
    df['guolv_duo'] = df['ar'] > 0.5
    df['guolv_kong'] = df['ar'] < 0.3
    df['cha'] = abs(df['close'] - df['median'])
    # 计算平均差
    df['ping_jun_cha'] = df['cha'].rolling(n, min_periods=1).mean()
    # 计算上轨、下轨道
    df['upper'] = df['median'] + m * df['ping_jun_cha']
    df['lower'] = df['median'] - m * df['ping_jun_cha']
    # ===计算信号
    # 找出做多信号
    condition1 = df['close'] > df['upper']  # 当前K线的收盘价 > 上轨
    condition2 = df['close'].shift(1) <= df['upper'].shift(1)  # 之前K线的收盘价 <= 上轨
    condition3 = df['pc'] > df['median']
    df.loc[condition1 & condition2 & condition3 & df['guolv_duo'], 'signal_long'] = 1  # 将产生做多信号的那根K线的signal设置为1，1代表做多

    # 找出做多平仓信号
    condition1 = df['pc'] < df['median']  # 当前K线的收盘价 < 中轨
    condition2 = df['pc'].shift(1) >= df['median'].shift(1)  # 之前K线的收盘价 >= 中轨
    df.loc[condition1 & condition2, 'signal_long'] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓

    # 找出做空信号
    condition1 = df['close'] < df['lower']  # 当前K线的收盘价 < 下轨
    condition2 = df['close'].shift(1) >= df['lower'].shift(1)  # 之前K线的收盘价 >= 下轨
    condition3 = df['pc'] < df['median']
    df.loc[
        condition1 & condition2 & condition3 & df['guolv_kong'], 'signal_short'] = -1  # 将产生做空信号的那根K线的signal设置为-1，-1代表做空

    # 找出做空平仓信号
    condition1 = df['pc'] > df['median']  # 当前K线的收盘价 > 中轨
    condition2 = df['pc'].shift(1) <= df['median'].shift(1)  # 之前K线的收盘价 <= 中轨
    df.loc[condition1 & condition2, 'signal_short'] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓

    # 合并做多做空信号，去除重复信号
    df['signal'] = df[['signal_long', 'signal_short']].sum(axis=1, min_count=1,
                                                           skipna=True)  # 若你的pandas版本是最新的，请使用本行代码代替上面一行
    temp = df[df['signal'].notnull()][['signal']]
    temp = temp[temp['signal'] != temp['signal'].shift(1)]
    df['signal'] = temp['signal']

    # ===删除无关变量
    # df.drop(['median', 'std', 'upper', 'lower', 'signal_long', 'signal_short'], axis=1, inplace=True)
    df.drop(['signal_long', 'signal_short'], axis=1, inplace=True)

    return df.iloc[-1]['signal']


def real_signal_simple_bolling_ee(df, now_pos, avg_price, para=[200, 2]):
    """
    平均差布林+均线回归W+PC平仓+AR过滤
    """
    # ===策略参数
    n = int(para[0])
    m = para[1]
    # 固定参数
    a = 13
    # ===计算指标
    # 计算均线
    df['median'] = ta.LINEARREG(df['close'], timeperiod=a)
    df['median'] = ta.EMA(df['median'], timeperiod=n)
    # 平仓均线
    df['pc'] = ta.TEMA(df['close'], timeperiod=13)
    # ar过滤
    df['arh'] = ta.EMA(df['high'], timeperiod=a) - ta.EMA(df['open'], timeperiod=a)
    df['arl'] = ta.EMA(df['open'], timeperiod=a) - ta.EMA(df['low'], timeperiod=a)
    df['ar'] = df['arh'] / df['arl']
    df['guolv_duo'] = df['ar'] > 0.5
    df['guolv_kong'] = df['ar'] < 0.3
    df['cha'] = abs(df['close'] - df['median'])
    # 计算平均差
    df['ping_jun_cha'] = df['cha'].rolling(n, min_periods=1).mean()
    # 计算上轨、下轨道
    df['upper'] = df['median'] + m * df['ping_jun_cha']
    df['lower'] = df['median'] - m * df['ping_jun_cha']
    # ===计算信号
    # 找出做多信号
    condition1 = df['close'] > df['upper']  # 当前K线的收盘价 > 上轨
    condition2 = df['close'].shift(1) <= df['upper'].shift(1)  # 之前K线的收盘价 <= 上轨
    condition3 = df['pc'] > df['median']
    df.loc[condition1 & condition2 & condition3 & df['guolv_duo'], 'signal_long'] = 1  # 将产生做多信号的那根K线的signal设置为1，1代表做多

    # 找出做多平仓信号
    condition1 = df['pc'] < df['median']  # 当前K线的收盘价 < 中轨
    condition2 = df['pc'].shift(1) >= df['median'].shift(1)  # 之前K线的收盘价 >= 中轨
    df.loc[condition1 & condition2, 'signal_long'] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓

    # 找出做空信号
    condition1 = df['close'] < df['lower']  # 当前K线的收盘价 < 下轨
    condition2 = df['close'].shift(1) >= df['lower'].shift(1)  # 之前K线的收盘价 >= 下轨
    condition3 = df['pc'] < df['median']
    df.loc[
        condition1 & condition2 & condition3 & df['guolv_kong'], 'signal_short'] = -1  # 将产生做空信号的那根K线的signal设置为-1，-1代表做空

    # 找出做空平仓信号
    condition1 = df['pc'] > df['median']  # 当前K线的收盘价 > 中轨
    condition2 = df['pc'].shift(1) <= df['median'].shift(1)  # 之前K线的收盘价 <= 中轨
    df.loc[condition1 & condition2, 'signal_short'] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓

    # 合并做多做空信号，去除重复信号
    df['signal'] = df[['signal_long', 'signal_short']].sum(axis=1, min_count=1,
                                                           skipna=True)  # 若你的pandas版本是最新的，请使用本行代码代替上面一行
    temp = df[df['signal'].notnull()][['signal']]
    temp = temp[temp['signal'] != temp['signal'].shift(1)]
    df['signal'] = temp['signal']

    # ===删除无关变量
    # df.drop(['median', 'std', 'upper', 'lower', 'signal_long', 'signal_short'], axis=1, inplace=True)
    df.drop(['signal_long', 'signal_short'], axis=1, inplace=True)

    return df.iloc[-1]['signal']


def real_signal_simple_bolling_we(df, now_pos, avg_price, para=[200, 2]):
    """
    real_signal_simple_bolling_we
    平均差布林+均线回归W+PC平仓+AR过滤
    """

    # ===策略参数
    n = int(para[0])
    m = para[1]
    # 固定参数
    a = 13
    # ===计算指标
    # 计算均线
    df['median'] = ta.LINEARREG(df['close'], timeperiod=a)
    df['median'] = ta.WMA(df['median'], timeperiod=n)
    # 平仓均线
    df['pc'] = ta.TEMA(df['close'], timeperiod=a)
    # ar过滤
    df['arh'] = ta.EMA(df['high'], timeperiod=a) - ta.EMA(df['open'], timeperiod=a)
    df['arl'] = ta.EMA(df['open'], timeperiod=a) - ta.EMA(df['low'], timeperiod=a)
    df['ar'] = df['arh'] / df['arl']
    df['guolv_duo'] = df['ar'] > 0.5
    df['guolv_kong'] = df['ar'] < 0.3
    df['cha'] = abs(df['close'] - df['median'])
    # 计算平均差
    df['ping_jun_cha'] = df['cha'].rolling(n, min_periods=1).mean()
    # 计算上轨、下轨道
    df['upper'] = df['median'] + m * df['ping_jun_cha']
    df['lower'] = df['median'] - m * df['ping_jun_cha']
    # ===计算信号
    # 找出做多信号
    condition1 = df['close'] > df['upper']  # 当前K线的收盘价 > 上轨
    condition2 = df['close'].shift(1) <= df['upper'].shift(1)  # 之前K线的收盘价 <= 上轨
    condition3 = df['pc'] > df['median']
    df.loc[condition1 & condition2 & condition3 & df['guolv_duo'], 'signal_long'] = 1  # 将产生做多信号的那根K线的signal设置为1，1代表做多

    # 找出做多平仓信号
    condition1 = df['pc'] < df['median']  # 当前K线的收盘价 < 中轨
    condition2 = df['pc'].shift(1) >= df['median'].shift(1)  # 之前K线的收盘价 >= 中轨
    df.loc[condition1 & condition2, 'signal_long'] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓

    # 找出做空信号
    condition1 = df['close'] < df['lower']  # 当前K线的收盘价 < 下轨
    condition2 = df['close'].shift(1) >= df['lower'].shift(1)  # 之前K线的收盘价 >= 下轨
    condition3 = df['pc'] < df['median']
    df.loc[
        condition1 & condition2 & condition3 & df['guolv_kong'], 'signal_short'] = -1  # 将产生做空信号的那根K线的signal设置为-1，-1代表做空

    # 找出做空平仓信号
    condition1 = df['pc'] > df['median']  # 当前K线的收盘价 > 中轨
    condition2 = df['pc'].shift(1) <= df['median'].shift(1)  # 之前K线的收盘价 <= 中轨
    df.loc[condition1 & condition2, 'signal_short'] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓

    # 合并做多做空信号，去除重复信号
    df['signal'] = df[['signal_long', 'signal_short']].sum(axis=1, min_count=1,
                                                           skipna=True)  # 若你的pandas版本是最新的，请使用本行代码代替上面一行
    temp = df[df['signal'].notnull()][['signal']]
    temp = temp[temp['signal'] != temp['signal'].shift(1)]
    df['signal'] = temp['signal']

    # ===删除无关变量
    # df.drop(['median', 'std', 'upper', 'lower', 'signal_long', 'signal_short'], axis=1, inplace=True)
    df.drop(['signal_long', 'signal_short'], axis=1, inplace=True)

    return df.iloc[-1]['signal']


def real_signal_simple_bolling_jxk_lize(df, now_pos, avg_price, para=[200, 2]):
    """
    李泽
    布林有一个指标叫极限宽指标,实际就是衡量邢大提到的布林开口大小的指标,听说越简单的策略越有效,试了一下效果还不错。
    加我的策略中轨平均差pc平仓
    # 布林线极限宽度：(上轨 - 下轨) / 均价e
    # 当收盘价由下向上穿过上轨且极限宽度小于0.1的时候，做多；然后由上向下穿过中轨的时候，平仓。
    # 当收盘价由上向下穿过下轨且极限宽度小于0.1的时候，做空；然后由下向上穿过中轨的时候，平仓。
    """
    # ===策略参数
    n = int(para[0])
    m = para[1]
    # 固定参数
    a = 13

    # ===计算指标
    # 计算均线
    df['median'] = ta.LINEARREG(df['close'], timeperiod=a)
    df['median'] = ta.WMA(df['median'], timeperiod=n)
    df['cha'] = abs(df['close'] - df['median'])
    # 计算平均差
    df['ping_jun_cha'] = df['cha'].rolling(n, min_periods=1).mean()
    # 计算上轨、下轨道
    df['upper'] = df['median'] + m * df['ping_jun_cha']
    df['lower'] = df['median'] - m * df['ping_jun_cha']

    # 平仓均线
    df['pc'] = ta.TEMA(df['close'], timeperiod=a)
    # ar过滤
    df['arh'] = ta.EMA(df['high'], timeperiod=a) - ta.EMA(df['open'], timeperiod=a)
    df['arl'] = ta.EMA(df['open'], timeperiod=a) - ta.EMA(df['low'], timeperiod=a)
    df['ar'] = df['arh'] / df['arl']
    df['guolv_duo'] = df['ar'] > 0.5
    df['guolv_kong'] = df['ar'] < 0.3

    df['width'] = (df['upper'] - df['lower']) / df['median']  # 计算极限宽度指标
    # ===计算信号
    # 找出做多信号
    condition1 = df['close'] > df['upper']  # 当前K线的收盘价 > 上轨
    condition2 = df['close'].shift(1) <= df['upper'].shift(1)  # 之前K线的收盘价 <= 上轨
    condition3 = df['width'] <= 0.1  # 判断敞口大小
    condition4 = df['pc'] > df['median']
    df.loc[condition1 & condition2 & condition3 & condition4, 'signal_long'] = 1  # 将产生做多信号的那根K线的signal设置为1，1代表做多

    # 找出做多平仓信号
    condition1 = df['pc'] < df['median']  # 当前K线的收盘价 < 中轨
    condition2 = df['pc'].shift(1) >= df['median'].shift(1)  # 之前K线的收盘价 >= 中轨
    df.loc[condition1 & condition2, 'signal_long'] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓

    # 找出做空信号
    condition1 = df['close'] < df['lower']  # 当前K线的收盘价 < 下轨
    condition2 = df['close'].shift(1) >= df['lower'].shift(1)  # 之前K线的收盘价 >= 下轨
    condition3 = df['width'] <= 0.1
    condition4 = df['pc'] < df['median']
    df.loc[condition1 & condition2 & condition3 & condition4, 'signal_short'] = -1  # 将产生做空信号的那根K线的signal设置为-1，-1代表做空

    # 找出做空平仓信号
    condition1 = df['pc'] > df['median']  # 当前K线的收盘价 > 中轨
    condition2 = df['pc'].shift(1) <= df['median'].shift(1)  # 之前K线的收盘价 <= 中轨
    df.loc[condition1 & condition2, 'signal_short'] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓

    # 合并做多做空信号，去除重复信号
    df['signal'] = df[['signal_long', 'signal_short']].sum(axis=1, min_count=1,
                                                           skipna=True)  # 若你的pandas版本是最新的，请使用本行代码代替上面一行
    temp = df[df['signal'].notnull()][['signal']]
    temp = temp[temp['signal'] != temp['signal'].shift(1)]
    df['signal'] = temp['signal']

    # ===删除无关变量
    # df.drop(['median', 'std', 'upper', 'lower', 'signal_long', 'signal_short'], axis=1, inplace=True)
    df.drop(['signal_long', 'signal_short'], axis=1, inplace=True)

    return df.iloc[-1]['signal']


def real_signal_simple_bolling_sbias_zhangyao(df, now_pos, avg_price, para=[200, 2, 0.05]):
    """
    张尧
    该策略魔改传统布林带策略的开仓点和平仓位置两个方面：
    1、将开仓价格控制在一定数值范围内；
    2、将传统穿越布林带中轨平仓改变为：多仓在上轨从上升变为下降的时刻平仓，空仓在下轨从下降变为上升的时刻平仓
    3、加我的策略中轨平均差pc平仓
    针对原始布林策略进行修改。
    bias = close / 均线 - 1
    当开仓的时候，如果bias过大，即价格离均线过远，那么就不开仓。
    :param df:
    :param para: n,m,bias_pct
    :return:
    """
    # ===策略参数
    n = int(para[0])
    m = float(para[1])
    bias_pct = float(para[2])
    # 固定参数
    a = 13

    # ===计算指标
    # 计算均线
    df['median'] = ta.LINEARREG(df['close'], timeperiod=13)
    df['median'] = ta.WMA(df['median'], timeperiod=n)
    # 计算每根k线收盘价和均线的差值，取绝对数
    df['cha'] = abs(df['close'] - df['median'])
    # 计算平均差
    df['ping_jun_cha'] = df['cha'].rolling(n, min_periods=1).mean()
    # 计算上轨、下轨道
    df['upper'] = df['median'] + m * df['ping_jun_cha']
    df['lower'] = df['median'] - m * df['ping_jun_cha']

    # 平仓均线
    df['pc'] = ta.TEMA(df['close'], timeperiod=a)

    # 计算bias
    df['bias'] = abs(df['close'] / df['median'] - 1)

    # ===计算原始布林策略信号
    # 找出做多信号
    condition1 = df['close'] > df['upper']  # 当前K线的收盘价 > 上轨
    condition2 = df['close'].shift(1) <= df['upper'].shift(1)  # 之前K线的收盘价 <= 上轨
    condition3 = df['bias'] < bias_pct  # 开仓价格 < 设定范围
    condition4 = df['pc'] > df['median']
    df.loc[condition1 & condition2 & condition3 & condition4, 'signal_long'] = 1  # 将产生做多信号的那根K线的signal设置为1，1代表做多

    # 找出做多平仓信号
    condition1 = df['pc'] < df['median']  # 当前K线的收盘价 < 中轨
    condition2 = df['pc'].shift(1) >= df['median'].shift(1)  # 之前K线的收盘价 >= 中轨
    condition3 = df['upper'] < df['upper'].shift(1)  # 当布林带上轨由上涨转为下降时触发
    condition4 = df['close'] > df['median']  # 当前K线的收盘价 > 中轨
    df.loc[(condition1 & condition2) | (condition3 & condition4), 'signal_long'] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓

    # 找出做空信号
    condition1 = df['close'] < df['lower']  # 当前K线的收盘价 < 下轨
    condition2 = df['close'].shift(1) >= df['lower'].shift(1)  # 之前K线的收盘价 >= 下轨
    condition3 = df['bias'] < bias_pct  # 开仓价格 < 设定范围
    condition4 = df['pc'] < df['median']
    df.loc[condition1 & condition2 & condition3 & condition4, 'signal_short'] = -1  # 将产生做空信号的那根K线的signal设置为-1，-1代表做空

    # 找出做空平仓信号
    condition1 = df['pc'] > df['median']  # 当前K线的收盘价 > 中轨
    condition2 = df['pc'].shift(1) <= df['median'].shift(1)  # 之前K线的收盘价 <= 中轨
    condition3 = df['lower'] > df['lower'].shift(1)  # 当布林带下轨由下降转为上涨时触发
    condition4 = df['close'] < df['median']  # 当前K线的收盘价 < 中轨
    df.loc[(condition1 & condition2) | (condition3 & condition4), 'signal_short'] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓

    # ===将long和short合并为signal
    df['signal_short'].fillna(method='ffill', inplace=True)
    df['signal_long'].fillna(method='ffill', inplace=True)
    df['signal'] = df[['signal_long', 'signal_short']].sum(axis=1)
    df['signal'].fillna(value=0, inplace=True)
    df['raw_signal'] = df['signal']

    # ===将signal中的重复值删除
    temp = df[['signal']]
    temp = temp[temp['signal'] != temp['signal'].shift(1)]
    df['signal'] = temp

    df.drop(['raw_signal', 'bias', 'signal_long', 'signal_short'], axis=1,
            inplace=True)  # 'upper', 'lower',  'median','std',

    return df.iloc[-1]['signal']


def real_signal_simple_bolling_pjc_sbias(df, now_pos, avg_price, para=[200, 2, 0.1, 0.5]):
    """李冰的平均值上下轨+骁川双BIAS限流+我的策略"""

    n = int(para[0])
    m = para[1]
    bias = para[2]  # 止盈比例
    bias_pct = para[3]  # 限制开仓比例
    # 固定参数
    a = 13

    # ===计算指标
    # 计算均线
    df['median'] = ta.LINEARREG(df['close'], timeperiod=a)
    df['median'] = ta.WMA(df['median'], timeperiod=n)
    # 平仓均线
    df['pc'] = ta.TEMA(df['close'], timeperiod=a)
    # ar过滤
    df['arh'] = ta.EMA(df['high'], timeperiod=a) - ta.EMA(df['open'], timeperiod=a)
    df['arl'] = ta.EMA(df['open'], timeperiod=a) - ta.EMA(df['low'], timeperiod=a)
    df['ar'] = df['arh'] / df['arl']
    df['guolv_duo'] = df['ar'] > 0.5
    df['guolv_kong'] = df['ar'] < 0.3
    # 计算上轨、下轨道
    df['cha'] = abs(df['close'] - df['median'])
    # 计算平均差
    df['ping_jun_cha'] = df['cha'].rolling(n, min_periods=1).mean()
    # 计算上轨、下轨道
    df['upper'] = df['median'] + m * df['ping_jun_cha']
    df['lower'] = df['median'] - m * df['ping_jun_cha']
    # 计算bias通道
    df['bias'] = abs(df['close'] / df['median'] - 1)  # 设置bisa值
    # ===计算布林策略信号

    condition1 = df['close'] > df['upper']  # 当前K线的收盘价 > 上轨
    condition2 = df['close'].shift(1) <= df['upper'].shift(1)  # 之前K线的收盘价 <= 上轨
    condition3 = df['pc'] > df['median']
    df.loc[condition1 & condition2 & condition3 & df['guolv_duo'], 'signal_long'] = 1  # 将产生做多信号的那根K线的signal设置为1，1代表做多

    # 找出做多平仓信号
    condition1 = df['pc'] < df['median']  # 当前K线的收盘价 < 中轨
    condition2 = df['pc'].shift(1) >= df['median'].shift(1)  # 之前K线的收盘价 >= 中轨
    condition3 = df['bias'] >= bias
    df.loc[(condition1 & condition2) | condition3, 'signal_long'] = 0

    # 找出做空信号
    condition1 = df['close'] < df['lower']  # 当前K线的收盘价 < 下轨
    condition2 = df['close'].shift(1) >= df['lower'].shift(1)  # 之前K线的收盘价 >= 下轨
    condition3 = df['pc'] < df['median']
    df.loc[condition1 & condition2 & condition3 & df['guolv_kong'], 'signal_short'] = -1

    # 找出做空平仓信号
    condition1 = df['pc'] > df['median']  # 当前K线的收盘价 > 中轨
    condition2 = df['pc'].shift(1) <= df['median'].shift(1)  # 之前K线的收盘价 <= 中轨
    condition3 = df['bias'] >= bias
    df.loc[(condition1 & condition2) | condition3, 'signal_short'] = 0

    # ===将long和short合并为signal
    df['signal'] = df[['signal_long', 'signal_short']].sum(axis=1, min_count=1, skipna=True)
    temp = df[df['signal'].notnull()][['signal']]
    temp = temp[temp['signal'] != temp['signal'].shift(1)]
    df['signal'] = temp['signal']
    df['signal'].fillna(method='ffill', inplace=True)
    df.drop(['signal_long', 'signal_short'], axis=1, inplace=True)

    # ===根据bias，修改开仓时间
    df['temp'] = df['signal']

    # 将原始信号持仓中 bias大于阀值，设置为空
    condition1 = (df['signal'] != 0)
    condition2 = (df['bias'] > bias_pct)
    df.loc[condition1 & condition2, 'temp'] = None

    # 原始信号刚开仓，并且大于阀值，将信号设置为0
    condition1 = (df['signal'] != df['signal'].shift(1))
    condition2 = (df['temp'].isnull())
    df.loc[condition1 & condition2, 'temp'] = 0

    df['temp'].fillna(method='ffill', inplace=True)
    df['signal'] = df['temp']

    # ===将signal中的重复值删除(提取关键点)
    temp = df[['signal']]
    temp = temp[temp['signal'] != temp['signal'].shift(1)]
    df['signal'] = temp
    df.drop(['bias', 'temp', ], axis=1, inplace=True)  # 'std',

    return df.iloc[-1]['signal']
