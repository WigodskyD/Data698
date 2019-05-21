# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 14:53:48 2019

@author: dawig
"""

import numpy as np, pandas as pd, matplotlib.pyplot as plt
from lxml import html
import requests
import re

""" This method to get county boundaries was superceded by the below method
The idea had been to define it by the edge of where tickets were written.  The western part of the
county is sparse.

speed_violations= pd.read_csv('C:/Users/dawig/Desktop/Data698/Maryland/by_violation_category/joined_registration_violations.csv', skiprows=0)
#print(speed_violations['Latitude'])
print(speed_violations['Latitude'].min())
print(speed_violations['Latitude'].max())
lat_order=speed_violations.sort_values(by='Latitude',ascending=True)
#print(lat_order['Latitude'])"""

x_coord = 77.46
y_coord = 39.1834
page_to_get = 'https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x=-' + str(x_coord) + '&y=' + str(y_coord) + '&benchmark=4&vintage=4'
page = requests.get(page_to_get)
#page = requests.get('https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x=-77.46&y=39.1834&benchmark=4&vintage=4')
xml_from_page = html.fromstring(page.content)
xml_doc = xml_from_page.xpath('//div[@id="pl_gov_census_geo_geocoder_domain_GeographyResult"]')[0]
our_div = xml_doc.text_content()
counties_keyword=re.split('Counties', our_div)[1]
county_name_split=re.split('BASENAME: ', counties_keyword)[1]
print(county_name_split[0:10])
print(int(bool(county_name_split[0:4]=='Mont')))
