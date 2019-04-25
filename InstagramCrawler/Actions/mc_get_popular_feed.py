#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 16:46:09 2019

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

import sys
from read_credential import credential



'''
# =============================================================================
# get all the post which instagrm suggests
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

api.getPopularFeed()
popular_feed = api.LastJson
api.getPopularFeed()
popular_feed2 = api.LastJson


total_comments = 0
comments = {}
medias  = {}

ids = []

for media in popular_feed['items']:
    if media['id'] not in ids: 
        ids.append(media['id'])
        medias[media['id']] = media
    else: 
        print('present')
        
    try:
        total_comments += media['comment_count']
    except KeyError:
        print('media %s has comment disabled'% media['id'])
        
        
    
for media in popular_feed2['items']:
    if media['id'] not in ids: 
        ids.append(media['id'])
        medias[media['id']] = media
    else: 
        print('present2')
        
    try:
        total_comments += media['comment_count']
    except KeyError:
        print('media %s has comment disabled'% media['id'])
        
        
print('Download %d commets'%total_comments)

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
    time.sleep(5)

for i in range(len(ids)):
    threads[i].join()

final_dl_comment= int((time.time() - init_dl_comment)/60)

print('%d comment downloaded in %d  minute(s)'%(total_comments, final_dl_comment))




# =============================================================================
# save the scraped data
# =============================================================================
'''save media ids downloaded'''
party = 'LEGA'
try:
    ids_pt = open('./INSTAGRAM/%s/PopularFeed/meida_ids.txt'%party, 'a+')
    for media_id in ids:
        print (media_id)
        ids_pt.write(media_id+'\n')
    ids_pt.close()
    
except FileNotFoundError:
    print('No media id present')
    ids_pt = open('../INSTAGRAM/%s/PopularFeed/meida_ids.txt'%party, 'w')
    for media_id in ids:
        print (media_id)
        ids_pt.write(media_id+'\n')
    ids_pt.close()
    
    
'''save the medias'''
#create the timestamp
localtime = reference.LocalTimezone()
now = datetime.datetime.today().strftime('%Y-%m-%dT%H-%m-%S')

#save the media
media_pt = open('../INSTAGRAM/%s/PopularFeed/medias/%s.jsonl'%(party,now), 'w')
for media_id in medias.keys():
    str_print = json.dumps(medias[media_id])
    media_pt.write(str_print+'\n')
media_pt.close()

'''save comments for each  media'''
for media_id in ids:
    comments_pt = open('../INSTAGRAM/%s/PopularFeed/comments/%s-%s.jsonl'%(party,now, media_id), 'w')
    for comments in comments_dict[media_id]:
        comments_pt.write(json.dumps(comments)+'\n')
    comments_pt.close()
    


# =============================================================================
# copy on hdfs
# =============================================================================


# =============================================================================
# remmove data
# =============================================================================
#myCmd = 'rm -r ../INSTAGRAM/%s/PopularFeed' % party
#os.system(myCmd)
#make_dir('..')

    
 




    
    



















