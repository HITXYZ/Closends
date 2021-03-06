from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType

import time
import codecs
from libsvm.svmutil import *
from celery.task import task
from celery.task import periodic_task
from celery.schedules import crontab
from datetime import datetime, timedelta
from closends.svm.svm import Preprocess, topic_name
from closends.spider.weibo_spider import WeiboSpider
from closends.spider.zhihu_spider import ZhihuSpider
from closends.spider.tieba_spider import TiebaSpider
from closends.models import Friend, WeiboContent, ZhihuContent, TiebaContent, Image, User


delta_days = 7
scrape_num = 1000


@periodic_task(run_every=(crontab(minute='*/5')), name="weibo_spider")
def weibo_spider():
    spider = WeiboSpider()
    lab = Preprocess('', 1000)
    svm_model = svm_load_model(settings.BASE_DIR + '/closends/svm/svm.model')
    friends = Friend.objects.all().exclude(weibo_account='')
    updating_list = cache.get('weibo_updating_list', set())

    update_num = 0
    for friend in friends:
        if friend.id in updating_list: continue

        try:
            start_time = friend.weibocontent_set.latest('pub_date').pub_date + timedelta(seconds=1)
            start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        except:
            start_time = datetime.now() + timedelta(days=-delta_days)
            start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        time_2 = time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))
        time_1 = time.time()

        try:
            weibos = spider.scrape_user_weibo(int(friend.weibo_ID), before=time_1, after=time_2, number=scrape_num)
        except:
            with codecs.open('weibo_spider_error.txt', 'a', encoding='utf8') as fw:
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                time_1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_1))
                time_2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_2))
                fw.write(current_time + '\t' + friend.nickname + '\t' + friend.weibo_ID + '\t' + str(time_1) + '\t' + str(time_2)+'\n')
            continue
        update_num += len(weibos)

        for weibo in weibos:
            weibo = weibo.convert_format()
            try:
                if len(weibo) == 6:  # original weibo
                    has_image = len(weibo['images']) > 0
                    vector = lab.text_preprocess(weibo['content'])
                    p_label, _, _ = svm_predict([0,], [vector,], svm_model)
                    content = WeiboContent(pub_date     = weibo['pub_date'],
                                           src_url      = weibo['src_url'],
                                           content      = weibo['content'],
                                           is_repost    = weibo['is_repost'],
                                           has_image    = has_image,
                                           video_image  = weibo['video_image'],
                                           topic        = topic_name[int(p_label[0])-1],
                                           friend_id    = friend.id)
                    content.save()
                    if has_image:
                        for image_url in weibo['images']:
                            Image(content_object=content, image_url=image_url).save()
                else:               # reposted weibo
                    has_image = len(weibo['origin_images']) > 0
                    vector = lab.text_preprocess(weibo['content'])
                    p_label, _, _ = svm_predict([0, ], [vector, ], svm_model)
                    content = WeiboContent(pub_date         = weibo['pub_date'],
                                           src_url          = weibo['src_url'],
                                           content          = weibo['content'],
                                           is_repost        = weibo['is_repost'],
                                           has_image        = False,
                                           video_image      = weibo['video_image'],
                                           origin_account   = weibo['origin_account'],
                                           origin_link      = weibo['origin_link'],
                                           origin_pub_date  = weibo['origin_pub_date'],
                                           origin_src_url   = weibo['origin_src_url'],
                                           origin_content   = weibo['origin_content'],
                                           origin_has_image = has_image,
                                           origin_video_image=weibo['origin_video_image'],
                                           topic            = topic_name[int(p_label[0]) - 1],
                                           friend_id        = friend.id)
                    content.save()
                    if has_image:
                        for image_url in weibo['origin_images']:
                            Image(content_object=content, image_url=image_url).save()
            except: pass

    print("爬取完毕, 微博更新了" + str(update_num) + '条动态!')


