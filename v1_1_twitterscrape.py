#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 09:33:58 2022

@author: davidcastle
"""
import logging
import sys
import os
from datetime import datetime, timedelta

# Setting up the logger. 

stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler('scrape_loop_log.log')

class OneLineExceptionFormatter(logging.Formatter):
    def formatException(self, exc_info):
        result = super().formatException(exc_info)
        return repr(result)
 
    def format(self, record):
        result = super().format(record)
        if record.exc_text:
            result = result.replace("\n", "")
        return result

formatter = OneLineExceptionFormatter(logging.BASIC_FORMAT)
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(os.environ.get("LOGLEVEL", "ERROR"))

logger.addHandler(stream_handler)
logger.addHandler(file_handler)
logger.propagate = False


# Base components for search
base_url = 'twitter.com'
language = 'English'
keyword = None
profile_name = 'soundstrue'
search_term = ['linux', 'fun']
hashtags = ['oktoberfest', 'munich', 'linux']
date_from = '2022-09-01'
date_to = '2022-10-01'
today = datetime.today()


class Scrape_Twitter():
    def __init__(self, hashtags, date_from, date_to, profile_name, search_term):
        self.hashtags = hashtags
        self.date_from = date_from
        self.date_to = date_to
        self.profile_name = profile_name
        self.search_term = search_term


    def hashtag(self, date_from=today - timedelta(days=30), 
                                date_to=today):
        if hashtags != None:
            for tag in self.hashtags:
                try:
                    command = 'snscrape --jsonl --with-entity --max-results 100 ' \
                    '--since ' + self.date_from + ' twitter-hashtag ' + str(tag) + ' >20221108_hashtag_test.jsonl'
                    #print(command)
                    cmd = command
                    os.system(cmd)
                    logger.info("Request for hashtag sent to Twitter via subprocess")
                except:
                    logger.error('No hashtags in request.')
                    pass
    
    def profile(self, date_from=today - timedelta(days=30), 
                                date_to=today):
        if profile_name != None:
            try:
                command = 'snscrape --jsonl --with-entity --max-results 100 ' \
                '--since ' + self.date_from + ' twitter-user ' + str(self.profile_name) + ' >20221108_profile_test.jsonl'
                #print(command)
                cmd = command
                os.system(cmd)
                logger.info("Request for profile sent to Twitter via subprocess")
            except:
                logger.error('No profile specified in request.')
                pass
     
    def search(self, date_from=today - timedelta(days=30), 
                                date_to=today):
        if search_term != None:
            for term in self.search_term:
                try:
                    command = 'snscrape --jsonl --with-entity --max-results 100 ' \
                        '--since ' + self.date_from + ' twitter-search ' + term + ' >20221108_search_test.jsonl'
                    #print(command)
                    cmd = command
                    os.system(cmd)
                    logger.info("Request for search term sent to Twitter via subprocess")
                except:
                    logger.error('No search term in request.')
                    pass
    


searches = Scrape_Twitter(hashtags, date_from, date_to, profile_name, search_term)
searches.hashtag()
searches.profile()
searches.search()
