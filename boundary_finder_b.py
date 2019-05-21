# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 10:29:04 2019

@author: dawig
"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt
import copy
"""This section filled in some missing points
area_set = pd.read_csv\
    ('C:/Users/dawig/Desktop/Data698/Maryland/python_files/county_area.csv'\
     , skiprows=0,index_col=0)
list_long = list(area_set)
list_lat = list(area_set.index.values)

for index in range(2,22):
    for column in range(2,22):
        neighbors= area_set.loc[list_lat[index],list_long[column-2]]\
                  +area_set.loc[list_lat[index],list_long[column-2]]\
                  +area_set.loc[list_lat[index],list_long[column+1]]\
                  +area_set.loc[list_lat[index],list_long[column+2]]
        own_num=area_set.loc[list_lat[index],list_long[column]]
        print(neighbors)
        if (neighbors==24 and own_num==5):
            area_set.loc[list_lat[index],list_long[column]]=6  
area_set.to_csv(r'C:/Users/dawig/Desktop/Data698/Maryland/python_files/county_area.csv')"""

area_set = pd.read_csv\
    ('C:/Users/dawig/Desktop/Data698/Maryland/python_files/county_area.csv'\
     , skiprows=0,index_col=0)
list_long = list(area_set)
list_lat = list(area_set.index.values)

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
            self.__dir_plus = -1
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

top_set = []
bottom_set = []  #top and bottom sets will hold lat/long of places to check near for edges
end_set = [[39.18],[39.16],[39.14],[39.12],[39.18],[39.16],[39.14],[39.12]] #the edges need to be looked at to the side also(left)
end_set_right = [[39.12],[39.1],[39.08],[39.12],[39.1],[39.08]] #this set looks to the side - to the right
for end in range(0,4):
    end_set[end].append(77.53)
    end_set[end+4].append(77.5)
for end in range(0,3):
    end_set_right[end].append(76.93)
    end_set_right[end+3].append(76.9)
for index in range(0,21):
    for column in range(2,23):
        if (area_set.loc[list_lat[index-1],list_long[column]]==5 and area_set.loc[list_lat[index],list_long[column]]==6):
            top_set.append([list_lat[index],list_long[column]])
        if (area_set.loc[list_lat[index+1],list_long[column]]==5 and area_set.loc[list_lat[index],list_long[column]]==6):
            bottom_set.append([list_lat[index],list_long[column]])
for point in range(0, len(top_set)):                  #these two sets have a str to convert to float 
    top_set[point][1] = float(top_set[point][1])
for point in range(0, len(bottom_set)):
    bottom_set[point][1] = float(bottom_set[point][1])

#use class to clone each of the values into 6 values
clone_set_top = point_cloner(top_set,3)
clone_set_bottom = point_cloner(bottom_set,4)
clone_set_left = point_cloner(end_set,1)
clone_set_right = point_cloner(end_set_right,2)
clone_set_top = clone_set_top.cloner()
clone_set_bottom = clone_set_bottom.cloner()
clone_set_left = clone_set_left.cloner()
clone_set_right = clone_set_right.cloner()
clone_set = clone_set_top + clone_set_bottom + clone_set_left + clone_set_right

final_edge_set = pd.DataFrame.from_dict(clone_set)
final_edge_set.columns = ['latitude','longitude']
final_edge_set.to_csv(r'C:/Users/dawig/Desktop/Data698/Maryland/python_files/county_area_edge_set.csv', index=False)

