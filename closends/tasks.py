from celery.task import task
from celery.task import periodic_task
from celery.schedules import crontab
from closends.spider.weibo_spider import WeiboSpider
from .models import Friend, WeiboContent, Image


@periodic_task(run_every=(crontab(minute='*/5')), name="weibo_spider")
def weibo_spider():
    friends = Friend.objects.all().exclude(weibo_account='')
    spider = WeiboSpider()
    for friend in friends:
        weibos = spider.scrape_weibo(int(friend.weibo_ID), 20)
        for weibo in weibos:
            weibo = weibo.convert_format()
            if len(weibo) == 6:
                has_image = len(weibo['images']) > 0
                content = WeiboContent(pub_date=weibo['pub_date'], src_url=weibo['src_url'], content=weibo['content'],
                                       is_repost=weibo['is_repost'], has_image=has_image,
                                       video_image=weibo['video_image'],
                                       friend_id=friend.id)
                content.save()
                if has_image:
                    for image_url in weibo['images']:
                        Image(content_object=content, image_url=image_url).save()
            else:
                has_image = len(weibo['origin_images']) > 0
                content = WeiboContent(pub_date=weibo['pub_date'], src_url=weibo['src_url'], content=weibo['content'],
                                       is_repost=weibo['is_repost'], has_image=False, video_image=weibo['video_image'],
                                       origin_account=weibo['origin_account'], origin_link=weibo['origin_link'],
                                       origin_pub_date=weibo['origin_pub_date'], origin_src_url=weibo['origin_src_url'],
                                       origin_content=weibo['origin_content'], origin_has_image=has_image,
                                       origin_video_image=weibo['origin_video_image'], friend_id=friend.id)
                content.save()
                if has_image:
                    for image_url in weibo['origin_images']:
                        Image(content_object=content, image_url=image_url).save()


@task(name="weibo_spider_friend")
def weibo_spider_friend(friend):
    spider = WeiboSpider()
    weibos = spider.scrape_weibo(int(friend['weibo_ID']), 20)
    for weibo in weibos:
        weibo = weibo.convert_format()
        if len(weibo) == 6:
            has_image = len(weibo['images']) > 0
            content = WeiboContent(pub_date=weibo['pub_date'], src_url=weibo['src_url'], content=weibo['content'],
                                   is_repost=weibo['is_repost'], has_image=has_image,
                                   video_image=weibo['video_image'],
                                   friend_id=friend['id'])
            content.save()
            if has_image:
                for image_url in weibo['images']:
                    Image(content_object=content, image_url=image_url).save()
        else:
            has_image = len(weibo['origin_images']) > 0
            content = WeiboContent(pub_date=weibo['pub_date'], src_url=weibo['src_url'], content=weibo['content'],
                                   is_repost=weibo['is_repost'], has_image=False, video_image=weibo['video_image'],
                                   origin_account=weibo['origin_account'], origin_link=weibo['origin_link'],
                                   origin_pub_date=weibo['origin_pub_date'], origin_src_url=weibo['origin_src_url'],
                                   origin_content=weibo['origin_content'], origin_has_image=has_image,
                                   origin_video_image=weibo['origin_video_image'], friend_id=friend['id'])
            content.save()
            if has_image:
                for image_url in weibo['origin_images']:
                    Image(content_object=content, image_url=image_url).save()


@periodic_task(run_every=(crontab(minute='*/5')), name="zhihu_spider")
def zhihu_spider():
    pass


@task(name="zhihu_spider_friend")
def zhihu_spider_friend(friend):
    pass