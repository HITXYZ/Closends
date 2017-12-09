import operator
from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from closends.methods.draw_bar import draw_bar
from closends.methods.draw_line import draw_liveness
from closends.methods.word2cloud import generate_cloud


@csrf_exempt
@login_required
def friend_index(request, friend, page=1):
    user = request.user.userinfo
    friend_item = user.friend_set.filter(nickname=friend)[0]

    weibo_contents = friend_item.weibocontent_set.all()
    zhihu_contents = friend_item.zhihucontent_set.all()
    tieba_contents = friend_item.tiebacontent_set.all()
    all_contents = []
    all_contents += weibo_contents
    all_contents += zhihu_contents
    all_contents += tieba_contents
    all_contents.sort(key=lambda content: content.pub_date, reverse=True)

    word_num = {}
    for content in all_contents:
        topic = content.topic
        if not word_num.get(topic):
            word_num[topic] = 1
        else:
            word_num[topic] += 1
    word_num = sorted(word_num.items(), key=operator.itemgetter(1, 0), reverse=True)

    draw_bar(word_num)
    generate_cloud(word_num)
    draw_liveness(weibo_contents, zhihu_contents, tieba_contents)

    paginator = Paginator(all_contents, 20)
    try:
        contents = paginator.page(page)
    except PageNotAnInteger:
        contents = paginator.page(1)
    except EmptyPage:
        contents = paginator.page(paginator.num_pages)

    result = {'contents': contents,
              'friend': friend_item,
              'current_friend': friend, }
    return render(request, 'closends/friend_index.html', result)
