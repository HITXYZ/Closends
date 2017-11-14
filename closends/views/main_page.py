from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

"""
    动态主页模块：
        平台、分组、主题、时间、关键字查询
"""


@csrf_exempt
@login_required
def index(request):
    user = request.user.userinfo
    group_name = user.group_list.split(',')
    group_index = ['group_' + str(index) for index in range(len(group_name))]
    group_list = list(zip(group_index, group_name))
    result = {'group_list': group_list}
    return render(request, 'closends/index.html', result)
