#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 08:48:49 2019

@author: mc
"""

from InstagramAPI import InstagramAPI
from mc_get_all_comments import get_all_comments
from service_functions import get_id
import time
from threading import Thread
import json
from read_credential import credential
import datetime
import os
from pytz import reference
import requests
import string
import re

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

popular_hashtags = {}

try: party = sys.argv[1]
except IndexError: party = 'LEGA'


def get_popular_hashtag(pary):
    with open('../partyMedias/%s_medias.json'%party, 'r') as fp:
        medias = json.load(fp)
    
                                         
    RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
    def strip_emoji(text):
        return RE_EMOJI.sub(r'', text)
    
    
    my_punt = string.punctuation.replace('#', '')
    my_punt +='\n'
    media_strange = []
    for media in medias:
        
        try :
            text = media['caption']['text']
            text = text.translate(str.maketrans('', '', my_punt))
            text = strip_emoji(text)
            
                                                                                   
            text = text.split(' ')
            for word in text:
                if '#' in word:
                    word = word.lower().rstrip().lstrip()
                    if word[0] == '#':
                        continue
                    else:
                        word =  word.split('#')[1]
                        word = '#'+word
                    
                    if word not in popular_hashtags.keys():
                        popular_hashtags[word] = 1
                    else:
                        popular_hashtags[word] +=1
        except TypeError:
            media_strange.append(media)
                    
    
    sorted_x = sorted(popular_hashtags.items(), key=lambda kv: kv[1])[::-1]
    return sorted_x

#for party in ['LEGA', 'M5S', 'PD']:
for party in ['matteosalvini']:
    sorted_hasthags = get_popular_hashtag(party)
#    fp = open('../MEDIA/%s/Hashtags/%s_popular_hashtags.txt'%(party,party), 'w')
#    for hashtag in sorted_hasthags:
#        fp.write(hashtag[0] + '\n')
#    fp.close()




    