#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 09:33:58 2022

@author: davidcastle
"""
import logging
import sys
import os

# Setting up the logger. 
logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler('scrape_loop_log.log')

formatter = logging.Formatter('%(asctime)s - %(message)s')
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

# Base components for search
base_url = 'twitter.com'
language = 'English'
keyword = None
hashtags = ['oktoberfest', 'munich']
date_from = '2022-09-01'
date_to = '2022-10-01'

def scrape_twitter(hashtag, date_from):
    if hashtags != None:
        for tag in hashtags:
            command = 'snscrape --jsonl --with-entity --max-results 100 ' \
            '--since ' + date_from + ' twitter-hashtag ' + tag + ' >20221030_test.jsonl'
            print(command)
            cmd = command
            os.system(cmd)
            logger.info("Request sent to Twitter via subprocess")
    else:
        logger.info('Query needs a valid hashtag value to be entered.')
        pass

scrape_twitter(hashtags, date_from)
