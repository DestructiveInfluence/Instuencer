#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__  = 'QD'
__copyright__   = 'Copyright (C) 2016 QD'
__version__     = '0.2'
__email__   = 'QD@dstrctv.io'
__github__  = 'http://github.com/DestructiveInfluence/Instuencer'
__python__    = '2.7'
__credit__  = 'https://github.com/LevPasha/instabot.py'

import requests
import random
import time
import datetime
import logging
import json
import itertools

# Fill in these 4 lines below!
username = 'your_username' # what profile do you want to boost?
overwatchUser = 'username0' # bot constantly scanning your feed
loginUser = ['username1','username2','username3'] # bot interacting with your account
loginPassword = 'password123' # password for all of the bots

url = 'https://www.instagram.com/'
url_likes = 'https://www.instagram.com/web/likes/%s/like/'
url_unlike = 'https://www.instagram.com/web/likes/%s/unlike/'
url_comment = 'https://www.instagram.com/web/comments/%s/add/'
url_follow = 'https://www.instagram.com/web/friendships/%s/follow/'
url_unfollow = 'https://www.instagram.com/web/friendships/%s/unfollow/'
url_login = 'https://www.instagram.com/accounts/login/ajax/'
url_logout = 'https://www.instagram.com/accounts/logout/'

user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
accept_language = 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'

error_400 = 0
error_400_to_ban = 3

# Log setting.
log_file_path = ''
log_file = 0
# log_mod 0 to console, 1 to file
log_mod = 0
login_status = False

bot_start = datetime.datetime.now()
now_time = datetime.datetime.now()
time_in_day = 24*60*60

media_id = ''
like_counter = 0

s = requests.Session()
sOverwatch = requests.Session()

def login(user_login):
    global login_status
    s = requests.Session()
    log_string = 'Logging in as %s...' % (user_login)
    write_log(log_string)
    s.cookies.update ({'sessionid' : '', 'mid' : '', 'ig_pr' : '1',
                           'ig_vw' : '1920', 'csrftoken' : '',
                           's_network' : '', 'ds_user_id' : ''})
    login_post = {'username' : user_login,
                       'password' : loginPassword}
    s.headers.update ({'Accept-Encoding' : 'gzip, deflate',
                           'Accept-Language' : accept_language,
                           'Connection' : 'keep-alive',
                           'Content-Length' : '0',
                           'Host' : 'www.instagram.com',
                           'Origin' : 'https://www.instagram.com',
                           'Referer' : 'https://www.instagram.com/',
                           'User-Agent' : user_agent,
                           'X-Instagram-AJAX' : '1',
                           'X-Requested-With' : 'XMLHttpRequest'})
    r = s.get(url)
    s.headers.update({'X-CSRFToken' : r.cookies['csrftoken']})
    time.sleep(5 * random.random())
    login = s.post(url_login, data=login_post,
                        allow_redirects=True)
    s.headers.update({'X-CSRFToken' : login.cookies['csrftoken']})
    csrftoken = login.cookies['csrftoken']
    time.sleep(5 * random.random())

    if login.status_code == 200:
        r = s.get('https://www.instagram.com/')
        finder = r.text.find(user_login)
        if finder != -1:
            login_status = True
            log_string = '%s login success!' % (user_login)
            write_log(log_string)
            return s
        else:
            login_status = False
            write_log('Login error! Check your login data!')
    else:
        write_log('Login error! Connection error!')

def logout():
    global s
    global login_status
    now_time = datetime.datetime.now()
    try:
        logout = s.post(url_logout)
        write_log("Logout success!")
        login_status = False
    except:
        write_log("Logout error!")
    if (login_status):
        logout()
#    exit(0)

def like(media_id):
    global s
    global login_status
    global like_counter

    if (login_status):
        nowurl_likes = url_likes % (media_id)
        try:
            like = s.post(nowurl_likes)
            write_log("Liking media: " + media_id)
            like_counter += 1
        except:
            write_log("Except on like!")
            like = 0
        return like

def comment(media_id, comment_text):
    global s
    global login_status
    if (login_status):
        comment_post = {'comment_text' : comment_text}
        url_comment = url_comment % (media_id)
        try:
            comment = s.post(url_comment, data=comment_post)
            if comment.status_code == 200:
                comments_counter += 1
                log_string = 'Write: "%s". #%i.' % (comment_text, comments_counter)
                write_log(log_string)
            return comment
        except:
            write_log("Except on comment!")
    return False

def follow(user_id):
    global s
    global login_status
    if (login_status):
        url_follow = url_follow % (user_id)
        try:
            follow = s.post(url_follow)
            if follow.status_code == 200:
                follow_counter += 1
                log_string = "Followed: %s #%i." % (user_id, follow_counter)
                write_log(log_string)
            return follow
        except:
            write_log("Except on follow!")
    return False

