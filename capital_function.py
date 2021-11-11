import time
import pandas as pd
from capital_allocate.capital_config import *
from datetime import datetime, timedelta
import numpy as np
import json
import requests
import hmac
import hashlib
import base64
from urllib import parse

# ===通过ccxt、交易所接口获取单个交割合约账户持仓信息
def fetch_single_futures_position(exchange, instrument_id, max_try_amount=5):
    """
    :param instrument_id:
    :param exchange:
    :param max_try_amount:
    :return:
     """
    for _ in range(max_try_amount):
        try:
            # 获取数据
            position_info = exchange.futures_get_instrument_id_position({'instrument_id': instrument_id})
            return position_info
        except Exception as e:
            print('通过ccxt的通过futures_get_position获取所有合约的持仓信息，失败，稍后重试。失败原因：\n', e)
            # time.sleep(medium_sleep_time)

    _ = '通过ccxt的通过futures_get_position获取所有合约的持仓信息，失败次数过多，程序Raise Error'
    # send_dingding_and_raise_error(_)


# ===通过ccxt、交易所接口获取单个永续合约账户持仓信息
def fetch_single_swap_position(exchange, instrument_id, max_try_amount=5):
    """
    :param instrument_id:
    :param exchange:
    :param max_try_amount:
    :return:
     """
    for _ in range(max_try_amount):
        try:
            # 获取数据
            position_info = exchange.swap_get_instrument_id_position({'instrument_id': instrument_id})
            return position_info
        except Exception as e:
            print('通过ccxt的通过futures_get_position获取所有合约的持仓信息，失败，稍后重试。失败原因：\n', e)
            # time.sleep(medium_sleep_time)

    _ = '通过ccxt的通过futures_get_position获取所有合约的持仓信息，失败次数过多，程序Raise Error'
    # send_dingding_and_raise_error(_)


# ===通过ccxt、交易所接口获取单个交割合约账户持仓信息
def fetch_futures_position(exchange, max_try_amount=5):
    """
    :param exchange:
    :param max_try_amount:
    :return:
     """
    for _ in range(max_try_amount):
        try:
            # 获取数据
            position_info = exchange.futures_get_position()
            return position_info
        except Exception as e:
            print('通过ccxt的通过futures_get_position获取所有合约的持仓信息，失败，稍后重试。失败原因：\n', e)
            # time.sleep(medium_sleep_time)

    _ = '通过ccxt的通过futures_get_position获取所有合约的持仓信息，失败次数过多，程序Raise Error'
    # send_dingding_and_raise_error(_)


# ===通过ccxt、交易所接口获取单个永续合约账户持仓信息
def fetch_swap_position(exchange, max_try_amount=5):
    """
    :param exchange:
    :param max_try_amount:
    :return:
     """
    for _ in range(max_try_amount):
        try:
            # 获取数据
            position_info = exchange.swap_get_position()
            return position_info
        except Exception as e:
            print('通过ccxt的通过futures_get_position获取所有合约的持仓信息，失败，稍后重试。失败原因：\n', e)
            # time.sleep(medium_sleep_time)

    _ = '通过ccxt的通过futures_get_position获取所有合约的持仓信息，失败次数过多，程序Raise Error'
    # send_dingding_and_raise_error(_)


# 获取单个合约信息
def fetch_single_futures_account(exchange, underlying, max_try_amount=5):
    '''
    :param exchange: ccxt创建的交易所对象
    :param underlying: 合约交易对，比如：btc-usdt
    :param max_try_amount: 报错之后，最大重试次数
    :return:
    '''
    for _ in range(max_try_amount):
        try:
            future_info = exchange.futures_get_accounts_underlying({'underlying': underlying})
            return future_info
        except Exception as e:
            print('通过ccxt的通过futures_get_accounts获取单个合约账户信息，失败，稍后重试：\n', e)
            time.sleep(1)

    _ = '通过ccxt的通过futures_get_accounts_underlying获取单个合约账户信息，失败次数过多'
    print(_)


