import json

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse

"""
    账号绑定模块:
        绑定、查询、更改、取绑
"""


@csrf_exempt
@login_required
def user_binding(request):
    sites = request.user.userinfo.website_set.all()
    binding_sites = {}
    for site in sites:
        binding_sites[site.site] = site.account
    binding_sites = {'binding_sites': binding_sites}
    return render(request, 'closends/setting_user_binding.html', binding_sites)


@csrf_exempt
@login_required
def query_weibo_user(request):
    if request.method == "POST":
        weibo_account = request.POST['weibo_account']
        if request.POST['adding_option'] == "账号":
            person_html = ""
        else:
            person_html = ""
        result = {'status': 'success', 'person_html': person_html}
        return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
@login_required
def query_bound_weibo_info(request):
    if request.method == 'POST':
        user = request.user.userinfo
        weibo = user.website_set.filter(site='weibo')[0]
        result = {'link': weibo.link, 'head': weibo.head}
        return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
@login_required
def weibo_binding(request):
    if request.method == 'POST':
        user = request.user.userinfo
        account = request.POST['account']
        link = request.POST['link']
        head = request.POST['head']
        site = user.website_set.filter(site='weibo')
        if not site:  # binding account
            user.website_set.create(site='weibo', account=account, link=link, head=head)
            user.save()
        else:  # update account
            site = site[0]
            site.account = account
            site.link = link
            site.head = head
            site.save()
        result = {'status': 'success'}
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
    return render(request, 'closends/setting_user_binding.html', binding_sites)


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
    return render(request, 'closends/setting_user_binding.html', binding_sites)


@csrf_exempt
@login_required
def zhihu_unbinding(request):
    sites = request.user.userinfo.website_set.all()
    binding_sites = {}
    for site in sites:
        if site.site == 'tieba':
            site.delete()
        else:
            binding_sites[site.site] = site.account
    binding_sites = {'binding_sites': binding_sites}
    return render(request, 'closends/setting_user_binding.html', binding_sites)
