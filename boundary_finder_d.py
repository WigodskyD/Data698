# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 02:05:52 2019

@author: dawig
"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt
import copy
"""
class point_cloner:
    def __init__(self, set, direction): #1-left,2-right,3-up,4-down
        self.__set = set
        self.__direction = direction
        self.__new_set = []
        self.__dir = 0   #N/S or E/W
        self.__dir_plus = -1   #N/E or S/W
        self.__first_add = .0067  #shift value up/down 
        self.__second_add = .0111  #   shift value left/right      
        if direction==2:
            self.__dir_plus = 1
        elif direction==3:
            self.__dir = 1
            self.__first_add = .0111
            self.__second_add = .0067
        elif direction==4:
            self.__dir = 1
            self.__dir_plus = 1
            self.__first_add = .0111
            self.__second_add = .0067  
    def cloner(self):
        for member in self.__set:
            member_b = copy.deepcopy(member)
            member_c = copy.deepcopy(member)
            member_b[self.__dir] = member_b[self.__dir]+self.__first_add
            member_c[self.__dir] = member_c[self.__dir]-self.__first_add
            member_d = copy.deepcopy(member)
            member_e = copy.deepcopy(member_b)
            member_f = copy.deepcopy(member_c)
            member_d[(self.__dir+1) % 2] = member_d[(self.__dir+1) % 2]-self.__second_add*self.__dir_plus
            member_e[(self.__dir+1) % 2] = member_e[(self.__dir+1) % 2]-self.__second_add*self.__dir_plus
            member_f[(self.__dir+1) % 2] = member_f[(self.__dir+1) % 2]-self.__second_add*self.__dir_plus
            self.__new_set.append(member)
            self.__new_set.append(member_b)
            self.__new_set.append(member_c)
            self.__new_set.append(member_d)
            self.__new_set.append(member_e)
            self.__new_set.append(member_f)
        return self.__new_set

new_points_set = [[39.125,76.95],[39.13,76.94],[39.13,76.96]]

clone_maker = point_cloner(new_points_set,3)
clone_maker_second_stage = clone_maker.cloner()
#clone_maker_second_stage = point_cloner(clone_maker_second_stage,2)
#clone_maker_second_stage = clone_maker_second_stage.cloner()
edge_add_set = pd.DataFrame.from_dict(clone_maker_second_stage)
edge_add_set.columns = ['latitude','longitude']
montgomery_county_bool = [5] *18
edge_add_set['bool'] = montgomery_county_bool
print(edge_add_set)
edge_add_set.to_csv(r'C:/Users/dawig/Desktop/Data698/Maryland/python_files/county_edges_stage_3.csv', index=False)
"""
edge_add_set = pd.read_csv(r'C:/Users/dawig/Desktop/Data698/Maryland/python_files/county_edges_stage_3.csv')

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


for index in range(0,18):
        if edge_add_set['bool'][index]>4:
            try:
                county_test_var = lat_long_checker(edge_add_set.iloc[index,0],edge_add_set.iloc[index,1])
                edge_add_set.iloc[index,2] = county_test_var.check_county()             
            except:
                print('oops. that location coud not be found')

edge_add_set.to_csv(r'C:/Users/dawig/Desktop/Data698/Maryland/python_files/county_edges_stage_3.csv', index=False)
