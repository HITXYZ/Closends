from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType

import time
from libsvm.svmutil import *
from celery.task import task
from celery.task import periodic_task
from celery.schedules import crontab
from closends.svm.svm import Preprocess, topic_name
from closends.spider.weibo_spider import WeiboSpider
from closends.spider.zhihu_spider import ZhihuSpider
from closends.spider.tieba_spider import TiebaSpider
from closends.models import Friend, WeiboContent, ZhihuContent, TiebaContent, Image, User

time_1 = time.time()
time_2 = time.mktime(time.strptime('2017-12-2 12:00:00', '%Y-%m-%d %H:%M:%S'))


@periodic_task(run_every=(crontab(minute='*/1')), name="weibo_spider")
def weibo_spider():
    spider = WeiboSpider()
    lab = Preprocess('', 1000)
    svm_model = svm_load_model(settings.BASE_DIR + '/closends/svm/svm.model')
    friends = Friend.objects.all().exclude(weibo_account='')
    for friend in friends:
        weibos = spider.scrape_user_weibo(int(friend.weibo_ID), before=time_1, after=time_2, number=1000)
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


@periodic_task(run_every=(crontab(minute='*/1')), name="zhihu_spider")
def zhihu_spider():
    spider = ZhihuSpider()
    lab = Preprocess('', 1000)
    svm_model = svm_load_model(settings.BASE_DIR + '/closends/svm/svm.model')
    friends = Friend.objects.all().exclude(zhihu_account='')
    for friend in friends:
        zhihus = spider.scrape_user_activities(friend.zhihu_ID, before=time_1, after=time_2, number=1000)
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


@periodic_task(run_every=(crontab(minute='*/1')), name="tieba_spider")
def tieba_spider():
    spider = TiebaSpider()
    lab = Preprocess('', 1000)
    svm_model = svm_load_model(settings.BASE_DIR + '/closends/svm/svm.model')
    friends = Friend.objects.all().exclude(tieba_account='')
    for friend in friends:
        tiebas = spider.scrape_user_posts(friend.tieba_ID, before=time_1, after=time_2, number=1000)
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


@task(name="weibo_spider_friend")
def weibo_spider_friend(friend):
    spider = WeiboSpider()
    lab = Preprocess('', 1000)
    svm_model = svm_load_model(settings.BASE_DIR + '/closends/svm/svm.model')
    weibos = spider.scrape_user_weibo(int(friend['weibo_ID']), before=time_1, after=time_2, number=1000)
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


@task(name="zhihu_spider_friend")
def zhihu_spider_friend(friend):
    spider = ZhihuSpider()
    lab = Preprocess('', 1000)
    svm_model = svm_load_model(settings.BASE_DIR + '/closends/svm/svm.model')
    zhihus = spider.scrape_user_activities(friend['zhihu_ID'], before=time_1, after=time_2, number=1000)
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


@task(name="tieba_spider_friend")
def tieba_spider_friend(friend):
    spider = TiebaSpider()
    lab = Preprocess('', 1000)
    svm_model = svm_load_model(settings.BASE_DIR + '/closends/svm/svm.model')
    tiebas = spider.scrape_user_posts(friend['tieba_ID'], before=time_1, after=time_2, number=1000)
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

    # all_contents.sort(key= lambda content: content.pub_date)
    paginator = Paginator(all_contents, 20)
    cache.set(username + '_paginator', paginator, 5 * 60)


@task(name="cache_query_platform")
def cached_query_platform(username, platform):
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

    # all_contents.sort(key=lambda content: content.pub_date)
    paginator = Paginator(all_contents, 20)
    cache.set(username + '_' + platform + '_paginator', paginator, 5 * 60)


@task(name="cache_query_group")
def cached_query_group(username, group):
    user = User.objects.get(username=username).userinfo
    friends = user.friend_set.all()
    group_list = user.group_list.split(',')

    all_contents = []
    for friend in friends:
        if friend.group == group_list[int(group)]:
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

    # all_contents.sort(key=lambda content: content.pub_date)
    paginator = Paginator(all_contents, 20)
    cache.set(username + '_' + group + '_paginator', paginator, 5 * 60)


@task(name="cache_query_topic")
def cached_query_topic(username, topic):
    user = User.objects.get(username=username).userinfo
    friends = user.friend_set.all()

    all_contents = []
    for friend in friends:
        weibo_contents = [content for content in friend.weibocontent_set.all() if content.topic == topic_name[int(topic)]]
        zhihu_contents = [content for content in friend.zhihucontent_set.all() if content.topic == topic_name[int(topic)]]
        tieba_contents = [content for content in friend.tiebacontent_set.all() if content.topic == topic_name[int(topic)]]
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

    # all_contents.sort(key=lambda content: content.pub_date)
    paginator = Paginator(all_contents, 20)
    cache.set(username + '_' + topic + '_paginator', paginator, 5 * 60)
