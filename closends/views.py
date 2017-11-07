from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, render_to_response, HttpResponse, HttpResponseRedirect

import json
from .models import *


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
    return render(request, 'closends/user_info.html')


@csrf_exempt
@login_required
def user_binding(request):
    return render(request, 'closends/user_binding.html')


@csrf_exempt
@login_required
def friend_manage(request):
    return render(request, 'closends/friends_manage.html')

