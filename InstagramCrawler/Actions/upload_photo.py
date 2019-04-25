#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password

from InstagramAPI import InstagramAPI



InstagramAPI = InstagramAPI("fan_della_lega@libero.it", "chitarra")
InstagramAPI.login()  # login

photo_path = './photo/salvini.jpg'
caption = "Forza Capitano! #efinitalapacchia"
InstagramAPI.uploadPhoto(photo_path, caption=caption)
