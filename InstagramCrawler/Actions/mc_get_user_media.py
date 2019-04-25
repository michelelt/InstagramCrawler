#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 17:52:07 2019

@author: mc
"""

from InstagramAPI import InstagramAPI
from mc_get_all_comments import get_all_comments
import time
from threading import Thread
import json

import datetime
import os
from pytz import reference
from read_credential import credential
import sys



def get_media_likers(API, media_id,  media_likers):
    API.getMediaLikers(media_id)
    if len(API.LastJson) > 0:
        media_likers[media_id] = API.LastJson['users']
    else: media_likers[media_id] = []
    
    return API.LastJson


'''
# =============================================================================
# download all the images pulished on the user's priofile
# =============================================================================
'''

from make_dir import make_dir
#make_dir('..')

try: party = sys.argv[1]
except IndexError: party = 'LEGA'


crd = credential(party)
api = InstagramAPI(crd[0], crd[1])
api.login()
username_id = api.username_id


# =============================================================================
# download followers
# =============================================================================
followers = []
next_max_id = True
while next_max_id:

    # first iteration hack
    if next_max_id is True:
        next_max_id = ''

    _ = api.getUserFollowers(username_id, maxid=next_max_id)
    followers.extend(api.LastJson.get('users', []))
    next_max_id = api.LastJson.get('next_max_id', '')


# =============================================================================
# download following
# =============================================================================
api.getSelfUsersFollowing()
followings = api.LastJson['users']



# =============================================================================
# download media, comments and likes
# =============================================================================
#api.getSelfUserFeed()
medias = api.getTotalUserFeed(username_id)
ids = []
comments_dict = {}
media_likers = {}
total_comments = 0

for media in medias:
    ids.append(media['id'])
    total_comments += media['comment_count']
        
    
init_dl_comment = time.time()

threads = [None] * len(ids)
comments_dict  = {}
for i in range(len(ids)):
    print(i)

    threads[i] = Thread(target=get_all_comments, 
           args=(
            api, 
            ids[i], 
            '2000-01-01', 
            total_comments, 
            True, 
            '',
            comments_dict)
    )
    threads[i].start()
    
for i in range(len(ids)):
    threads[i].join()


threads_likers = [None] * len(ids)
for i in range(len(ids)):
    threads_likers[i] = Thread(target=get_media_likers,
                  args=(api,
                        ids[i],
                        media_likers
                         )
                  
                  )
    threads_likers[i].start()
    
for i in range(len(ids)):
    threads_likers[i].join()    

    
final_dl_comment =  (time.time()-init_dl_comment)/60
print('%d comment downloaded in %d  minute(s)'%(total_comments, final_dl_comment))



# =============================================================================
# save the scraped data
# =============================================================================

'''save the medias'''
#create the timestamp
localtime = reference.LocalTimezone()
now = datetime.datetime.today().strftime('%Y-%m-%dT%H-%m-%S')

#save the media
media_pt = open('../INSTAGRAM/%s/User/medias/%s.jsonl'%(party,now), 'w')
for media in medias:
    str_print = json.dumps(media)
    media_pt.write(str_print+'\n')
media_pt.close()

'''save comments for each  media'''
for media_id in ids:
    comments_pt = open('../INSTAGRAM/%s/User/comments/%s-%s.jsonl'%(party,now, media_id), 'w')
    for comments in comments_dict[media_id]:
        comments_pt.write(json.dumps(comments)+'\n')
    comments_pt.close()
    

followers_pt = open('../INSTAGRAM/%s/User/followers/%s.jsonl'%(party,now), 'w')
for follower in followers:
    str_print = json.dumps(follower)
    followers_pt.write(str_print + '\n')
followers_pt.close()
    

following_pt = open('../INSTAGRAM/%s/User/followings/%s.jsonl'%(party,now), 'w')
for following in followings:
    str_print = json.dumps(following)
    following_pt.write(str_print + '\n')
following_pt.close()


for media_id in media_likers.keys():
    media_likers_pt = open('../INSTAGRAM/%s/User/media_likers/%s-%s.jsonl'%(party,now, media_id), 'w')
    for user in media_likers[media_id]:
        str_print = json.dumps(user)
        media_likers_pt.write(str_print + '\n')
    media_likers_pt.close()



## =============================================================================
## delete dwnloaded info
## =============================================================================
#myCmd = 'rm -r ../INSTAGRAM/%s/User' % 'LEGA'
#os.system(myCmd)
#make_dir('..')            





