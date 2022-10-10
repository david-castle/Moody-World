#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 10:33:20 2022

@author: davidcastle
"""
base_url = 'twitter.com'
language = 'English'
keyword = None
hashtags = ['oktoberfest', 'munich']
date_from = '2022-09-01'
date_to = '2022-10-01'

language_dict = {
    'English':'en',
    'French':'fr',
    'German':'de'}

language_component = ''
url_tags = []
#all_tags = ''

comp1 = 'https://'
comp2 = '/search?lang='
comp3 = '&q='
comp4 = '%20until%3A'
comp5 = '%20since%3A'
comp6 = '&src=typed_query'
comp7 = '/search?q='
comp8 = '&src=typed_query&f=latest'

# BUILD A CLASS FOR THE PARSING PROCESS FROM THE ORIGINAL FRONT END JSON
class Parse_and_Build():
    def __init__(self, base_url, language, keyword, hashtags, date_to, date_from):
        self.base_url = base_url
        self.language = language
        self.keyword = keyword
        self.hashtags = hashtags
        self.date_to = date_to
        self.date_from = date_from
        
        self.hashtag_parsing(hashtags)
        self.url_builder(base_url, language, keyword, date_to, date_from)
        

    def hashtag_parsing(self, hashtags):
        if len(hashtags) > 1:
            for tag in hashtags:
                url_tag = '%23' + tag + '%20'
                url_tags.append(url_tag)
            global all_tags    
            all_tags = ''.join(url_tags)
            all_tags = all_tags[0:-3]
            print(all_tags)
        else:
            pass


    
    # FUNCTION TO BUILD THE URL
    def url_builder(self, base_url, language, keyword, date_to, date_from):
        for key, value in language_dict.items():
            if language == key:
                language_component = value
            else:
                pass
        if keyword is None:
            #build url-string with hash tags
            url = comp1 + base_url + comp7 + all_tags + comp4 + date_to + \
            comp5 + date_from + comp8
            print(url)
        elif hashtags is None:
            # Build url-string
            url = comp1 + base_url + comp2 + language_component + comp3 + \
                keyword + comp4 + date_to + comp5 + date_from + comp6
            print(url)

 
Parse_and_Build(base_url, language, keyword, hashtags, date_to, date_from)