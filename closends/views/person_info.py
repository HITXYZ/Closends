import json
from ..models import *

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse

"""
    个人信息设置模块：
        查询、设置、更改
"""


@csrf_exempt
@login_required
def user_info(request):
    # user = request.user.userinfo
    # context = {'user': user}
    return render(request, 'closends/setting_user_info.html')


@csrf_exempt
@login_required
def set_head_image(request):
    if request.method == 'POST':
        user = request.user.userinfo
        if request.FILES:
            user.head_img = request.FILES['head_img']
            user.save()
        return HttpResponse("")


@csrf_exempt
@login_required
def update_username(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST['username']
        if username != user.username:
            if User.objects.filter(username=username):
                result = {'status': "error", 'error_msg': 'username_exist'}
                return HttpResponse(json.dumps(result), content_type='application/json')
            else:
                user.username = username
                user.save()
        result = {'status': 'success'}
        return HttpResponse(json.dumps(result), content_type='application/json')
