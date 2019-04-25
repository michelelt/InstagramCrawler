#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 15:12:32 2019

@author: mc
"""


from InstagramAPI import InstagramAPI
import time
from datetime import datetime

michele = InstagramAPI("michele__lt", "ab187!Qry")
michele.login()
username_id = michele.username_id


# =============================================================================
# functions
# =============================================================================

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
            older_comment = comments[-1]
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



# =============================================================================
# retrieving all the media of my profile
# =============================================================================
michele.getSelfUserFeed()
total_user_feed = michele.getTotalUserFeed(username_id)



# =============================================================================
# detect de type of media if carousel or single post
# =============================================================================
#media_dict ={}
#parsed_medias = []
#list_id  = -1
#carosuel = 0
#for media in total_user_feed:
#    parsed_medias.append(parse_media(media))


#michele.timelineFeed()
#time_line_feed = michele.LastJson
#print('processing cr7')  
#cr7_id = 173560420

    
            

    
