#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 08:05:00 2022

@author: davidcastle
"""

import logging
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler('scveda_20221009.log')

formatter = logging.Formatter('%(asctime)s - %(message)s')
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

# Enable headless browsing to save resources
options = Options()
options.headless = True
options.add_argument("--window-size=1920, 1200")

# Access to Twitter - Ensure browser is already active
url = r'https://twitter.com/search?lang=en-GB&q=pfizer%20until%3A2015-08-10%20since%3A2014-08-10&src=typed_query'
driver = webdriver.Firefox()
#driver = webdriver.Firefox(options=options)
driver.get(url)
logger.info("Request sent to Twitter start page")
#print(driver.page_source)
#driver.quit