# 获取币币账户所有币种余额信息
def fetch_spot_accounts(exchange, max_try_amount=5):
    '''
    :param exchange: ccxt创建的交易所对象
    :param max_try_amount: 报错之后，最大重试次数
    :return:
    '''
    for _ in range(max_try_amount):
        try:
            spot_info = exchange.spot_get_accounts()
            return spot_info
        except Exception as e:
            print('通过ccxt的通过spot_get_accounts获取币币账户所有币种余额信息，失败，稍后重试：\n', e)
            time.sleep(1)

    _ = '通过ccxt的通过spot_get_accounts获取币币账户所有币种余额信息，失败次数过多'
    print(_)


# 获取永续账户所有币种余额信息
def fetch_swap_accounts(exchange, max_try_amount=5):
    '''
    :param exchange: ccxt创建的交易所对象
    :param max_try_amount: 报错之后，最大重试次数
    :return:
    '''
    for _ in range(max_try_amount):
        try:
            swap_info = exchange.swap_get_accounts()
            return swap_info
        except Exception as e:
            print('通过ccxt的通过swap_get_accounts获取币币账户所有币种余额信息，失败，稍后重试：\n', e)
            time.sleep(1)

    _ = '通过ccxt的通过swap_get_accounts获取币币账户所有币种余额信息，失败次数过多'
    print(_)


# 获取多个合约信息
def fetch_futures_accounts(exchange, max_try_amount=5):
    '''
    :param exchange: ccxt创建的交易所对象
    :param max_try_amount: 报错之后，最大重试次数
    :return:
    '''
    for _ in range(max_try_amount):
        try:
            future_info = exchange.futures_get_accounts()
            return future_info
        except Exception as e:
            print('通过ccxt的通过futures_get_accounts获取单个合约账户信息，失败，稍后重试：\n', e)
            time.sleep(1)

    _ = '通过ccxt的通过futures_get_accounts_underlying获取单个合约账户信息，失败次数过多'
    print(_)


# 获取币币账户中指定币种的余额信息
def fetch_single_spot_account(exchange, currency, max_try_amount=5):
    '''
    :param exchange: ccxt创建的交易所对象
    :param currency: 需要获取币币账户中余额信息的币种，比如：btc
    :param max_try_amount: 报错之后，最大重试次数
    :return:
    '''
    for _ in range(max_try_amount):
        try:
            spot_info = exchange.spot_get_accounts_currency({
                'currency': currency
            })
            return spot_info
        except Exception as e:
            print('通过ccxt的通过spot_get_accounts_currency获取币币账户指定币种余额信息，失败，稍后重试：\n', e)
            time.sleep(1)

    _ = '通过ccxt的通过spot_get_accounts_currency获取币币账户指定币种余额信息，失败次数过多'
    print(_)


# 获取子账户余额信息
def fetch_sub_account_info(exchange, sub_account_name, max_try_amount=5):
    '''
    :param exchange: ccxt创建的交易所对象
    :param sub_account_name: 子账户名
    :param max_try_amount: 报错之后，最大重试次数
    :return:
    '''
    for _ in range(max_try_amount):
        try:
            sub_account_info = exchange.account_get_sub_account({
                'sub-account': sub_account_name
            })
            return sub_account_info
        except Exception as e:
            print('通过ccxt的account_get_sub_account获取子账户信息失败，稍后重试：\n', e)
            time.sleep(1)

    _ = '通过ccxt的account_get_sub_account获取子账户信息失败次数过多'
    print(_)


