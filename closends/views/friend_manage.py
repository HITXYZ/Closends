import json

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse

"""
    好友管理模块:
        分组管理 增、移
        好友管理 增、删、改、查询
        好友账号管理 增、删、改、查询
"""


@csrf_exempt
@login_required
def friend_manage(request):
    user = request.user.userinfo
    all_friends = user.friend_set.filter(group='group_0')
    paginator = Paginator(all_friends, 9)
    friends = paginator.page(1)

    group_name = user.group_list.split(',')
    group_index = ['group_' + str(index) for index in range(len(group_name))]
    group_list = list(zip(group_index, group_name))
    context = {'group_list': group_list, 'current_group': 'group_0', 'friends': friends}
    return render(request, 'closends/setting_friends_manage.html', context)


@csrf_exempt
@login_required
def get_group_friends(request, group, page):
    user = request.user.userinfo
    all_friends = user.friend_set.filter(group=group)
    paginator = Paginator(all_friends, 9)
    try:
        friends = paginator.page(page)
    except PageNotAnInteger:
        friends = paginator.page(1)
    except EmptyPage:
        friends = paginator.page(paginator.num_pages)

    group_name = user.group_list.split(',')
    group_index = ['group_' + str(index) for index in range(len(group_name))]
    group_list = list(zip(group_index, group_name))
    context = {'group_list': group_list, 'current_group': group, 'friends': friends}
    return render(request, 'closends/setting_friends_manage.html', context)


@csrf_exempt
@login_required
def add_group(request):
    if request.method == 'POST':
        group_name = request.POST['group_name']
        user = request.user.userinfo
        group_list = user.group_list.split(',')
        if group_name in group_list:
            result = {'status': 'error', 'error_msg': 'group_exsit'}
            return HttpResponse(json.dumps(result), content_type='application/json')

        group_list.append(group_name)
        user.group_list = ','.join(group_list)
        user.save()
        group_index = 'group_' + str(len(group_list) - 1)
        group_url = reverse('closends:setting:get_group_friends', args=(group_index, 1))
        result = {'status': 'success', 'group_name': group_name, 'group_url': group_url}
        return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
@login_required
def add_friend(request):
    user = request.user.userinfo
    group_name = user.group_list.split(',')
    return render(request, 'closends/setting_add_friends.html', {'group_list': group_name})


@csrf_exempt
@login_required
def delete_friend(request):
    if request.method == "POST":
        user = request.user.userinfo
        friend = user.friend_set.filter(nickname=request.POST['friend_name'])[0]
        friend.delete()
        friend.save()
        return HttpResponse("")


@csrf_exempt
@login_required
def add_friend_info(request):
    if request.method == 'POST':
        user = request.user.userinfo
        nickname = request.POST['nickname']
        group_name = user.group_list.split(',')
        group_index = 'group_' + str(group_name.index(request.POST['group']))
        if user.friend_set.filter(nickname=nickname):
            result = {'status': 'error', 'error_msg': 'nickname_exist'}
            return HttpResponse(json.dumps(result), content_type='application/json')

        if not request.FILES:
            user.friend_set.create(nickname=nickname, group=group_index)
        else:
            head_img = request.FILES['head_img']
            user.friend_set.create(nickname=nickname, head_img=head_img, group=group_index)
        user.save()
        result = {'status': 'success'}
        return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
@login_required
def query_friend_info(request):
    if request.method == 'POST':
        user = request.user.userinfo
        friend_name = request.POST['friend_name']
        friend = user.friend_set.filter(nickname=friend_name)[0]
        head_img = friend.image_name()
        group_list = user.group_list.split(',')
        group_name = group_list[int(friend.group[6:])]
        result = {'status': 'success', 'head_img': head_img, 'group_name': group_name}
        return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
@login_required
def update_friend_info(request):
    if request.method == 'POST':
        user = request.user.userinfo
        nickname = request.POST['nickname']
        old_nickname = request.POST['old_nickname']
        if nickname != old_nickname:
            if user.friend_set.filter(nickname=nickname):
                result = {'status': 'error', 'error_msg': 'nickname_exist'}
                return HttpResponse(json.dumps(result), content_type='application/json')

        group_name = user.group_list.split(',')
        group_index = 'group_' + str(group_name.index(request.POST['group']))

        friend = user.friend_set.filter(nickname=old_nickname)[0]
        friend.nickname = nickname
        friend.group = group_index
        if request.FILES:
            friend.head_img = request.FILES['head_img']
        friend.save()
        result = {'status': 'success'}
        return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
@login_required
def add_found_weibo_friend(request):
    if request.method == 'POST':
        user = request.user.userinfo
        friend_name = request.POST['friend_name']
        friend = user.friend_set.filter(nickname=friend_name)[0]
        friend.weibo_account = request.POST['account']
        friend.weibo_link = request.POST['link']
        friend.weibo_head = request.POST['head']
        friend.save()
        result = {'status': 'success'}
        return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
@login_required
def query_exist_weibo_friend(request):
    if request.method == 'POST':
        user = request.user.userinfo
        friend_name = request.POST['friend_name']
        friend = user.friend_set.filter(nickname=friend_name)[0]
        account = friend.weibo_account
        link = friend.weibo_link
        head = friend.weibo_head
        result = {'account': account, 'link': link, 'head': head}
        return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
@login_required
def query_weibo_friend_by_link(request):
    if request.method == 'POST':
        # user = request.user.userinfo
        # weibo_link = request.POST['weibo_link']
        result = {}
        return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
@login_required
def query_weibo_friend_by_account(request):
    if request.method == 'POST':
        weibo_account = request.POST['weibo_account']
        person_html = ""
        result = {'status': 'success', 'person_html': person_html}
        return HttpResponse(json.dumps(result), content_type='application/json')
