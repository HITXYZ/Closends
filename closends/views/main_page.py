from ..models import WeiboContent, Image
from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

"""
    动态主页模块：
        平台、分组、主题、时间、关键字查询
"""

topic_name = ['体育', '健康', '动漫', '女性', '娱乐', '房产',
              '教育', '文学', '新闻', '旅游', '时尚', '校园',
              '汽车', '游戏', '生活', '科技', '美食', '育儿', '财经']


@csrf_exempt
@login_required
def query_all(request, page=1):
    user = request.user.userinfo
    friends = user.friend_set.all()
    group_list = user.group_list.split(',')
    group_list = list(enumerate(group_list))
    topic_list = list(enumerate(topic_name))

    all_contents = []
    for friend in friends:
        weibo_contents = friend.weibocontent_set.all()
        zhihu_contents = friend.zhihucontent_set.all()
        tieba_contents = friend.tiebacontent_set.all()
        content_type = ContentType.objects.get_for_model(WeiboContent)
        for content in weibo_contents:
            if not content.is_repost:
                if content.has_image:
                    content.images = Image.objects.filter(content_type=content_type, object_id=content.id)
            else:
                if content.origin_has_image:
                    content.origin_images = Image.objects.filter(content_type=content_type, object_id=content.id)

        all_contents += weibo_contents
        all_contents += zhihu_contents
        all_contents += tieba_contents

    # all_contents.sort(key= lambda content: content.pub_date)

    paginator = Paginator(all_contents, 20)
    try:
        contents = paginator.page(page)
    except PageNotAnInteger:
        contents = paginator.page(1)
    except EmptyPage:
        contents = paginator.page(paginator.num_pages)

    result = {'group_list': group_list,
              'topic_list': topic_list,
              'contents': contents}
    return render(request, 'closends/index.html', result)


@csrf_exempt
@login_required
def query_by_group(request, group, page=1):
    user = request.user.userinfo
    friends = user.friend_set.all()
    group_list = user.group_list.split(',')
    topic_list = list(enumerate(topic_name))

    all_contents = []
    for friend in friends:
        if friend.group == group_list[int(group)]:
            weibo_contents = friend.weibocontent_set.all()
            zhihu_contents = friend.zhihucontent_set.all()
            tieba_contents = friend.tiebacontent_set.all()
            content_type = ContentType.objects.get_for_model(WeiboContent)
            for content in weibo_contents:
                if not content.is_repost:
                    if content.has_image:
                        content.images = Image.objects.filter(content_type=content_type, object_id=content.id)
                else:
                    if content.origin_has_image:
                        content.origin_images = Image.objects.filter(content_type=content_type, object_id=content.id)

            all_contents += weibo_contents
            all_contents += zhihu_contents
            all_contents += tieba_contents

    # all_contents.sort(key=lambda content: content.pub_date)

    paginator = Paginator(all_contents, 20)
    try:
        contents = paginator.page(page)
    except PageNotAnInteger:
        contents = paginator.page(1)
    except EmptyPage:
        contents = paginator.page(paginator.num_pages)

    group_list = list(enumerate(group_list))
    result = {'group_list': group_list,
              'topic_list': topic_list,
              'current_group': group,
              'contents': contents}
    return render(request, 'closends/display_group.html', result)


@csrf_exempt
@login_required
def query_by_platform(request, platform, page=1):
    user = request.user.userinfo
    friends = user.friend_set.all()
    group_list = user.group_list.split(',')
    group_list = list(enumerate(group_list))
    topic_list = list(enumerate(topic_name))

    all_contents = []
    if platform == 'weibo':
        for friend in friends:
            all_contents += friend.weibocontent_set.all()
        content_type = ContentType.objects.get_for_model(WeiboContent)
        for content in all_contents:
            if not content.is_repost:
                if content.has_image:
                    content.images = Image.objects.filter(content_type=content_type, object_id=content.id)
            else:
                if content.origin_has_image:
                    content.origin_images = Image.objects.filter(content_type=content_type, object_id=content.id)
    elif platform == 'zhihu':
        for friend in friends:
            all_contents += friend.zhihucontent_set.all()
    elif platform == 'tieba':
        for friend in friends:
            all_contents += friend.tiebacontent_set.all()

    # all_contents.sort(key=lambda content: content.pub_date)

    paginator = Paginator(all_contents, 20)
    try:
        contents = paginator.page(page)
    except PageNotAnInteger:
        contents = paginator.page(1)
    except EmptyPage:
        contents = paginator.page(paginator.num_pages)

    result = {'group_list': group_list,
              'topic_list': topic_list,
              'current_platform': platform,
              'contents': contents}
    return render(request, 'closends/display_platform.html', result)


@csrf_exempt
@login_required
def query_by_topic(request, topic, page=1):
    print(topic)
    user = request.user.userinfo
    friends = user.friend_set.all()
    group_list = user.group_list.split(',')
    group_list = list(enumerate(group_list))
    topic_list = list(enumerate(topic_name))

    all_contents = []
    for friend in friends:
        weibo_contents = [content for content in friend.weibocontent_set.all() if content.topic == topic_name[int(topic)]]
        zhihu_contents = [content for content in friend.zhihucontent_set.all() if content.topic == topic_name[int(topic)]]
        tieba_contents = [content for content in friend.tiebacontent_set.all() if content.topic == topic_name[int(topic)]]
        content_type = ContentType.objects.get_for_model(WeiboContent)
        for content in weibo_contents:
            if not content.is_repost:
                if content.has_image:
                    content.images = Image.objects.filter(content_type=content_type, object_id=content.id)
            else:
                if content.origin_has_image:
                    content.origin_images = Image.objects.filter(content_type=content_type, object_id=content.id)
        all_contents += weibo_contents
        all_contents += zhihu_contents
        all_contents += tieba_contents

    # all_contents.sort(key=lambda content: content.pub_date)

    paginator = Paginator(all_contents, 20)
    try:
        contents = paginator.page(page)
    except PageNotAnInteger:
        contents = paginator.page(1)
    except EmptyPage:
        contents = paginator.page(paginator.num_pages)

    result = {'group_list': group_list,
              'topic_list': topic_list,
              'current_topic': topic,
              'contents': contents}
    return render(request, 'closends/display_topic.html', result)
