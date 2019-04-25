#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 18:48:52 2019

@author: mc
"""

from InstagramAPI import InstagramAPI
from mc_get_all_comments import get_all_comments
import time
from threading import Thread
import json
from read_credential import credential
import datetime
import os
from pytz import reference

import sys
sys.path.append('../')

'''
# =============================================================================
# download all the info about storiline:
#     medias
#     comments
#     suggested users
#     follow suggested users
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
# get all the TIMELINE post
# =============================================================================
api.timelineFeed()
timeline_feed = api.LastJson
    
    
medias = timeline_feed['items']
downloaded_media = {}
suggested_users = []
ids = []
total_comments=0

for media in medias:
    if 'suggestions' not in media:
        downloaded_media[media['id']]  = media
        ids.append(media['id'])
        try:
             total_comments += media['comment_count']
        except KeyError:
            print('media %s has comment disabled'% media['id'])
            
    else:
        for user in media['suggestions']:
#            api.follow(user['user']['pk'])
            suggested_users.append(user['user'])
        
init_dl_comment = time.time()

threads = [None] * len(ids)
comments_dict  = {}
for i in range(len(ids)):
#for i in range(0,1):

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
    
final_dl_comment =  (time.time()-init_dl_comment)/60
print('%d comment downloaded in %d  minute(s)'%(total_comments, final_dl_comment))


# =============================================================================
# print data on local files
# =============================================================================
'''save media ids downloaded'''
try:
    ids_pt = open('./INSTAGRAM/%s/TimeLineFeed/meida_ids.txt'%party, 'a+')
    for media_id in ids:
        print (media_id)
        ids_pt.write(media_id+'\n')
    ids_pt.close()
    
except FileNotFoundError:
    print('No media id present')
    ids_pt = open('../INSTAGRAM/%s/TimeLineFeed/meida_ids.txt'%party, 'w')
    for media_id in ids:
        print (media_id)
        ids_pt.write(media_id+'\n')
    ids_pt.close()
    
    
'''save the medias'''
#create the timestamp
localtime = reference.LocalTimezone()
now = datetime.datetime.today().strftime('%Y-%m-%dT%H-%m-%S')

#save the media
media_pt = open('../INSTAGRAM/%s/TimeLineFeed/medias/%s.jsonl'%(party,now), 'w')
for media_id in downloaded_media.keys():
    str_print = json.dumps(downloaded_media[media_id])
    media_pt.write(str_print+'\n')
media_pt.close()

'''save comments for each  media'''
for media_id in ids:
    comments_pt = open('../INSTAGRAM/%s/TimeLineFeed/comments/%s-%s.jsonl'%(party,now, media_id), 'w')
    for comments in comments_dict[media_id]:
        comments_pt.write(json.dumps(comments)+'\n')
    comments_pt.close()
    
'''save suggested users'''
suggested_users_pt = open('../INSTAGRAM/%s/TimeLineFeed/suggested_users/%s.jsonl'%(party,now), 'w')
for user in suggested_users:
    suggested_users_pt.write(json.dumps(user)+'\n')
suggested_users_pt.close()
    

# =============================================================================
# move data to HDFS
# =============================================================================
    
    

# =============================================================================
# delete dwnloaded info
# =============================================================================
#myCmd = 'rm -r ../INSTAGRAM/%s/TimeLineFeed' % party
#os.system(myCmd)
#make_dir('..')
#
        
    