# 获取子账户所有账户余额信息
def fetch_all_account_info(exchange, sub_account_name):
    '''
    :param exchange: ccxt创建的交易所对象
    :param sub_account_name: 子账户名
    :return:
    '''

    wallet = fetch_wallet_account(exchange)
    spot = fetch_spot_accounts(exchange)
    futures = fetch_futures_accounts(exchange)
    swap = fetch_swap_accounts(exchange)
    df_spot = pd.DataFrame(spot)
    if df_spot.empty:
        df_spot = pd.DataFrame(columns=['equity', 'max_withdraw', 'underlying', 'account_type', 'currency'])
    df_spot.rename(columns={'balance': 'equity', 'available': 'max_withdraw'}, inplace=True)
    df_spot['underlying'] = ''
    df_spot['account_type'] = 'spot'
    df_wallet = pd.DataFrame(wallet)
    if df_wallet.empty:
        df_wallet = pd.DataFrame(columns=['equity', 'max_withdraw', 'underlying', 'account_type', 'currency'])
    df_wallet.rename(columns={'balance': 'equity', 'available': 'max_withdraw'}, inplace=True)
    df_wallet['underlying'] = ''
    df_wallet['account_type'] = 'funding'
    df_futures = pd.DataFrame(futures['info']).T.reset_index()
    df_futures.rename(columns={'underlying': 'symbol', 'index': 'underlying', 'can_withdraw': 'max_withdraw'},
                      inplace=True)
    if df_futures.empty:
        df_futures = pd.DataFrame(columns=['equity', 'max_withdraw', 'underlying', 'account_type', 'currency'])
    df_futures['underlying'] = df_futures['underlying'].str.upper()
    df_futures['account_type'] = 'futures'
    df_swap = pd.DataFrame(swap['info'])
    if df_swap.empty:
        df_swap = pd.DataFrame(columns=['equity', 'max_withdraw', 'underlying', 'account_type', 'currency'])
    df_swap['account_type'] = 'swap'
    df_swap.rename(columns={'index': 'underlying', 'can_withdraw': 'max_withdraw'}, inplace=True)
    df_accounts_info = pd.concat([df_wallet, df_spot, df_futures, df_swap], join='inner')
    df_accounts_info['account_name'] = sub_account_name
    df_accounts_info['max_withdraw'] = df_accounts_info['max_withdraw'].astype(float)
    df_accounts_info['equity'] = df_accounts_info['equity'].astype(float)
    df_accounts_info = df_accounts_info.loc[df_accounts_info['equity'] > 0.00000001]
    return df_accounts_info


# 获取资金余额信息
def fetch_wallet_account(exchange, max_try_amount=5):
    '''
    :param exchange: ccxt创建的交易所对象
    :param max_try_amount: 报错之后，最大重试次数
    :return:
    '''
    for _ in range(max_try_amount):
        try:
            sub_account_info = exchange.account_get_wallet()
            return sub_account_info
        except Exception as e:
            print('通过ccxt的account_get_wallet获取子账户信息失败，稍后重试：\n', e)
            time.sleep(1)

    _ = '通过ccxt的account_get_wallet获取子账户信息失败次数过多'
    print(_)


# 用于把OKex返回的子账户信息整理为DataFrame，便于后续计算
def convert_accounts(accounts):
    df_list = []
    for account_name in accounts.keys():
        _df = accounts[account_name]
        df_list.append(_df)
    return pd.concat(df_list, sort=True)


# okex各个账户间转钱
def okex_account_transfer(exchange, params, tips='', max_try_amount=5):
    # 开始转账
    for i in range(max_try_amount):
        try:
            transfer_info = exchange.account_post_transfer(params=params)
            if transfer_info['result'] is True:
                print('【' + tips + '】划转成功，detail：', transfer_info, '\n')
            else:
                print('【' + tips + '】划转失败，detail：', transfer_info, '\n')
            # 避免多次转账间隔太短，接口报错
            time.sleep(1)
            return transfer_info

        except Exception as e:
            print('【' + tips + '】划转报错，1s后重试', e)
            time.sleep(1)
    print('划转报错次数过多，停止划转，程序继续')


