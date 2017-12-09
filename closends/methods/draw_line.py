from django.conf import settings
from matplotlib import pyplot as plt
from datetime import datetime, timedelta

base_dir = settings.BASE_DIR + '/static/closends/bar_graph/'
plt.rcParams['font.sans-serif'] = ['SimHei']


def weibo_liveness(dates, liveness):
    plt.figure()
    plt.xlabel("时间")
    plt.ylabel("活跃度")
    plt.title("微博活跃度统计")
    plt.grid(True)

    plt.plot(list(range(7)), liveness)
    plt.xticks(list(range(7)), dates)
    plt.savefig(base_dir + 'weibo_liveness.jpg')


def zhihu_liveness(dates, liveness):
    plt.figure()
    plt.xlabel("时间")
    plt.ylabel("活跃度")
    plt.title("知乎活跃度统计")
    plt.grid(True)

    plt.plot(list(range(7)), liveness)
    plt.xticks(list(range(7)), dates)
    plt.savefig(base_dir + 'zhihu_liveness.jpg')


def tieba_liveness(dates, liveness):
    plt.figure()
    plt.xlabel("时间")
    plt.ylabel("活跃度")
    plt.title("贴吧活跃度统计")
    plt.grid(True)

    plt.plot(list(range(7)), liveness)
    plt.xticks(list(range(7)), dates)
    plt.savefig(base_dir + 'tieba_liveness.jpg')


def total_liveness(dates, liveness):
    plt.figure()
    plt.xlabel("时间")
    plt.ylabel("活跃度")
    plt.title("总体活跃度统计")
    plt.grid(True)

    plt.plot(list(range(7)), liveness)
    plt.xticks(list(range(7)), dates)
    plt.savefig(base_dir + 'total_liveness.jpg')


def draw_liveness(weibo_contents, zhihu_contents, tieba_contents):
    dates = []
    today = datetime.now()
    for i in range(7):
        today += timedelta(days=-1)
        dates.append(today.strftime('%m-%d'))

    date_num = dict(zip(dates, [0 for _ in range(7)]))
    for content in weibo_contents:
        cur_date = str(content.pub_date)[5:10]
        if date_num.get(cur_date, -1) == -1: continue
        date_num[cur_date] += 1
    weibo_num = list(date_num.values())

    date_num = dict(zip(dates, [0 for _ in range(7)]))
    for content in zhihu_contents:
        cur_date = str(content.pub_date)[5:10]
        if date_num.get(cur_date, -1) == -1: continue
        date_num[cur_date] += 1
    zhihu_num = list(date_num.values())

    date_num = dict(zip(dates, [0 for _ in range(7)]))
    for content in tieba_contents:
        cur_date = str(content.pub_date)[5:10]
        if date_num.get(cur_date, -1) == -1: continue
        date_num[cur_date] += 1
    tieba_num = list(date_num.values())
    total_num = [a + b + c for a, b, c in zip(weibo_num, zhihu_num, tieba_num)]

    weibo_liveness(dates, weibo_num)
    zhihu_liveness(dates, zhihu_num)
    tieba_liveness(dates, tieba_num)
    total_liveness(dates, total_num)


if __name__ == '__main__':
    dates = ['10月1日', '10月2日', '10月3日', '10月4日', '10月5日', '10月6日', '10月7日']
    liveness = [60, 85, 95, 90, 80, 85, 75]
    weibo_liveness(dates, liveness)