@periodic_task(run_every=(crontab(minute='*/5')), name="zhihu_spider")
def zhihu_spider():
    spider = ZhihuSpider()
    lab = Preprocess('', 1000)
    svm_model = svm_load_model(settings.BASE_DIR + '/closends/svm/svm.model')
    friends = Friend.objects.all().exclude(zhihu_account='')
    updating_list = cache.get_or_set('zhihu_updating_list', set())

    update_num = 0
    for friend in friends:
        if friend.id in updating_list: continue

        try:
            start_time = friend.zhihucontent_set.latest('pub_date').pub_date + timedelta(seconds=1)
            start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        except:
            start_time = datetime.now() + timedelta(days=-delta_days)
            start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        time_2 = time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))
        time_1 = time.time()

        try:
            zhihus = spider.scrape_user_activities(friend.zhihu_ID, before=time_1, after=time_2, number=scrape_num)
        except:
            with codecs.open('zhihu_spider_error.txt', 'a', encoding='utf8') as fw:
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                time_1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_1))
                time_2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_2))
                fw.write(current_time + '\t' + friend.nickname + '\t' + friend.zhihu_ID + '\t' + str(time_1) + '\t' + str(time_2)+'\n')
            continue
        update_num += len(zhihus)

        for zhihu in zhihus:
            zhihu = zhihu.convert_format()
            try:
                vector = lab.text_preprocess(zhihu['target_content'])
                p_label, _, _ = svm_predict([0, ], [vector, ], svm_model)
                content = ZhihuContent(pub_date            = zhihu['pub_date'],
                                       action_type         = zhihu['action_type'],
                                       target_user_name    = zhihu['target_user_name'],
                                       target_user_head    = zhihu['target_user_head'],
                                       target_user_url     = zhihu['target_user_url'],
                                       target_user_headline= zhihu['target_user_headline'],
                                       target_title        = zhihu['target_title'],
                                       target_title_url    = zhihu['target_title_url'],
                                       target_content      = zhihu['target_content'],
                                       target_content_url  = zhihu['target_content_url'],
                                       topic               = topic_name[int(p_label[0]) - 1],
                                       friend_id           = friend.id)
                if zhihu['cover_image']:
                    content.cover_image = zhihu['cover_image']
                content.save()
            except: pass

    print("爬取完毕, 知乎更新了" + str(update_num) + '条动态!')


@periodic_task(run_every=(crontab(minute='*/5')), name="tieba_spider")
def tieba_spider():
    spider = TiebaSpider()
    lab = Preprocess('', 1000)
    svm_model = svm_load_model(settings.BASE_DIR + '/closends/svm/svm.model')
    friends = Friend.objects.all().exclude(tieba_account='')
    updating_list = cache.get_or_set('tieba_updating_list', set())

    update_num = 0
    for friend in friends:
        if friend.id in updating_list: continue

        try:
            start_time = friend.tiebacontent_set.latest('pub_date').pub_date + timedelta(seconds=1)
            start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        except:
            start_time = datetime.now() + timedelta(days=-delta_days)
            start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        time_2 = time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))
        time_1 = time.time()

        try:
            tiebas = spider.scrape_user_posts(friend.tieba_ID, before=time_1, after=time_2, number=scrape_num)
        except:
            with codecs.open('tieba_spider_error.txt', 'a', encoding='utf8') as fw:
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                time_1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_1))
                time_2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_2))
                fw.write(current_time + '\t' + friend.nickname + '\t' + friend.tieba_ID + '\t' + str(time_1) + '\t' + str(time_2)+'\n')
            continue

        update_num += len(tiebas)
        for tieba in tiebas:
            tieba = tieba.convert_format()
            try:
                vector = lab.text_preprocess(tieba['content'])
                p_label, _, _ = svm_predict([0, ], [vector, ], svm_model)
                content = TiebaContent(pub_date     = tieba['pub_date'],
                                       forum        = tieba['forum'],
                                       forum_url    = tieba['forum_url'],
                                       title        = tieba['title'],
                                       title_url    = tieba['title_url'],
                                       content      = tieba['content'],
                                       content_url  = tieba['content_url'],
                                       topic        = topic_name[int(p_label[0]) - 1],
                                       friend_id    = friend.id)
                content.save()
            except: pass

    print("爬取完毕, 贴吧更新了" + str(update_num) + '条动态!')


