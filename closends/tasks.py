from celery.task import task
from celery.task import periodic_task
from celery.schedules import crontab
from closends.spider.weibo_spider import WeiboSpider
from closends.spider.zhihu_spider import ZhihuSpider
from closends.spider.tieba_spider import TiebaSpider
from .models import Friend, WeiboContent, ZhihuContent, TiebaContent, Image


@periodic_task(run_every=(crontab(minute='*/1')), name="weibo_spider")
def weibo_spider():
    friends = Friend.objects.all().exclude(weibo_account='')
    spider = WeiboSpider()
    for friend in friends:
        weibos = spider.scrape_user_weibo(int(friend.weibo_ID), 20)
        for weibo in weibos:
            weibo = weibo.convert_format()
            if len(weibo) == 6:  # original weibo
                has_image = len(weibo['images']) > 0
                content = WeiboContent(pub_date     = weibo['pub_date'],
                                       src_url      = weibo['src_url'],
                                       content      = weibo['content'],
                                       is_repost    = weibo['is_repost'],
                                       has_image    = has_image,
                                       video_image  = weibo['video_image'],
                                       friend_id    = friend.id)
                content.save()
                if has_image:
                    for image_url in weibo['images']:
                        Image(content_object=content, image_url=image_url).save()
            else:               # reposted weibo
                has_image = len(weibo['origin_images']) > 0
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
                                       friend_id        = friend.id)
                content.save()
                if has_image:
                    for image_url in weibo['origin_images']:
                        Image(content_object=content, image_url=image_url).save()


@periodic_task(run_every=(crontab(minute='*/1')), name="zhihu_spider")
def zhihu_spider():
    friends = Friend.objects.all().exclude(zhihu_account='')
    spider = ZhihuSpider()
    for friend in friends:
        zhihus = spider.scrape_user_activities(friend.zhihu_ID)
        for zhihu in zhihus:
            zhihu = zhihu.convert_format()
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
                                   friend_id           = friend.id)
            if zhihu['cover_image']:
                content.cover_image = zhihu['cover_image']
            content.save()


@periodic_task(run_every=(crontab(minute='*/1')), name="tieba_spider")
def tieba_spider():
    friends = Friend.objects.all().exclude(tieba_account='')
    spider = TiebaSpider()
    for friend in friends:
        tiebas = spider.scrape_user_posts(friend.tieba_ID)
        for tieba in tiebas:
            tieba = tieba.convert_format()
            content = TiebaContent(pub_date     = tieba['pub_date'],
                                   forum        = tieba['forum'],
                                   forum_url    = tieba['forum_url'],
                                   title        = tieba['title'],
                                   title_url    = tieba['title_url'],
                                   content      = tieba['content'],
                                   content_url  = tieba['content_url'],
                                   friend_id    = friend.id)
            content.save()


@task(name="weibo_spider_friend")
def weibo_spider_friend(friend):
    spider = WeiboSpider()
    weibos = spider.scrape_user_weibo(int(friend['weibo_ID']), 20)
    for weibo in weibos:
        weibo = weibo.convert_format()
        if len(weibo) == 6:
            has_image = len(weibo['images']) > 0
            content = WeiboContent(pub_date     = weibo['pub_date'],
                                   src_url      = weibo['src_url'],
                                   content      = weibo['content'],
                                   is_repost    = weibo['is_repost'],
                                   has_image    = has_image,
                                   video_image  = weibo['video_image'],
                                   friend_id    = friend['id'])
            content.save()
            if has_image:
                for image_url in weibo['images']:
                    Image(content_object=content, image_url=image_url).save()
        else:
            has_image = len(weibo['origin_images']) > 0
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
                                   friend_id        = friend['id'])
            content.save()
            if has_image:
                for image_url in weibo['origin_images']:
                    Image(content_object=content, image_url=image_url).save()


@task(name="zhihu_spider_friend")
def zhihu_spider_friend(friend):
    spider = ZhihuSpider()
    zhihus = spider.scrape_user_activities(friend['zhihu_ID'])
    for zhihu in zhihus:
        zhihu = zhihu.convert_format()
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
                               friend_id            = friend['id'])
        if zhihu['cover_image']:
            content.cover_image = zhihu['cover_image']
        content.save()


@task(name="tieba_spider_friend")
def tieba_spider_friend(friend):
    spider = TiebaSpider()
    tiebas = spider.scrape_user_posts(friend['tieba_ID'])
    for tieba in tiebas:
        tieba = tieba.convert_format()
        content = TiebaContent(pub_date     =tieba['pub_date'],
                               forum        =tieba['forum'],
                               forum_url    =tieba['forum_url'],
                               title        =tieba['title'],
                               title_url    =tieba['title_url'],
                               content      =tieba['content'],
                               content_url  =tieba['content_url'],
                               friend_id    =friend['id'])
        content.save()