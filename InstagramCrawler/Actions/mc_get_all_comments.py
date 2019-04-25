#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password

from InstagramAPI import InstagramAPI
import time
from datetime import datetime

 
def get_all_comments(API, media_id, until_date, count, has_more_comments, max_id,
                     comments_dict):
    old_id  = API.username_id
    API.username_id = media_id.split('_')[1]
    print('comments scrape of %s begun'%media_id)
        
    comments = []
    while has_more_comments:
        _ = API.getMediaComments(media_id, max_id=max_id)
        
        # comments' page come from older to newer, lets preserve desc order in full list
        for c in reversed(API.LastJson['comments']):
            ''' TODO: clean the field of this'''
            comments.append(c)
            
    
    
        has_more_comments = API.LastJson.get('has_more_comments', False)
#        print (has_more_comments)
        
        # evaluate stop conditions
        if count and len(comments) >= count:
            comments = comments[:count]
            # stop loop
            has_more_comments = False
            print ("stopped by count")
            
        if until_date:
            try:
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
            except IndexError:
                print('Media %s does not have comments' % media_id)
                if not comments_dict is None:
                    comments_dict[media_id] = comments
                return []
                
        # next page
        if has_more_comments:
            max_id = API.LastJson.get('next_max_id', '')
            time.sleep(2)
            
    if not comments_dict is None:
        comments_dict[media_id] = comments
        
    print('comments scrape of %s ended'%media_id)

    return comments

