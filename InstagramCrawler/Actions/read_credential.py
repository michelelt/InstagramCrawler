#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 18:08:36 2019

@author: mc
"""

path = '../../Credential/'

def credential(party):
    file = open(path+'%s_cred.txt'%party, 'r')
    cred_list = file.readlines()[0].split(';')
    return cred_list[0], cred_list[1]


