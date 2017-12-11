import json
from django.core.cache import cache
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from ..tasks import weibo_spider_friend, zhihu_spider_friend, tieba_spider_friend

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
    all_friends = user.friend_set.filter(group='未分组')
    paginator = Paginator(all_friends, 9)
    friends = paginator.page(1)

    group_list = user.group_list.split(',')
    group_list = list(enumerate(group_list))
    context = {'group_list': group_list, 'current_group': 0, 'friends': friends}
    return render(request, 'closends/setting_friends_manage.html', context)


@csrf_exempt
@login_required
def get_group_friends(request, group, page):
    user = request.user.userinfo
    group_list = user.group_list.split(',')
    all_friends = user.friend_set.filter(group=group_list[int(group)])
    paginator = Paginator(all_friends, 9)
    try:
        friends = paginator.page(page)
    except PageNotAnInteger:
        friends = paginator.page(1)
    except EmptyPage:
        friends = paginator.page(paginator.num_pages)

    group_list = list(enumerate(group_list))
    context = {'group_list': group_list, 'current_group': int(group), 'friends': friends}
    return render(request, 'closends/setting_friends_manage.html', context)


@csrf_exempt
@login_required
def add_group(request):
    if request.method == 'POST':
        user = request.user.userinfo
        group_name = request.POST['group_name']
        group_list = user.group_list.split(',')
        if group_name in group_list:
            result = {'status': 'error', 'error_msg': 'group_exsit'}
            return HttpResponse(json.dumps(result), content_type='application/json')

        group_list.append(group_name)
        user.group_list = ','.join(group_list)
        user.save()
        result = {'status': 'success'}
        return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
@login_required
def delete_group(request):
    if request.method == 'POST':
        user = request.user.userinfo
        group_list = user.group_list.split(',')
        group_name = request.POST['group_name']
        group_list.remove(group_name)
        user.group_list = ','.join(group_list)
        user.save()

        friends = user.friend_set.filter(group=group_name)
        for friend in friends:
            friend.group = '未分组'
            friend.save()
        return HttpResponse("")


@csrf_exempt
@login_required
def add_friend(request):
    user = request.user.userinfo
    group_list = user.group_list.split(',')
    return render(request, 'closends/setting_add_friends.html', {'group_list': group_list})


@csrf_exempt
@login_required
def delete_friend(request):
    if request.method == "POST":
        user = request.user.userinfo
        friend = user.friend_set.filter(nickname=request.POST['friend_name'])[0]
        friend.delete()
        return HttpResponse("")


@csrf_exempt
@login_required
def add_friend_info(request):
    if request.method == 'POST':
        user = request.user.userinfo
        nickname = request.POST['nickname']
        group_name = request.POST['group']
        if user.friend_set.filter(nickname=nickname):
            result = {'status': 'error', 'error_msg': 'nickname_exist'}
            return HttpResponse(json.dumps(result), content_type='application/json')

        if not request.FILES:
            user.friend_set.create(nickname=nickname, group=group_name)
        else:
            head_img = request.FILES['head_img']
            user.friend_set.create(nickname=nickname, head_img=head_img, group=group_name)
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
        result = {'status': 'success',
                  'head_img': head_img,
                  'group_name': friend.group}
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

        group_name = request.POST['group']
        friend = user.friend_set.filter(nickname=old_nickname)[0]
        friend.nickname = nickname
        friend.group = group_name
        if request.FILES:
            friend.head_img = request.FILES['head_img']
        friend.save()
        result = {'status': 'success'}
        return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
@login_required
def delete_friend_weibo(request):
    if request.method == 'POST':
        user = request.user.userinfo
        friend_name = request.POST['friend_name']
        friend = user.friend_set.filter(nickname=friend_name)[0]
        friend.weibo_ID = ""
        friend.weibo_account = ""
        friend.weibo_link = ""
        friend.weibo_head = ""
        friend.save()
        return HttpResponse("")


