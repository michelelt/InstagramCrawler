#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 19:06:05 2019

@author: mc
"""

import datetime
import sys
from pytz import reference
import os
# =============================================================================
# popular feed
# =============================================================================

  

localtime = reference.LocalTimezone()
today = datetime.datetime.today().strftime('%Y-%m-%d') # in local timezone

if not os.path.exists('./MEDIA/'):
    os.mkdir('MEDIA')



for party in ['LEGA', 'M5S', 'PD']:
    if not os.path.exists('./MEDIA/%s/'%(party)):
        os.mkdir('./MEDIA/%s/'%(party))
#        
    if not os.path.exists('./MEDIA/%s/Hashtags/'%(party)):
        os.mkdir('./MEDIA/%s/Hashtags/'%(party))
        
        

    if not os.path.exists('./MEDIA/%s/Captions/'%(party)):
        os.mkdir('./MEDIA/%s/Captions/'%(party))
#        
    if not os.path.exists('./MEDIA/%s/Photos/'%(party)):
        os.mkdir('./MEDIA/%s/Photos/'%(party))