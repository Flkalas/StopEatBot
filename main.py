# coding=utf8
def get_api():
    import twitter
    api = twitter.Api(consumer_key='1imnw4fYChDI8eG05lWNHq83E',
                    consumer_secret='LvqTzMlmSsZ3UfzgNG3NEyu14uVHTY7tFH0QEFgxEe1K3d7KCp',
                    access_token_key='1008181687216365568-rpsiVLAhroCtdoZH6krcjXUionJteF',
                    access_token_secret='s5an4leYr5Gj8PujXitfgBEh5rzKn8sgmxMjicHOTYMJt')
    return api

def sync_friend_follower(api):
    followers_ids = api.GetFollowerIDs()
    friends_ids = api.GetFriendIDs()

    not_following = list(set(followers_ids) - set(friends_ids))
    not_following_result = [api.CreateFriendship(user_id) for user_id in not_following]

    not_follower = list(set(friends_ids) - set(followers_ids))
    not_follower_result = [api.DestroyFriendship(user_id) for user_id in not_follower]

    return not_following_result, not_follower_result

def get_user_timeline(api, user_id):
    prev_tweet_id = get_prev_tweet_id(user_id)
    statuses = api.GetUserTimeline(user_id = user_id, since_id = prev_tweet_id, count = 200, include_rts = False, trim_user = True)
    return [s.text for s in statuses], max([s.id for s in statuses])

def get_prev_tweet_id(user_id):
    return 8052507480715264

def get_now_kst():
    import datetime
    import pytz
    return datetime.datetime.now(pytz.timezone('Asia/Seoul'))

def get_phrase(user):
    now = get_now_kst()
    phrase = "{3} {2}님! 이제 {0}시입니다. 자기 전 6시간 내에 먹으면 소화가 잘 되지 않고 살이 찔 수 있어요! 지금 먹으면 {1}시 넘어서 자야하니 먹지마세요!".format(now.hour-12, (now.hour-6)%12, user.name, '@'+user.screen_name)
    return phrase

def send_notification(api):
    users = api.GetFollowers()
    for user in users:
        phrase = get_phrase(user)
        api.PostUpdate(phrase)

def check_and_send():
    now = get_now_kst()
    if now.hour > 19 or now.hour < 2:
        print(now)
        api = get_api()
        sync_friend_follower(api)
        send_notification(api)

if __name__ == "__main__":
    import apscheduler.schedulers.background
    import time
    sched = apscheduler.schedulers.background.BackgroundScheduler()
    sched.add_job(check_and_send, 'cron', hour='20-23,0-1')
    sched.start()
    while True:
        time.sleep(1)
