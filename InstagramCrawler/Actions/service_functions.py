#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 17:52:46 2019

@author: mc
"""
from InstagramAPI import InstagramAPI
import time
from datetime import datetime
import requests

media_types =  {1: 'photo', 2:  'video', 8: 'carosuel'}

def parse_media(media):
    media_dict = {}
    
    media_dict['media_id'] = media['id']
    media_dict['creation_utc'] = media['taken_at']
    media_dict['number_of_comments'] = media['comment_count']
    media_dict['number_of_likes'] = media['like_count']
    media_dict['saving_timestamp'] = int(time.time())
    media_dict['media_type_id'] = media['media_type']
    media_dict['media_type_name'] = media_types[media['media_type']]
    
    if not media['caption'] is None :        
        media_dict['caption_media_id'] = media['caption']['media_id']
        media_dict['caption'] = media['caption']['text']
        
    else:
        media_dict['caption_media_id'] = ''
        media_dict['caption'] = ''
    
    if 'carousel_media' in media.keys():
        media_dict['media_id_in_carousel'] = []
        for media_in_carousel in media['carousel_media']:
            media_dict['media_id_in_carousel'].append(media_in_carousel['id'])
    
    return media_dict



'''Given a media ID return COUNT comments and all newer and UNTIL_DATE '''
def parse_comment(API, media_id, count, until_date):
    max_id = ''
    has_more_comments = True
    comments = []
    counter = 1
    while has_more_comments:
        _ = API.getMediaComments(media_id, max_id=max_id)
        
        # comments' page come from older to newer, lets preserve desc order in full list
        for c in reversed(API.LastJson['comments']):
            ''' TODO: clean the field of this'''
            comments.append(c)
        if len(comments) == 0:
            return []
    
    
        has_more_comments = API.LastJson.get('has_more_comments', False)
        print ('%d calls'%counter)
        counter += 1
        
        # evaluate stop conditions
        if count and len(comments) >= count:
            comments = comments[:count]
            # stop loop
            has_more_comments = False
            print ("stopped by count")
            
        if until_date:
            try:
                older_comment = comments[-1]
            except IndexError:
                older_comment = {'created_at_utc' : 1e10}
                until_date = 0
#                return comments
            dt = datetime.utcfromtimestamp(older_comment.get('created_at_utc', 0))
            # only check all records if the last is older than stop condition
            if dt.isoformat() <= until_date:
                # keep comments after until_date
                comments = [
                    c
                    for c in comments
                    if datetime.utcfromtimestamp(c.get('created_at_utc', 0)) > until_date
                ]
                # stop loop
                has_more_comments = False
                print ("stopped by until_date")
                
        # next page
        if has_more_comments:
            max_id = API.LastJson.get('next_max_id', '')
            time.sleep(0.5)
        
    return comments


def get_id(username):
    url = "https://www.instagram.com/web/search/topsearch/?context=blended&query="+username+"&rank_token=0.3953592318270893&count=1"
#    url = 'https://www.instagram.com/%s/?__a=1' % username
    response = requests.get(url)
    respJSON = response.json()
    try:
        user_id = str( respJSON['users'][0].get("user").get("pk") )
        return user_id
    except:
        return "Unexpected error"