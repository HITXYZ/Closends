from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, render_to_response, HttpResponse, HttpResponseRedirect

import json
from .models import *
from .user_binding import *


@csrf_exempt
def page_not_found(request):
    return render_to_response('404.html')


@csrf_exempt
def page_error(request):
    return render_to_response('500.html')


@csrf_exempt
def to_login(request):
    if request.user.is_authenticated:
        print(request.user.email)
    return render(request, 'closends/login.html')


@csrf_exempt
def to_register(request):
    return render(request, 'closends/register.html')


@csrf_exempt
def username_login(request):
    if request.method == "POST":
        info = request.POST
        username = info['username']
        password = info['password']
        if not User.objects.filter(username=username):
            result = {'status': 'error', 'error_message': 'user_not_exist'}
            return HttpResponse(json.dumps(result), content_type='application/json')
        user = authenticate(request=request, username=username, password=password)
        if user and user.is_active:
            login(request, user)
            try:
                info['remember_me']
            except Exception:
                request.session.set_expiry(0)
            result = {'status': 'success'}
            return HttpResponse(json.dumps(result), content_type='application/json')
        result = {'status': 'error', 'error_message': 'wrong_password'}
        return HttpResponse(json.dumps(result), content_type='application/json')
    else:
        return render_to_response('404.html')


@csrf_exempt
def email_login(request):
    if request.method == "POST":
        info = request.POST
        email = info['email']
        password = info['password']
        if not User.objects.get(email=email):
            result = {'status': 'error', 'error_message': 'user_not_exist'}
            return HttpResponse(json.dumps(result), content_type='application/json')
        user = authenticate(request=request, email=email, password=password)
        if user and user.is_active:
            login(request, user)
            try:
                info['remember_me']
            except Exception:
                request.session.set_expiry(0)
            result = {'status': 'success'}
            return HttpResponse(json.dumps(result), content_type='application/json')
        result = {'status': 'error', 'error_message': 'wrong_password'}
        return HttpResponse(json.dumps(result), content_type='application/json')
    else:
        return render_to_response('404.html')


@csrf_exempt
def register(request):
    if request.method == "POST":
        info = request.POST

        # check username
        username = info['username']
        if User.objects.filter(username=username):
            result = {'status': 'error', 'error_message': 'username_exist'}
            return HttpResponse(json.dumps(result), content_type='application/json')

        # check email
        email = info['email']
        if User.objects.filter(email=email):
            result = {'status': 'error', 'error_message': 'email_exist'}
            return HttpResponse(json.dumps(result), content_type='application/json')

        # register new user
        password = info['password1']
        try:
            User.objects.create_user(username, email, password).save()
        except:
            result = {'status': 'error', 'error_message': 'other'}
            return HttpResponse(json.dumps(result), content_type='application/json')
        else:
            result = {'status': 'success'}
            return HttpResponse(json.dumps(result), content_type='application/json')
    else:
        return render_to_response('404.html')


@csrf_exempt
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('closends:to_login'))


@csrf_exempt
@login_required
def index(request):
    user = request.user
    print(user.username, user.email)
    return render(request, 'closends/index.html')


@csrf_exempt
@login_required
def user_info(request):
    user = request.user.userinfo
    context = {'user': user}
    return render(request, 'closends/user_info.html', context)


@csrf_exempt
@login_required
def user_binding(request):
    sites = request.user.userinfo.website_set.all()
    binding_sites = {}
    for site in sites:
        binding_sites[site.site] = site.account
    print(binding_sites)
    binding_sites = {'binding_sites': binding_sites}
    return render(request, 'closends/user_binding.html', binding_sites)


@csrf_exempt
@login_required
def qq_binding(request):
    if request.method == 'POST':
        qq = request.POST['qq']
        password = request.POST['password']
        status = qq_login(qq, password)
        # print(qq, password, status)
        if status:
            user = request.user.userinfo
            user.website_set.create(site='qq', account=qq, authcode=password)
            result = {'status': 'success'}
        else:
            result = {'status': 'error', 'error_msg': 'wrong_password'}
        return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
@login_required
def qq_unbinding(request):
    sites = request.user.userinfo.website_set.all()
    binding_sites = {}
    for site in sites:
        if site.site == 'qq':
            site.delete()
        else:
            binding_sites[site.site] = site.account
    binding_sites = {'binding_sites': binding_sites}
    return render(request, 'closends/user_binding.html', binding_sites)


@csrf_exempt
@login_required
def weibo_binding(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        status = weibo_login(username, password)
        print(username, password, status)
        if status:
            user = request.user.userinfo
            user.website_set.create(site='weibo', account=username, authcode=password)
            result = {'status': 'success'}
        else:
            result = {'status': 'error', 'error_msg': 'wrong_password'}
        return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
@login_required
def weibo_unbinding(request):
    sites = request.user.userinfo.website_set.all()
    binding_sites = {}
    for site in sites:
        if site.site == 'weibo':
            site.delete()
        else:
            binding_sites[site.site] = site.account
    binding_sites = {'binding_sites': binding_sites}
    return render(request, 'closends/user_binding.html', binding_sites)


@csrf_exempt
@login_required
def zhihu_binding(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        status = zhihu_login(username, password)
        print(username, password, status)
        if status:
            user = request.user.userinfo
            user.website_set.create(site='zhihu', account=username, authcode=password)
            result = {'status': 'success'}
        else:
            result = {'status': 'error', 'error_msg': 'wrong_password'}
        return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
@login_required
def zhihu_unbinding(request):
    sites = request.user.userinfo.website_set.all()
    binding_sites = {}
    for site in sites:
        if site.site == 'zhihu':
            site.delete()
        else:
            binding_sites[site.site] = site.account
    binding_sites = {'binding_sites': binding_sites}
    return render(request, 'closends/user_binding.html', binding_sites)


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
    return render(request, 'closends/friends_manage.html', context)


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
    context = {'group_list': group_list, 'current_group': 'group_0', 'friends':friends}
    return render(request, 'closends/friends_manage.html', context)


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
        group_index = 'group_' + str(len(group_list)-1)
        group_url = reverse('closends:setting:get_group_friends', args=(group_index, 1))
        print(group_url)
        result = {'status': 'success', 'group_name': group_name, 'group_url': group_url}
        return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
@login_required
def add_friend(request):
    return render(request, 'closends/add_friends.html')


@csrf_exempt
@login_required
def add_qq_friend(request):
    if request.method == 'POST':
        user = request.user.userinfo
        qq = request.POST['qq']
        # check qq account
        user.friend_set
        result = {}
        return HttpResponse(json.dumps(result), content_type='application')


@csrf_exempt
def get_github_code(request, code):
    print(code)
    pass