@task(name="weibo_spider_friend")
def weibo_spider_friend(username, friend):
    spider = WeiboSpider()
    lab = Preprocess('', 1000)
    svm_model = svm_load_model(settings.BASE_DIR + '/closends/svm/svm.model')
    start_time = datetime.now() + timedelta(days=-delta_days)
    start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
    time_2 = time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))
    time_1 = time.time()

    try:
        weibos = spider.scrape_user_weibo(int(friend['weibo_ID']), before=time_1, after=time_2, number=scrape_num)
    except:
        with codecs.open('weibo_spider_error.txt', 'a', encoding='utf8') as fw:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            time_1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_1))
            time_2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_2))
            fw.write(current_time + '\t' + username + '\t' + friend['weibo_ID'] + '\t' + str(time_1) + '\t' + str(time_2)+'\n')
        return

    for weibo in weibos:
        weibo = weibo.convert_format()
        try:
            if len(weibo) == 6:
                has_image = len(weibo['images']) > 0
                vector = lab.text_preprocess(weibo['content'])
                p_label, _, _ = svm_predict([0, ], [vector, ], svm_model)
                content = WeiboContent(pub_date     = weibo['pub_date'],
                                       src_url      = weibo['src_url'],
                                       content      = weibo['content'],
                                       is_repost    = weibo['is_repost'],
                                       has_image    = has_image,
                                       video_image  = weibo['video_image'],
                                       topic        = topic_name[int(p_label[0]) - 1],
                                       friend_id    = friend['id'])
                content.save()
                if has_image:
                    for image_url in weibo['images']:
                        Image(content_object=content, image_url=image_url).save()
            else:
                has_image = len(weibo['origin_images']) > 0
                vector = lab.text_preprocess(weibo['content'])
                p_label, _, _ = svm_predict([0, ], [vector, ], svm_model)
                content = WeiboContent(pub_date         = weibo['pub_date'],
                                       src_url          = weibo['src_url'],
                                       content          = weibo['content'],
                                       is_repost        = weibo['is_repost'],
                                       has_image        = False,
                                       video_image      = weibo['video_image'],
                                       origin_account   = weibo['origin_account'],
                                       origin_link      = weibo['origin_link'],
                                       origin_pub_date  = weibo['origin_pub_date'],
                                       origin_src_url   = weibo['origin_src_url'],
                                       origin_content   = weibo['origin_content'],
                                       origin_has_image = has_image,
                                       origin_video_image=weibo['origin_video_image'],
                                       topic            = topic_name[int(p_label[0]) - 1],
                                       friend_id        = friend['id'])
                content.save()
                if has_image:
                    for image_url in weibo['origin_images']:
                        Image(content_object=content, image_url=image_url).save()
        except: pass

    updating_list = cache.get('weibo_updating_list')
    updating_list.remove(friend['id'])
    cache.set('weibo_updating_list', updating_list, None)
    
    updated_list = cache.get_or_set('updated_list', set())
    updated_list.add(username)
    cache.set('updated_list', updated_list, 5*60)

    print("爬取完毕, 微博初次抓取了" + str(len(weibos)) + '条动态!')


