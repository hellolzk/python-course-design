import matplotlib.pyplot as plt
import pandas as pd

import preprocess


def draw6_7(product_year_group) -> None:
    fig: plt.Figure = plt.figure(figsize=(22, 11), dpi=150)

    for fig_index, (year, product) in enumerate(product_year_group.items()):
        online: pd.DataFrame = product[0]
        offline: pd.DataFrame = product[1]

        # total
        online_x = online.index.to_list()
        online_y = online['requirement'].to_list()

        offline_x = offline.index.to_list()
        offline_y = offline['requirement'].to_list()

        # holiday
        is_holiday = online['is_holiday'] == 1
        online_holiday_x = online[is_holiday].index.to_list()
        online_holiday_y = online[is_holiday]['requirement'].to_list()

        is_holiday = offline['is_holiday'] == 1
        offline_holiday_x = offline[is_holiday].index.to_list()
        offline_holiday_y = offline[is_holiday]['requirement'].to_list()

        # discount
        is_discount = online['is_discount'] == 1
        online_discount_x = online[is_discount].index.to_list()
        online_discount_y = online[is_discount]['requirement'].to_list()

        is_discount = offline['is_discount'] == 1
        offline_discount_x = offline[is_discount].index.to_list()
        offline_discount_y = offline[is_discount]['requirement'].to_list()

        # draw
        ax = fig.add_subplot(2, 2, fig_index + 1)
        ax.set_xlabel('Date')
        ax.set_ylabel('Requirement')
        ax.set_title(f'{year} Requirements')
        ticks_data = online if len(online) > len(offline) else offline
        date_label = [ticks_data.loc[i, 'order_date'] for i in range(0, len(ticks_data), 20)]
        ax.set_xticks(range(0, len(ticks_data), 20))
        ax.set_xticklabels(date_label, rotation=45)

        # total
        ax.plot(online_x, online_y, label='online', color='royalblue', zorder=1)
        ax.plot(offline_x, offline_y, label='offline', color='darkorange', zorder=1)

        # holiday
        ax.scatter(online_holiday_x, online_holiday_y, label='online holiday', color='b', zorder=2)
        ax.scatter(offline_holiday_x, offline_holiday_y, label='offline holiday', color='r', zorder=2)

        # discount
        ax.scatter(online_discount_x, online_discount_y, label='online discount', color='darkblue', zorder=2,
                   marker='s')
        ax.scatter(offline_discount_x, offline_discount_y, label='offline discount', color='darkred', zorder=2,
                   marker='s')

        ax.legend(loc='upper right')

    plt.suptitle('Requirements influenced by holiday and discount')
    plt.tight_layout()
    plt.savefig('./temp/question6_7.png')
    plt.show()


def draw8(year_products) -> None:
    fig = plt.figure(figsize=(7, 10), dpi=150)
    for fig_index, (year, frame) in enumerate(year_products.items()):
        season = frame['season']
        requirement = frame['requirement']

        # draw
        season_label = ['Spring', 'Summer', 'Autumn', 'Winter']
        colors = ['yellowgreen', 'orangered', 'gold', 'dodgerblue']

        ax = fig.add_subplot(2, 2, fig_index + 1)
        ax.set_xlabel('Season')
        ax.set_ylabel('Requirement')
        ax.set_title(f'{year} Requirements')
        tick_label = [season_label[i - 1] for i in season]
        ax.set_xticks(range(len(season)))
        ax.set_xticklabels(tick_label)

        color = [colors[i - 1] for i in season]
        ax.bar(range(len(season)), requirement, color=color, width=0.6)

    plt.suptitle('Requirements influenced by season')
    plt.tight_layout()
    plt.savefig('./temp/question8.png')
    plt.show()


def preprocessing6_7(data: pd.DataFrame):
    """
    将数据按年份分类，对每年拆分为 online 和 offline 两类，合并相同日期的需求量
    :param data: 总订单表
    :return: 年份分组字典，每一年包含 online(0) 和 offline(1) 两组数据
    """

    # group by year
    year_products = preprocess.group_product(data, key='year')

    # group and merge
    for year, year_frame in list(year_products.items()):
        # group by channel
        channel_product = preprocess.group_product(year_frame, key='channel')

        # merge requirement of same date for every channel
        for channel, channel_frame in list(channel_product.items()):
            channel_product[channel] = preprocess.merge_product_date(channel_frame)

        year_products[year] = channel_product

    return year_products


def preprocessing8(data: pd.DataFrame):
    """
    将数据按年份分类，对每年合并相同季节的需求量
    :param data: 总订单表
    :return: 年份分组字典，每一年为一个DataFrame，包含四季的需求量
    """

    products = preprocess.group_product(data, key='year')

    for year, year_frame in list(products.items()):
        products[year] = preprocess.merge_product_season(year_frame)

    return products
