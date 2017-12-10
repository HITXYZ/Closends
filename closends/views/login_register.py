import json
from ..models import *
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, render_to_response, HttpResponse, HttpResponseRedirect

"""
    登录注册注销模块：
        用户名、密码登录
"""


@csrf_exempt
def to_login(request):
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
            result = {'status': 'error', 'error_msg': 'user_not_exist'}
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
        result = {'status': 'error', 'error_msg': 'wrong_password'}
        return HttpResponse(json.dumps(result), content_type='application/json')
    else:
        return render_to_response('404.html')


@csrf_exempt
def email_login(request):
    if request.method == "POST":
        info = request.POST
        email = info['email']
        password = info['password']
        print(email, password)
        if not User.objects.filter(email=email):
            result = {'status': 'error', 'error_msg': 'user_not_exist'}
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
        result = {'status': 'error', 'error_msg': 'wrong_password'}
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
            user = User.objects.create_user(username, email, password)
            userinfo = UserInfo(user=user)
            user.userinfo = userinfo
            userinfo.save()
            user.save()
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
