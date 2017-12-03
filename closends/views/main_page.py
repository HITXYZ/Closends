from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from ..models import WeiboContent, Image

"""
    动态主页模块：
        平台、分组、主题、时间、关键字查询
"""


@csrf_exempt
@login_required
def query_all(request, page=1):
    user = request.user.userinfo
    group_name = user.group_list.split(',')
    group_index = ['group_' + str(index) for index in range(len(group_name))]
    group_list = list(zip(group_index, group_name))

    friends = user.friend_set.all()
    all_contents = []
    for friend in friends:
        all_contents += friend.weibocontent_set.all()
    all_contents.sort(key= lambda content: content.pub_date)
    paginator = Paginator(all_contents, 20)
    try:
        contents = paginator.page(page)
    except PageNotAnInteger:
        contents = paginator.page(1)
    except EmptyPage:
        contents = paginator.page(paginator.num_pages)

    content_type = ContentType.objects.get_for_model(WeiboContent)
    for content in contents:
        if not content.is_repost:
            if content.has_image:
                content.images = Image.objects.filter(content_type=content_type, object_id=content.id)
        else:
            if content.origin_has_image:
                content.origin_images = Image.objects.filter(content_type=content_type, object_id=content.id)

    result = {'group_list': group_list, 'contents': contents, 'option':'index'}
    return render(request, 'closends/index.html', result)


@csrf_exempt
@login_required
def query_by_group(request, group, page=1):
    user = request.user.userinfo
    group_name = user.group_list.split(',')
    group_index = ['group_' + str(index) for index in range(len(group_name))]
    group_list = list(zip(group_index, group_name))

    friends = user.friend_set.all()
    all_contents = []
    for friend in friends:
        if friend.group == group:
            all_contents += friend.weibocontent_set.all()
    all_contents.sort(key=lambda content: content.pub_date)
    paginator = Paginator(all_contents, 20)
    try:
        contents = paginator.page(page)
    except PageNotAnInteger:
        contents = paginator.page(1)
    except EmptyPage:
        contents = paginator.page(paginator.num_pages)

    content_type = ContentType.objects.get_for_model(WeiboContent)
    for content in contents:
        if not content.is_repost:
            if content.has_image:
                content.images = Image.objects.filter(content_type=content_type, object_id=content.id)
        else:
            if content.origin_has_image:
                content.origin_images = Image.objects.filter(content_type=content_type, object_id=content.id)

    result = {'group_list': group_list, 'current_group': group, 'contents': contents, 'option': 'group'}
    return render(request, 'closends/index.html', result)