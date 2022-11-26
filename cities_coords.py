#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 07:58:30 2022

@author: davidcastle
"""

import pandas as pd

city_info = pd.read_csv('world_cities.csv')
city_coords_df = city_info[['city', 'lat', 'lng']]

city = city_coords_df.city.values.tolist()
city.append('NF')
lat = city_coords_df.lat.values.tolist()
lat.append('0')
lng = city_coords_df.lng.values.tolist()
lng.append('0')

lat_lng = zip(lat, lng)

city_lats = dict(zip(city, lat))
city_lngs = dict(zip(city, lng))
city_coords = dict(zip(city, lat_lng))