@csrf_exempt
@login_required
def add_found_friend_weibo(request):
    if request.method == 'POST':
        user = request.user.userinfo
        friend_name = request.POST['friend_name']
        friend = user.friend_set.filter(nickname=friend_name)[0]
        friend.weibo_ID = request.POST['ID']
        friend.weibo_account = request.POST['account']
        friend.weibo_link = request.POST['link']
        friend.weibo_head = request.POST['head']
        friend.save()

        args = {'id': friend.id, 'weibo_ID': friend.weibo_ID}
        weibo_spider_friend.delay(request.user.username, args)
        
        updating_list = cache.get_or_set('weibo_updating_list', set())
        updating_list.add(friend.id)
        cache.set('weibo_updating_list', updating_list, None)
        return HttpResponse("")


@csrf_exempt
@login_required
def query_exist_friend_weibo(request):
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
def delete_friend_zhihu(request):
    if request.method == 'POST':
        user = request.user.userinfo
        friend_name = request.POST['friend_name']
        friend = user.friend_set.filter(nickname=friend_name)[0]
        friend.zhihu_ID = ""
        friend.zhihu_account = ""
        friend.zhihu_link = ""
        friend.zhihu_head = ""
        friend.save()
        return HttpResponse("")


@csrf_exempt
@login_required
def add_found_friend_zhihu(request):
    if request.method == 'POST':
        user = request.user.userinfo
        friend_name = request.POST['friend_name']
        friend = user.friend_set.filter(nickname=friend_name)[0]
        friend.zhihu_ID = request.POST['ID']
        friend.zhihu_account = request.POST['account']
        friend.zhihu_link = 'https://www.zhihu.com' + request.POST['link']
        friend.zhihu_head = request.POST['head']
        friend.save()

        args = {'id': friend.id, 'zhihu_ID': friend.zhihu_ID}
        zhihu_spider_friend.delay(request.user.username, args)

        updating_list = cache.get_or_set('zhihu_updating_list', set())
        updating_list.add(friend.id)
        cache.set('zhihu_updating_list', updating_list, None)
        return HttpResponse("")


@csrf_exempt
@login_required
def query_exist_friend_zhihu(request):
    if request.method == 'POST':
        user = request.user.userinfo
        friend_name = request.POST['friend_name']
        friend = user.friend_set.filter(nickname=friend_name)[0]
        account = friend.zhihu_account
        link = friend.zhihu_link
        head = friend.zhihu_head
        result = {'account': account, 'link': link, 'head': head}
        return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
@login_required
def delete_friend_tieba(request):
    if request.method == 'POST':
        user = request.user.userinfo
        friend_name = request.POST['friend_name']
        friend = user.friend_set.filter(nickname=friend_name)[0]
        friend.tieba_ID = ""
        friend.tieba_account = ""
        friend.tieba_link = ""
        friend.tieba_head = ""
        friend.save()
        return HttpResponse("")


@csrf_exempt
@login_required
def add_found_friend_tieba(request):
    if request.method == 'POST':
        user = request.user.userinfo
        friend_name = request.POST['friend_name']
        friend = user.friend_set.filter(nickname=friend_name)[0]
        friend.tieba_ID = request.POST['ID']
        friend.tieba_account = request.POST['account']
        friend.tieba_link = request.POST['link']
        friend.tieba_head = request.POST['head']
        friend.save()

        args = {'id': friend.id, 'tieba_ID': friend.tieba_ID}
        tieba_spider_friend.delay(request.user.username, args)

        updating_list = cache.get_or_set('tieba_updating_list', set())
        updating_list.add(friend.id)
        cache.set('tieba_updating_list', updating_list, None)
        return HttpResponse("")


@csrf_exempt
@login_required
def query_exist_friend_tieba(request):
    if request.method == 'POST':
        user = request.user.userinfo
        friend_name = request.POST['friend_name']
        friend = user.friend_set.filter(nickname=friend_name)[0]
        account = friend.tieba_account
        link = friend.tieba_link
        head = friend.tieba_head
        result = {'account': account, 'link': link, 'head': head}
        return HttpResponse(json.dumps(result), content_type='application/json')
