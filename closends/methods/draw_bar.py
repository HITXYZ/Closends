import numpy as np
from django.conf import settings
from matplotlib import pyplot as plt
plt.style.use('seaborn-dark')
plt.rcParams['font.sans-serif']=['SimHei']
colors = ['black', 'red', 'blue', 'green', 'yellow']


def draw_bar(labels, quants):
    ind = np.linspace(1, 5, 5)
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    ax.bar(ind, quants, width=0.5, color=colors)
    ax.set_xticks(ind)
    ax.set_xticklabels(labels)
    ax.set_xlabel('分类')
    ax.set_ylabel('比例')
    ax.set_title('他/她最感兴趣的内容')
    plt.grid(True)
    plt.ylim(0, max(quants) + 0.1)
    plt.savefig(settings.BASE_DIR + '/static/closends/bar_graph/interest_bar.jpg')


if __name__ == '__main__':
    x = sorted([4, 11, 11, 17, 8])
    x = [num / sum(x) for num in x]
    xlabel = ['新闻', '科技', '体育', '旅游', '文学']
    draw_bar(xlabel, x)