# 按照子账户资金分配计划，进行资金划转
def allocate_accounts(exchange_main, sub_accounts, plan_sub_accounts, skip_on_position=True, decimal_precision=4):
    plan_sub_accounts.set_index(['account_name', 'account_type', 'underlying', 'currency'], inplace=True)
    sub_accounts.set_index(['account_name', 'account_type', 'underlying', 'currency'], inplace=True)

    plan_sub_accounts['max_withdraw'] = sub_accounts['max_withdraw']
    plan_sub_accounts['plan_allocate'] = plan_sub_accounts['plan_available'] - plan_sub_accounts['max_withdraw']
    plan_sub_accounts.sort_values('plan_allocate', inplace=True)
    plan_sub_accounts['plan_allocate'] = plan_sub_accounts['plan_allocate'].apply(lambda x: int(x * (10 ** decimal_precision)) / (10 ** decimal_precision))

    plan_sub_accounts.reset_index(inplace=True, drop=False)

    for row in plan_sub_accounts.iterrows():
        params = {}
        tips = ''
        if skip_on_position:
            if row[1]['position'] > 0:
                print(
                    '%s[%s-%s]账户有持仓，暂不参与资金划转' % (row[1]['account_name'], row[1]['account_type'], row[1]['underlying']))
                continue
        if row[1]['plan_allocate'] < 0:
            params = {'currency': row[1]['currency'],
                      'amount': str(-row[1]['plan_allocate']),
                      'type': '2',
                      'from': account_type_contrast[row[1]['account_type']],
                      'to': '6',
                      'sub_account': row[1]['account_name'],
                      'instrument_id': row[1]['underlying'],
                      # 'to_instrument_id': 'btc-usdt'
                      }
            tips = '%s[%s-%s] to 母账户[funding]' % (
                row[1]['account_name'], row[1]['account_type'], params['instrument_id'])
        elif row[1]['plan_allocate'] > 0:
            params = {'currency': row[1]['currency'],
                      'amount': str(row[1]['plan_allocate']),
                      'type': '1',
                      'from': '6',
                      'to': account_type_contrast[row[1]['account_type']],
                      'sub_account': row[1]['account_name'],
                      # 'instrument_id': row[1]['underlying'],
                      'to_instrument_id': row[1]['underlying']
                      }
            tips = '母账户[funding] to %s[%s-%s]' % (
                row[1]['account_name'], row[1]['account_type'], params['to_instrument_id'])

        if params:
            okex_account_transfer(exchange_main, params, tips)


# ===依据时间间隔, 自动计算并休眠到指定时间
def sleep_until_run_time(time_interval, offset_minutes=0, ahead_time=5, if_sleep=True):
    '''
    根据next_run_time()函数计算出下次程序运行的时候，然后sleep至该时间
    :param offset_minutes:
    :param if_sleep:
    :param time_interval:
    :param ahead_time:
    :return:
    '''
    # 计算下次运行时间
    run_time = next_run_time(time_interval, offset_minutes, ahead_time)

    if if_sleep:
        # sleep
        time.sleep(max(0, (run_time - datetime.now()).seconds))
        while True:  # 在靠近目标时间时
            if datetime.now() > run_time:
                break

        return run_time
    else:
        return run_time


# ===下次运行时间，和课程里面讲的函数是一样的
def next_run_time(time_interval, offset_minutes=0, ahead_seconds=5):
    '''
    根据time_interval，计算下次运行的时间，下一个整点时刻。
    目前只支持分钟和小时。
    :param offset_minutes: 相对于整点，偏离的分钟数，正整数或负整数均可
    :param time_interval: 运行的周期，15m，1h
    :param ahead_seconds: 预留的目标时间和当前时间的间隙
    :return: 下次运行的时间
    '''
    if time_interval.endswith('m') or time_interval.endswith('h'):
        pass
    elif time_interval.endswith('T'):
        time_interval = time_interval.replace('T', 'm')
    elif time_interval.endswith('H'):
        time_interval = time_interval.replace('H', 'h')
    else:
        print('time_interval格式不符合规范。程序exit')
        exit()

    ti = pd.to_timedelta(time_interval)
    now_time = datetime.now()
    # now_time = datetime(2019, 5, 9, 23, 50, 30)  # 修改now_time，可用于测试
    this_midnight = now_time.replace(hour=0, minute=0, second=0, microsecond=0)
    min_step = timedelta(minutes=1)

    target_time = now_time.replace(second=0, microsecond=0)

    while True:
        target_time = target_time + min_step
        delta = target_time - this_midnight
        if (delta.seconds - timedelta(minutes=offset_minutes).seconds) % ti.seconds == 0 and (
                target_time - now_time).seconds >= ahead_seconds:
            # 当符合运行周期，并且目标时间有足够大的余地，默认为60s
            break

    print('\n', '程序下次运行的时间：', target_time)

    return target_time


# 获取策略涉及的交易对
def get_symbol_list(allocate_type, sub_account_name, market, symbol_list):
    for underlying in eval(allocate_type).symbol_config_dict[sub_account_name]['symbol_config'].keys():
        instrument_id = eval(allocate_type).symbol_config_dict[sub_account_name]['symbol_config'][underlying]['instrument_id']
        for position_account in ['futures', 'swap', 'spot']:
            if market.loc[market['id'].isin([instrument_id]), position_account][0]:
                symbol = {'account_name': sub_account_name, 'account_type': position_account,
                          'underlying': underlying.upper(), 'currency': underlying.upper().split('-')[1],
                          'is_run': True, 'allocate_type': allocate_type
                          }
                symbol = pd.DataFrame([symbol])
                symbol_list.append(symbol)


