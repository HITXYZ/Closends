import operator
from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from closends.word2cloud.word2cloud import generate_cloud
from closends.methods.draw_bar import draw_bar

@csrf_exempt
@login_required
def friend_index(request, friend, page=1):
    user = request.user.userinfo
    friend_item = user.friend_set.filter(nickname=friend)[0]
    all_contents = []
    all_contents += friend_item.weibocontent_set.all()
    all_contents += friend_item.zhihucontent_set.all()
    all_contents += friend_item.tiebacontent_set.all()

    # generate wordcloud
    word_num = {}
    for content in all_contents:
        topic = content.topic
        if not word_num.get(topic):
            word_num[topic] = 1
        else:
            word_num[topic] += 1
    word_num = sorted(word_num.items(), key=operator.itemgetter(1, 0), reverse=True)
    generate_cloud(word_num)

    # draw bar of first five interest
    labels = [label for label, _ in word_num[:5]]
    quants = [num for _, num in word_num[:5]]
    quants = [num/sum(quants) for num in quants]
    draw_bar(labels, quants)

    # all_contents.sort(key=lambda content: content.pub_date)

    paginator = Paginator(all_contents, 20)
    try:
        contents = paginator.page(page)
    except PageNotAnInteger:
        contents = paginator.page(1)
    except EmptyPage:
        contents = paginator.page(paginator.num_pages)

    result = {'contents': contents,
              'friend': friend_item,
              'current_friend': friend,}
    return render(request, 'closends/friend_index.html', result)