# logging configurations
log_qzone = False  # 是否需要记录空间爬虫日志
log_tieba = False  # 是否需要记录贴吧爬虫日志
log_weibo = False  # 是否需要记录微博爬虫日志
log_zhihu = False  # 是否需要记录知乎爬虫日志
log_path = 'D:\PyCharm\PycharmProjects\SocialMediaScraper\logs'  # 日志文件夹路径

# weibo configurations
weibo_user_profile_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid1}&luicode=10000012&type=uid&value={uid2}'
weibo_user_info_url = 'https://m.weibo.cn/api/container/getIndex?containerid=230283{uid1}_-_INFO' \
                      '&title=%25E5%259F%25BA%25E6%259C%25AC%25E4%25BF%25A1%25E6%2581%25AF&luicode=10000011' \
                      '&lfid=230283{uid2}'
weibo_user_weibo_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid1}' \
                       '&luicode=10000012&containerid=107603{uid2}&page={page}'
weibo_user_follow_url = 'https://m.weibo.cn/api/container/getSecond?containerid=100505{uid}_-_FOLLOWERS&page={page}'
weibo_user_fans_url = 'https://m.weibo.cn/api/container/getSecond?containerid=100505{uid}_-_FANS&page={page}'
weibo_search_url = 'http://s.weibo.com/user/{user}&Refer=weibo_user'

# zhihu configurations
zhihu_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'
}
zhihu_user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
zhihu_follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?' \
                    'include={include}&offset={offset}&limit={limit}'
zhihu_followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?' \
                      'include={include}&offset={offset}&limit={limit}'
zhihu_activity_url = 'https://www.zhihu.com/api/v4/members/{user}/activities?' \
                     'limit={limit}&after_id={after}&desktop=True'
zhihu_question_url = 'https://www.zhihu.com/api/v4/questions/{id}?include={include}'
zhihu_user_questions_url = 'https://www.zhihu.com/api/v4/members/{user}' \
                           '/questions?offset={offset}&limit={limit}'
zhihu_answer_url = 'https://www.zhihu.com/api/v4/answers/{id}?include={include}'
zhihu_user_answers_url = 'https://www.zhihu.com/api/v4/members/{user}' \
                         '/answers?offset={offset}&limit={limit}'
zhihu_question_answers_url = 'https://www.zhihu.com/api/v4/questions/{id}' \
                             '/answers?offset={offset}&limit={limit}'
zhihu_user_query = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,' \
                   'following_count,following_topic_count,following_question_count,following_favlists_count,' \
                   'following_columns_count,answer_count,articles_count,question_count,favorited_count,is_bind_sina,' \
                   'sina_weibo_url,sina_weibo_name,show_sina_weibo,thanked_count,description'
zhihu_follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge'
zhihu_followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge'
zhihu_question_query = 'comment_count,follower_count,visit_count,topics'
zhihu_answer_query = 'voteup_count,comment_count'
zhihu_search_url = 'https://www.zhihu.com/search?type=people&q={key}'

# tieba configurations
tieba_user_profile_url = 'http://tieba.baidu.com/home/main?ie=utf-8&un={user}&fr=itb'
tieba_user_follow_url = 'http://tieba.baidu.com/i/i/concern?u={portrait}&pn={page}'
tieba_user_post_url = 'http://tieba.baidu.com/home/get/getthread?un={user}&pn={page}&ie=utf8'