def unfollow(user_id):
    global s
    global login_status
    if (login_status):
        url_unfollow = url_unfollow % (user_id)
        try:
            unfollow = s.post(url_unfollow)
            if unfollow.status_code == 200:
                unfollow_counter += 1
                log_string = "Unfollow: %s #%i." % (user_id, unfollow_counter)
                write_log(log_string)
            return unfollow
        except:
            write_log("Except on unfollow!")
    return False

def generate_comment():
    c_list = list(itertools.product(
                                ["this", "the", "your"],
                                ["photo", "picture", "pic", "shot", "snapshot"],
                                ["is", "looks", "feels", "is really"],
                                ["great", "super", "good", "very good",
                                "good", "wow", "WOW", "cool",
                                "GREAT", "magnificent", "magical", "very cool",
                                "stylish", "so stylish", "beautiful",
                                "so beautiful", "so stylish", "so professional",
                                "lovely", "so lovely", "very lovely",
                                "glorious", "so glorious", "very glorious",
                                "adorable", "excellent", "amazing"],
                                [".", "..", "...", "!", "!!", "!!!"]))

    repl = [("  ", " "), (" .", "."), (" !", "!")]
    res = " ".join(random.choice(c_list))
    for s, r in repl:
        res = res.replace(s, r)
    return res.capitalize()

def write_log(log_text):
    """ Write log by print() or logger """
    if log_mod == 0:
        try:
            print(log_text)
        except UnicodeEncodeError:
            print("Your text has unicode problem!")
    elif log_mod == 1:
        # Create log_file if not exist.
        if log_file == 0:
            log_file = 1
            now_time = datetime.datetime.now()
            log_full_path = '%s%s_%s.log' % (log_file_path,
                                 user_login,
                                 now_time.strftime("%d.%m.%Y_%H:%M"))
            formatter = logging.Formatter('%(asctime)s - %(name)s '
                        '- %(message)s')
            logger = logging.getLogger(user_login)
            hdrl = logging.FileHandler(log_full_path, mode='w')
            hdrl.setFormatter(formatter)
            logger.setLevel(level=logging.INFO)
            logger.addHandler(hdrl)
        # Log to log file.
        try:
            logger.info(log_text)
        except UnicodeEncodeError:
            print("Your text has unicode problem!")

# gets last media_ID from profile
def getmedia_id():
    try:
        r = sOverwatch.get(url + username)
        text = r.text
        finder_text_start = ('<script type="text/javascript">'
                             'window._sharedData = ')
        finder_text_start_len = len(finder_text_start)-1
        finder_text_end = ';</script>'
        all_data_start = text.find(finder_text_start)
        all_data_end = text.find(finder_text_end, all_data_start + 1)
        json_str = text[(all_data_start + finder_text_start_len + 1) \
                       : all_data_end]
        all_data = json.loads(json_str)
        #media_ids = list(all_data['entry_data']['ProfilePage'][0]['user']['media']['nodes'])
        new_media_id = all_data['entry_data']['ProfilePage'][0]['user']['media']['nodes'][0]['id'] #get media_id
        new_media_id = new_media_id + "_" + all_data['entry_data']['ProfilePage'][0]['user']['media']['nodes'][0]['owner']['id'] #get owner_id
        return new_media_id
    except:
                new_media_id = []
                write_log("Except on get_media!")
                time.sleep(60)
    else:
        return media_id

# handles liking of last image
def like_handler():
    global s
    global media_id

    write_log("[/] Scanning for new media now...")
    # overwatch account constantly scanning your feed, while never interacting with it
    while(True):
        if(media_id <> getmedia_id()):
            time.sleep(40 + (5 * random.random()))
            media_id = getmedia_id()
            write_log("New media posted, ID: " + media_id)
            time.sleep(20 + (5 * random.random()))
            # one cycle = approx 2min (90s + random + login)
            for element in loginUser:
                user_login = element
                s = login(user_login)
                time.sleep(27 + (5 * random.random()))
                like(media_id)
                #time.sleep(10 + (5* random.random())) # uncomment for random comments lol
                #comment(media_id, generate_comment()) # this line too, you fool!
                time.sleep(33 + (5 * random.random()))
                logout()
                write_log("–––––––––––––––––––––––––")
                time.sleep(30 + (5 * random.random()))
            write_log('[/] Cycle completed. Now lurking for new media. Extra Likes: ' + str(like_counter))
        time.sleep(300 + (5 * random.random())) # 5 minute sleep timer, before checking for new media

# Entry point
def main():
    global sOverwatch
    global login_status
    sOverwatch = login(overwatchUser)
    login_status = False
    like_handler()

## -- start of init call --
log_string = '[/\] Instuencer ' + __version__ + ' by QD started at %s:' %\
         (now_time.strftime("%d.%m.%Y %H:%M"))
write_log(log_string)
log_string = '[/\] Users: ' + str(len(loginUser)) + ' for account: ' + username
write_log(log_string)
main()