import json

from closends.spider.weibo_search import get_user_by_account as get_weibo_user_by_account
from closends.spider.weibo_search import get_user_by_homepage as get_weibo_user_by_homepage
from closends.spider.zhihu_search import get_user_by_search as get_zhihu_user_by_account
from closends.spider.zhihu_search import get_user_by_homepage as get_zhihu_user_by_homepage
from closends.spider.tieba_search import get_user_by_search as get_tieba_user_by_account
from closends.spider.tieba_search import get_user_by_homepage as get_tieba_user_by_homepage

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
        binding_sites[site.site] = site.site_account
    binding_sites = {'binding_sites': binding_sites}
    return render(request, 'closends/setting_user_binding.html', binding_sites)


@csrf_exempt
@login_required
def query_weibo_user(request):
    if request.method == "POST":
        weibo_account = request.POST['weibo_account']
        if request.POST['adding_option'] == "账号":
            user_ids, user_htmls = get_weibo_user_by_account(weibo_account)
            if not user_ids:
                result = {'status':'error', 'error_msg': 'user_not_exist'}
            else:
                result = {'status': 'success', 'person_html': user_htmls[0], 'person_id': user_ids[0]}
            return HttpResponse(json.dumps(result), content_type='application/json')
        else:
            user_id, user_html = get_weibo_user_by_homepage(weibo_account)
            if user_id is None:
                result = {'status': 'error', 'error_msg': 'user_not_exist'}
            else:
                result = {'status': 'success', 'person_html': user_html, 'person_id': user_id}
            return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
@login_required
def query_bound_weibo_info(request):
    if request.method == 'POST':
        user = request.user.userinfo
        weibo = user.website_set.filter(site='weibo')[0]
        result = {'link': weibo.site_link, 'head': weibo.site_head}
        return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
@login_required
def weibo_binding(request):
    if request.method == 'POST':
        user = request.user.userinfo
        account = request.POST['account']
        ID = request.POST['ID']
        link = request.POST['link']
        head = request.POST['head']
        site = user.website_set.filter(site='weibo')
        if not site:  # binding account
            user.website_set.create(site='weibo', site_account=account, site_ID=ID,site_link=link, site_head=head)
            user.save()
        else:  # update account
            site = site[0]
            site.site_account = account
            site.ID = ID
            site.site_link = link
            site.site_head = head
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
            binding_sites[site.site] = site.site_account
    binding_sites = {'binding_sites': binding_sites}
    return render(request, 'closends/setting_user_binding.html', binding_sites)


@csrf_exempt
@login_required
def query_zhihu_user(request):
    if request.method == "POST":
        zhihu_account = request.POST['zhihu_account']
        if request.POST['adding_option'] == "账号":
            user_ids, user_htmls = get_zhihu_user_by_account(zhihu_account)
            if not user_ids:
                result = {'status':'error', 'error_msg': 'user_not_exist'}
            else:
                result = {'status': 'success', 'htmls': user_htmls[0], 'person_id': user_ids[0]}
            return HttpResponse(json.dumps(result), content_type='application/json')
        else:
            user_id, user_html = get_zhihu_user_by_homepage(zhihu_account)
            if user_id is None:
                result = {'status': 'error', 'error_msg': 'user_not_exist'}
            else:
                result = {'status': 'success', 'person_html': user_html, 'person_id': user_id}
            return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
@login_required
def query_bound_zhihu_info(request):
    if request.method == 'POST':
        user = request.user.userinfo
        zhihu = user.website_set.filter(site='zhihu')[0]
        result = {'link': zhihu.site_link, 'head': zhihu.site_head}
        return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
@login_required
def zhihu_binding(request):
    if request.method == 'POST':
        user = request.user.userinfo
        account = request.POST['account']
        ID = request.POST['ID']
        link = request.POST['link']
        head = request.POST['head']
        site = user.website_set.filter(site='zhihu')
        if not site:  # binding account
            user.website_set.create(site='zhihu', site_account=account, site_ID=ID,site_link=link, site_head=head)
            user.save()
        else:  # update account
            site = site[0]
            site.site_account = account
            site.ID = ID
            site.site_link = link
            site.site_head = head
            site.save()
        result = {'status': 'success'}
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
            binding_sites[site.site] = site.site_account
    binding_sites = {'binding_sites': binding_sites}
    return render(request, 'closends/setting_user_binding.html', binding_sites)


@csrf_exempt
@login_required
def query_tieba_user(request):
    if request.method == "POST":
        tieba_account = request.POST['tieba_account']
        if request.POST['adding_option'] == "账号":
            user_ids, user_htmls = get_tieba_user_by_account(tieba_account)
            if not user_ids:
                result = {'status':'error', 'error_msg': 'user_not_exist'}
            else:
                result = {'status': 'success', 'htmls': user_htmls[0], 'person_id': user_ids[0]}
            return HttpResponse(json.dumps(result), content_type='application/json')
        else:
            user_id, user_html = get_tieba_user_by_homepage(tieba_account)
            if user_id is None:
                result = {'status': 'error', 'error_msg': 'user_not_exist'}
            else:
                result = {'status': 'success', 'person_html': user_html, 'person_id': user_id}
            return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
@login_required
def query_bound_tieba_info(request):
    if request.method == 'POST':
        user = request.user.userinfo
        tieba = user.website_set.filter(site='tieba')[0]
        result = {'link': tieba.site_link, 'head': tieba.site_head}
        return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
@login_required
def tieba_binding(request):
    if request.method == 'POST':
        user = request.user.userinfo
        account = request.POST['account']
        ID = request.POST['ID']
        link = request.POST['link']
        head = request.POST['head']
        site = user.website_set.filter(site='tieba')
        if not site:  # binding account
            user.website_set.create(site='tieba', site_account=account, site_ID=ID,site_link=link, site_head=head)
            user.save()
        else:  # update account
            site = site[0]
            site.site_account = account
            site.ID = ID
            site.site_link = link
            site.site_head = head
            site.save()
        result = {'status': 'success'}
        return HttpResponse(json.dumps(result), content_type='application/json')

    
@csrf_exempt
@login_required
def tieba_unbinding(request):
    sites = request.user.userinfo.website_set.all()
    binding_sites = {}
    for site in sites:
        if site.site == 'tieba':
            site.delete()
        else:
            binding_sites[site.site] = site.site_account
    binding_sites = {'binding_sites': binding_sites}
    return render(request, 'closends/setting_user_binding.html', binding_sites)