# 获取持仓信息
def get_position_list(exchange, sub_account_name, futures_list, swap_list, spot_list):
    position_info = fetch_futures_position(exchange)
    if position_info['holding']:
        df_position_info = pd.DataFrame(position_info['holding'][0])
        df_position_info['underlying'] = df_position_info['instrument_id'].apply(lambda x:x.split('-')[0] + '-' + x.split('-')[1])
        df_position_info['account_name'] = sub_account_name
        df_position_info['account_type'] = 'futures'
        futures_list.append(df_position_info)

    position_info = fetch_swap_position(exchange)
    info_list = []
    for info in position_info:
        if info['holding']:
            df_position_info = pd.DataFrame(info['holding'])
            info_list.append(df_position_info)
    if info_list:
        df_info = pd.concat(info_list)
        df_info['underlying'] = df_info['instrument_id'].apply(lambda x:x.split('-')[0] + '-' + x.split('-')[1])
        df_info['account_name'] = sub_account_name
        df_info['account_type'] = 'swap'
        swap_list.append(df_info)


# 整理持仓信息
def concat_position(futures_list, swap_list, spot_list):
    df_futures_position = pd.DataFrame()
    if futures_list:
        df_futures_position = pd.concat(futures_list)
        df_futures_position['underlying'] = df_futures_position['underlying'].str.upper()
        df_futures_position['position'] = df_futures_position['long_qty'].astype(float) + df_futures_position[
            'short_qty'].astype(float)
        df_futures_position = pd.pivot_table(df_futures_position, values='position',
                                             index=['account_name', 'account_type', 'underlying'],
                                             aggfunc=np.sum).reset_index()

    df_swap_position = pd.DataFrame()
    if swap_list:
        df_swap_position = pd.concat(swap_list)
        df_swap_position['underlying'] = df_swap_position['underlying'].str.upper()
        df_swap_position['position'] = df_swap_position['position'].astype(float)
        df_swap_position = pd.pivot_table(df_swap_position, values='position',
                                          index=['account_name', 'account_type', 'underlying'],
                                          aggfunc=np.sum).reset_index()
    df_position = pd.concat([df_futures_position, df_swap_position])
    return df_position


# 发送钉钉消息
def send_dingding_msg(content, robot_id=robot_id, secret=secret):
    """
    :param content:
    :param robot_id:  你的access_token，即webhook地址中那段access_token。例如如下地址：https://oapi.dingtalk.com/robot/
n    :param secret: 你的secret，即安全设置加签当中的那个密钥
    :return:
    """
    try:
        msg = {
            "msgtype": "text",
            "text": {"content": content + '\n' + datetime.now().strftime("%m-%d %H:%M:%S")}}
        headers = {"Content-Type": "application/json;charset=utf-8"}
        # https://oapi.dingtalk.com/robot/send?access_token=XXXXXX&timestamp=XXX&sign=XXX
        timestamp, sign_str = cal_timestamp_sign(secret)
        url = 'https://oapi.dingtalk.com/robot/send?access_token=' + robot_id + \
              '&timestamp=' + timestamp + '&sign=' + sign_str
        body = json.dumps(msg)
        requests.post(url, data=body, headers=headers, timeout=10)
        print('成功发送钉钉')
    except Exception as e:
        print("发送钉钉失败:", e)


# 计算钉钉时间戳
def cal_timestamp_sign(secret):
    # 根据钉钉开发文档，修改推送消息的安全设置https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq
    # 也就是根据这个方法，不只是要有robot_id，还要有secret
    # 当前时间戳，单位是毫秒，与请求调用时间误差不能超过1小时
    # python3用int取整
    timestamp = int(round(time.time() * 1000))
    # 密钥，机器人安全设置页面，加签一栏下面显示的SEC开头的字符串
    secret_enc = bytes(secret.encode('utf-8'))
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = bytes(string_to_sign.encode('utf-8'))
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    # 得到最终的签名值
    sign = parse.quote_plus(base64.b64encode(hmac_code))
    return str(timestamp), str(sign)


def send_dingding_and_raise_error(content):
    print(content)
    send_dingding_msg(content)
    raise ValueError(content)