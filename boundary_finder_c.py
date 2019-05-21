# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 00:58:27 2019

@author: dawig
"""

import numpy as np, pandas as pd, matplotlib.pyplot as plt
import copy

edge_set = pd.read_csv(r'C:/Users/dawig/Desktop/Data698/Maryland/python_files/county_edges_stage_2.csv')

"""This code created the 3rd column, but sould only be used once
montgomery_county_bool = [5] * 300
edge_set['bool'] = montgomery_county_bool"""

class lat_long_checker:
    def __init__(self,lat_input,long_input):
        self.__in_county=3
        self.__x_coord=long_input
        self.__y_coord=lat_input
    def check_county(self):
        page_to_get = 'https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x=-' + str(self.__x_coord) + '&y=' + str(self.__y_coord) + '&benchmark=4&vintage=4'
        page = requests.get(page_to_get)
        xml_from_page = html.fromstring(page.content)
        xml_doc = xml_from_page.xpath('//div[@id="pl_gov_census_geo_geocoder_domain_GeographyResult"]')[0]
        our_div = xml_doc.text_content()
        counties_keyword=re.split('Counties', our_div)[1]
        county_name_split=re.split('BASENAME: ', counties_keyword)[1]
        self.__in_county = int(bool(county_name_split[0:4]=='Mont'))
        return self.__in_county
#tester = lat_long_checker(39.1834,77.46)
#test_value = tester.check_county()     
#print(test_value)
        

for index in range(0,300):
        if edge_set['bool'][index]>4:
            try:
                county_test_var = lat_long_checker(edge_set.iloc[index,0],edge_set.iloc[index,1])
                edge_set.iloc[index,2] = county_test_var.check_county()             
            except:
                print('oops. that location coud not be found')

#edge_set.to_csv(r'C:/Users/dawig/Desktop/Data698/Maryland/python_files/county_edges_stage_2.csv', index=False)