@task(name="zhihu_spider_friend")
def zhihu_spider_friend(username, friend):
    spider = ZhihuSpider()
    lab = Preprocess('', 1000)
    svm_model = svm_load_model(settings.BASE_DIR + '/closends/svm/svm.model')
    start_time = datetime.now() + timedelta(days=-delta_days)
    start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
    time_2 = time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))
    time_1 = time.time()

    try:
        zhihus = spider.scrape_user_activities(friend['zhihu_ID'], before=time_1, after=time_2, number=scrape_num)
    except:
        with codecs.open('zhihu_spider_error.txt', 'a', encoding='utf8') as fw:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            time_1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_1))
            time_2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_2))
            fw.write(current_time + '\t' + username + '\t' + friend['zhihu_ID'] + '\t' + str(time_1) + '\t' + str(time_2)+'\n')
        return

    for zhihu in zhihus:
        zhihu = zhihu.convert_format()
        try:
            vector = lab.text_preprocess(zhihu['target_content'])
            p_label, _, _ = svm_predict([0, ], [vector, ], svm_model)
            content = ZhihuContent(pub_date             = zhihu['pub_date'],
                                   action_type          = zhihu['action_type'],
                                   target_user_name     = zhihu['target_user_name'],
                                   target_user_head     = zhihu['target_user_head'],
                                   target_user_url      = zhihu['target_user_url'],
                                   target_user_headline = zhihu['target_user_headline'],
                                   target_title         = zhihu['target_title'],
                                   target_title_url     = zhihu['target_title_url'],
                                   target_content       = zhihu['target_content'],
                                   target_content_url   = zhihu['target_content_url'],
                                   topic                = topic_name[int(p_label[0]) - 1],
                                   friend_id            = friend['id'])
            if zhihu['cover_image']:
                content.cover_image = zhihu['cover_image']
            content.save()
        except: pass

    updating_list = cache.get('zhihu_updating_list')
    updating_list.remove(friend['id'])
    cache.set('zhihu_updating_list', updating_list, None)

    updated_list = cache.get_or_set('updated_list', set())
    updated_list.add(username)
    cache.set('updated_list', updated_list, 5*60)

    print("爬取完毕, 知乎初次抓取了" + str(len(zhihus)) + '条动态!')


@task(name="tieba_spider_friend")
def tieba_spider_friend(username, friend):
    spider = TiebaSpider()
    lab = Preprocess('', 1000)
    svm_model = svm_load_model(settings.BASE_DIR + '/closends/svm/svm.model')
    start_time = datetime.now() + timedelta(days=-delta_days)
    start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
    time_2 = time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))
    time_1 = time.time()

    try:
        tiebas = spider.scrape_user_posts(friend['tieba_ID'], before=time_1, after=time_2, number=scrape_num)
    except:
        with codecs.open('tieba_spider_error.txt', 'a', encoding='utf8') as fw:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            time_1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_1))
            time_2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_2))
            fw.write(current_time + '\t' + username + '\t' + friend['tieba_ID'] + '\t' + str(time_1) + '\t' + str(time_2)+'\n')
        return

    for tieba in tiebas:
        tieba = tieba.convert_format()
        try:
            vector = lab.text_preprocess(tieba['content'])
            p_label, _, _ = svm_predict([0, ], [vector, ], svm_model)
            content = TiebaContent(pub_date     = tieba['pub_date'],
                                   forum        = tieba['forum'],
                                   forum_url    = tieba['forum_url'],
                                   title        = tieba['title'],
                                   title_url    = tieba['title_url'],
                                   content      = tieba['content'],
                                   content_url  = tieba['content_url'],
                                   topic        = topic_name[int(p_label[0]) - 1],
                                   friend_id    = friend['id'])
            content.save()
        except: pass

    updating_list = cache.get('tieba_updating_list')
    updating_list.remove(friend['id'])
    cache.set('tieba_updating_list', updating_list, None)
    
    updated_list = cache.get_or_set('updated_list', set())
    updated_list.add(username)
    cache.set('updated_list', updated_list, 5*60)

    print("爬取完毕, 贴吧初次抓取了" + str(len(tiebas)) + '条动态!')


@task(name="cache_query_all")
def cached_query_all(username):
    user = User.objects.get(username=username).userinfo
    friends = user.friend_set.all()

    all_contents = []
    for friend in friends:
        weibo_contents = friend.weibocontent_set.all()
        zhihu_contents = friend.zhihucontent_set.all()
        tieba_contents = friend.tiebacontent_set.all()
        content_type = ContentType.objects.get_for_model(WeiboContent)
        for content in weibo_contents:
            if not content.is_repost:
                if content.has_image:
                    content.images = Image.objects.filter(content_type=content_type, object_id=content.id)
            else:
                if content.origin_has_image:
                    content.origin_images = Image.objects.filter(content_type=content_type, object_id=content.id)

        all_contents += weibo_contents
        all_contents += zhihu_contents
        all_contents += tieba_contents

    all_contents.sort(key=lambda content: content.pub_date, reverse=True)
    paginator = Paginator(all_contents, 20)
    cache.set(username + '_paginator', paginator, 5 * 60)


