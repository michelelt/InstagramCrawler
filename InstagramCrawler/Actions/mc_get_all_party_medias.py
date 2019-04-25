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


party_igID ={
        'LEGA' :  get_id('legaofficial'),
        'M5S': get_id('movimento5stelle'),
        'PD' : get_id('partitodemocratico')
        }


crd = credential(party)
api = InstagramAPI(crd[0], crd[1])
api.login()

for party in party_igID.keys():
    username_id = party_igID[party]
    party='matteosalvini'
    username_id = get_id('matteosalviniofficial')
    medias = api.getTotalUserFeed(username_id)
    fp = open('../PartyMedias/%s_medias.json'%party, 'w')
    json.dump(medias, fp)
    fp.close()
    break


