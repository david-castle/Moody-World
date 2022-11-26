#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 15:03:19 2022

@author: davidcastle
"""

import spacy
import pandas as pd
import json
from collections import OrderedDict
import cities_coords

# Read in json file    
data = [json.loads(line) for line in open('20221108_hashtag_test.jsonl', 
                                          'r')]
# Convert read in data to dataframe
df = pd.DataFrame(data)

# Reduce to relevant columns
data_df = df[['url', 'date', 'content', 'id', 'user', 'coordinates', 'hashtags']]

# Convert jsonL file to csv
data_df.to_csv('20221030_test.csv')

# Fill empty coordinate cells with Dummy value
data_df.fillna('Dummy')

# Convert coordinates and content to lists
coordinates = data_df.coordinates.values.tolist()
content = data_df.content.values.tolist()
entities = []
c_entities = []
lats = []
lngs = []

# Define function to parse content for locations. 
def spacy_analysis(text_input):
    nlp = spacy.load('en_core_web_sm')
    text = text_input
    doc = nlp(text)
    global temp_entities
    temp_entities = []

    # Iterate over the predicted entities
    for ent in doc.ents:
        
        # Print the entity text based on its label
        if ent.label_ == "GPE":
            #print(ent.text)
            temp_entities.append(ent.text)
        else:
            temp_entities.append("NF")
    return temp_entities

def entities_cleanup(text_input):
    for entity in entities:
        result = list(OrderedDict.fromkeys(entity))
        if len(result) > 1:
            result.remove('NF')
        c_entities.append(result)
    return c_entities

def coord_assignments(entity_list, city_dictionary):
    for city in entity_list:
        for key, values in city_dictionary.items():
            if city[0] == key:
                lat = values[0]
                lng = values[1]
                lats.append(lat)
                lngs.append(lng)
            elif city[0] != key:
                lats.append(0)
                lngs.append(0)
    
for text in content:
    spacy_analysis(text)
    entities.append(temp_entities)

entities_cleanup(entities)
#coord_assignments(c_entities, cities_coords.city_coords)

data_df['city'] = c_entities
data_df['lats'] = ''
data_df['lngs'] = ''

for key, values in cities_coords.city_coords.items():
    data_df.loc[data_df.city.str[0] == key, 'lats'] = values[0]
    data_df.loc[data_df.city.str[0] == key, 'lngs'] = values[1]

data_df.to_json('query_result_to_site.json')



