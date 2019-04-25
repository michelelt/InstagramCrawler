#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 16:41:17 2019

@author: mc
"""

import sys,os

# =============================================================================
# popular feed
# =============================================================================
def make_dir(root):
    
    if not os.path.exists('%s/INSTAGRAM'%root):
        os.mkdir('%s/INSTAGRAM'%root)
        
    
    
    for party in ['LEGA', 'M5S', 'PD']:
        if not os.path.exists('%s/INSTAGRAM/%s/'%(root,party)):
            os.mkdir('%s/INSTAGRAM/%s/'%(root, party))



        if not os.path.exists('%s/INSTAGRAM/%s/PopularFeed'%(root, party)):
            os.mkdir('%s/INSTAGRAM/%s/PopularFeed'%(root, party))
        
        
        if not os.path.exists('%s/INSTAGRAM/%s/PopularFeed/medias/'%(root, party)):
            os.mkdir('%s/INSTAGRAM/%s/PopularFeed/medias/'%(root, party))
        
        if not os.path.exists('%s/INSTAGRAM/%s/PopularFeed/comments/'%(root, party)):
            os.mkdir('%s/INSTAGRAM/%s/PopularFeed/comments/'%(root, party))
            
        ####
        
        if not os.path.exists('%s/INSTAGRAM/%s/TimeLineFeed'%(root, party)):
            os.mkdir('%s/INSTAGRAM/%s/TimeLineFeed'%(root, party))
        
        
        if not os.path.exists('%s/INSTAGRAM/%s/TimeLineFeed/medias/'%(root, party)):
            os.mkdir('%s/INSTAGRAM/%s/TimeLineFeed/medias/'%(root, party))
        
        if not os.path.exists('%s/INSTAGRAM/%s/TimeLineFeed/comments/'%(root, party)):
            os.mkdir('%s/INSTAGRAM/%s/TimeLineFeed/comments/'%(root, party))
            
        if not os.path.exists('%s/INSTAGRAM/%s/TimeLineFeed/suggested_users/'%(root, party)):
            os.mkdir('%s/INSTAGRAM/%s/TimeLineFeed/suggested_users/'%(root, party))
                    
        ####
        
        if not os.path.exists('%s/INSTAGRAM/%s/User'%(root, party)):
            os.mkdir('%s/INSTAGRAM/%s/User'%(root, party))
        
        
        if not os.path.exists('%s/INSTAGRAM/%s/User/medias/'%(root, party)):
            os.mkdir('%s/INSTAGRAM/%s/User/medias/'%(root, party))
        
        if not os.path.exists('%s/INSTAGRAM/%s/User/comments/'%(root, party)):
            os.mkdir('%s/INSTAGRAM/%s/User/comments/'%(root, party))
            
        if not os.path.exists('%s/INSTAGRAM/%s/User/media_likers/'%(root, party)):
            os.mkdir('%s/INSTAGRAM/%s/User/media_likers/'%(root, party))
            
        if not os.path.exists('%s/INSTAGRAM/%s/User/followers/'%(root, party)):
            os.mkdir('%s/INSTAGRAM/%s/User/followers/'%(root, party))  
            
        if not os.path.exists('%s/INSTAGRAM/%s/User/followings/'%(root, party)):
            os.mkdir('%s/INSTAGRAM/%s/User/followings/'%(root, party))

   
        