@task(name="cache_query_platform")
def cached_query_platform(username, platform):
    print("caching " + username + " " +platform)

    user = User.objects.get(username=username).userinfo
    friends = user.friend_set.all()

    all_contents = []
    if platform == 'weibo':
        for friend in friends:
            all_contents += friend.weibocontent_set.all()
        content_type = ContentType.objects.get_for_model(WeiboContent)
        for content in all_contents:
            if not content.is_repost:
                if content.has_image:
                    content.images = Image.objects.filter(content_type=content_type, object_id=content.id)
            else:
                if content.origin_has_image:
                    content.origin_images = Image.objects.filter(content_type=content_type, object_id=content.id)
    elif platform == 'zhihu':
        for friend in friends:
            all_contents += friend.zhihucontent_set.all()
    elif platform == 'tieba':
        for friend in friends:
            all_contents += friend.tiebacontent_set.all()

    all_contents.sort(key=lambda content: content.pub_date, reverse=True)
    paginator = Paginator(all_contents, 20)
    cache.set(username + '_' + platform + '_paginator', paginator, 5 * 60)


@task(name="cache_query_group")
def cached_query_group(username, group_name):
    print("caching " + username + " " + group_name)

    user = User.objects.get(username=username).userinfo
    friends = user.friend_set.all()

    all_contents = []
    for friend in friends:
        if friend.group == group_name:
            weibo_contents = friend.weibocontent_set.all()
            zhihu_contents = friend.zhihucontent_set.all()
            tieba_contents = friend.tiebacontent_set.all()
            content_type = ContentType.objects.get_for_model(WeiboContent)
            for content in weibo_contents:
                if not content.is_repost:
                    if content.has_image:
                        content.images = Image.objects.filter(content_type=content_type, object_id=content.id)
                else:
                    if content.origin_has_image:
                        content.origin_images = Image.objects.filter(content_type=content_type, object_id=content.id)

            all_contents += weibo_contents
            all_contents += zhihu_contents
            all_contents += tieba_contents

    all_contents.sort(key=lambda content: content.pub_date, reverse=True)
    paginator = Paginator(all_contents, 20)
    cache.set(username + '_' + group_name + '_paginator', paginator, 5 * 60)


@task(name="cache_query_topic")
def cached_query_topic(username, topic):
    print("caching "+ username + " " + topic)

    user = User.objects.get(username=username).userinfo
    friends = user.friend_set.all()

    all_contents = []
    for friend in friends:
        weibo_contents = [content for content in friend.weibocontent_set.all() if content.topic == topic]
        zhihu_contents = [content for content in friend.zhihucontent_set.all() if content.topic == topic]
        tieba_contents = [content for content in friend.tiebacontent_set.all() if content.topic == topic]
        content_type = ContentType.objects.get_for_model(WeiboContent)
        for content in weibo_contents:
            if not content.is_repost:
                if content.has_image:
                    content.images = Image.objects.filter(content_type=content_type, object_id=content.id)
            else:
                if content.origin_has_image:
                    content.origin_images = Image.objects.filter(content_type=content_type, object_id=content.id)
        all_contents += weibo_contents
        all_contents += zhihu_contents
        all_contents += tieba_contents

    all_contents.sort(key=lambda content: content.pub_date, reverse=True)
    paginator = Paginator(all_contents, 20)
    cache.set(username + '_' + topic + '_paginator', paginator, 5 * 60)


@task(name="update_all_cache")
def update_all_cache(keys):
    for key in keys:
        if key.count('_') == 1:
            cached_query_all(key.split('_')[0])
        elif key.split('_')[1] in ['weibo', 'zhihu', 'tieba']:
            username, platform, _ = key.split('_')
            cached_query_platform(username, platform)
        elif key.split('_')[1] in topic_name:
            username, topic, _ = key.split('_')
            cached_query_topic(username, topic)
        else:
            username, group, _ = key.split('_')
            cached_query_group(username, group)
