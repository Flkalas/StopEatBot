# coding=utf8
def get_api():
    import twitter
    api = twitter.Api(consumer_key='1imnw4fYChDI8eG05lWNHq83E',
                    consumer_secret='LvqTzMlmSsZ3UfzgNG3NEyu14uVHTY7tFH0QEFgxEe1K3d7KCp',
                    access_token_key='1008181687216365568-rpsiVLAhroCtdoZH6krcjXUionJteF',
                    access_token_secret='s5an4leYr5Gj8PujXitfgBEh5rzKn8sgmxMjicHOTYMJt')
    return api

def follow_and_guide(api, user_id):
    api.CreateFriendship(user_id)
    api.PostUpdate(get_guide_phrase(api.GetUser(user_id)), media='https://pbs.twimg.com/media/Df5h_yzVAAAd4Jl.jpg')

def sync_friend_follower(api):
    followers_ids = api.GetFollowerIDs()
    friends_ids = api.GetFriendIDs()

    not_following = list(set(followers_ids) - set(friends_ids))
    not_following_result = [follow_and_guide(api, user_id) for user_id in not_following]

    not_follower = list(set(friends_ids) - set(followers_ids))
    not_follower_result = [api.DestroyFriendship(user_id) for user_id in not_follower]

    return not_following_result, not_follower_result

def get_now_kst():
    import datetime
    import pytz
    return datetime.datetime.now(pytz.timezone('Asia/Seoul'))

def get_guide_phrase(user):
    return "{3} {2}님! @stopeatbot 으로 가셔서 모바일 알람을 등록해주세요! 시간마다 모바일로 알람이 갈거에요!".format( user.name, '@'+user.screen_name)

def get_phrase():
    now = get_now_kst()
    phrase = "{0}시입니다. 자기 전 6시간 내에 먹으면 소화가 잘 되지 않고 살이 찔 수 있어요! 지금 먹으면 {1}시 넘어서 자야하니 먹지마세요!".format(now.hour-12, (now.hour-6)%12)
    return phrase

def send_notification(api):
    api.PostUpdate(get_phrase())

def check_and_send():
    now = get_now_kst()
    if now.hour > 19 or now.hour < 2:
        print(now)
        api = get_api()
        sync_friend_follower(api)
        send_notification(api)

if __name__ == "__main__":
    import apscheduler.schedulers.blocking
    import time
    scheduler = apscheduler.schedulers.blocking.BlockingScheduler()
    scheduler.add_job(check_and_send, 'cron', hour='20-23,0-1')
    scheduler.start()
