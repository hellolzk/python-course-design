from typing import *

import pandas as pd
from tqdm import tqdm

irrelevant_column = [
    'product_code', 'area_code', 'category_code', 'sub_category_code',
    'price', 'week', 'is_weekday', 'period'
]


def group_product(data: pd.DataFrame, key) -> dict[Any, Any]:
    """
    将商品列表按指定key分组，每组生成一个DataFrame
    :param key: 分组key
    :param data: 商品表
    :return: 分组字典
    """
    product_group = {}
    product_group_index = data.groupby(key).indices

    for item in product_group_index.items():
        k = item[0]
        product_orders = pd.DataFrame(data.loc[item[1], :]).reset_index()
        product_group[k] = product_orders

    return product_group


def merge_product_date(product: pd.DataFrame) -> pd.DataFrame:
    temp_list = []
    # 将同一日期的记录合并为一条记录，记录中的requirement相加
    for date, frame in tqdm(product.groupby('order_date'), desc='merge date', colour='green'):
        row = frame.iloc[0, :]
        merge_product = {
            'order_date': date,
            'requirement': sum(frame['requirement']),
            'is_discount': row['is_discount'],
            'is_holiday': row['is_holiday'],
            'channel': row['channel']
        }
        temp_list.append(merge_product)
    return pd.DataFrame(temp_list)


def merge_product_season(product: pd.DataFrame) -> pd.DataFrame:
    temp_list = []
    for season, frame in tqdm(product.groupby('season'), desc='merge season', colour='green'):
        merge = {
            'season': season,
            'requirement': sum(frame['requirement']),
        }
        temp_list.append(merge)
    return pd.DataFrame(temp_list)
