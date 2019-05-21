# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 02:04:24 2019

@author: dawig
"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt
import math
import statistics
import csv


test_data = [{'start':11,'end':47},{'start':6,'end':35},{'start':18,'end':27},{'start':40,'end':67},{'start':3,'end':44},{'start':8,'end':66}]
test_data_tester = test_data
test_data = pd.DataFrame(test_data,columns={'start','end'})
print(test_data)
class circle_edge_finder:
    def __init__(self,row,value_to_check,x_start_col,x_end_col,y_start_col,y_end_col):
        #x_set
        self.__x_start_col = x_start_col
        self.__x_end_col = x_end_col
        self.__x_start_set = row[self.__x_start_col]
        self.__x_end_set = row[self.__x_end_col] 
        self.__x_interval_set = []
        #y_set
        self.__y_start_col = y_start_col
        self.__y_end_col = y_end_col
        self.__y_start_set = row[self.__y_start_col]
        self.__y_end_set = row[self.__y_end_col] 
        self.__y_interval_set = []
        #
        self.__true_counter = 0
        self.__edge_match_holder = []  #holds values for match to be checked for max and min
        self.calculate_intervals(row)
        self.list_checker()
    def calculate_intervals(self,row):
        #x_set
        row_interval = (row[self.__x_end_col] - row[self.__x_start_col])/100
        for num in range(1,101):
            self.__x_interval_set.append(self.value_rounder(self.__x_start_set+row_interval * num))
        #y_set
        row_interval = (row[self.__y_end_col] - row[self.__y_start_col])/100
        for num in range(1,101):
            self.__y_interval_set.append(self.value_rounder(self.__y_start_set+row_interval * num))
        return(self.__x_interval_set,self.__y_interval_set)
    def value_rounder(self,val):
        val = val * 1.3
        val = round(val,2)
        val = val/1.3
        return(val)
    def list_checker(self):
        search_for_border_vals = []
        for num in self.__x_interval_set:
            if num in value_to_check:
                search_for_border_vals.append(num)
            else :
                pass
        #print(statistics.mean(search_for_border_vals))
        for row_index in range(0,len(self.__y_interval_set)):
            dict_of_circle_check_set = {'latitude':self.__y_interval_set[row_index],'longitude':self.__x_interval_set[row_index]*-1,'bool': '1'}
            #print(dict_of_circle_check_set in county_edges_set)
            if dict_of_circle_check_set in county_edges_set:
                self.__edge_match_holder.append(dict_of_circle_check_set)
                self.__true_counter = self.__true_counter+1
        edge_matches_as_data_frame=pd.DataFrame(self.__edge_match_holder)
        print(edge_matches_as_data_frame)
        print(edge_matches_as_data_frame.iloc[0])
        print(edge_matches_as_data_frame.iloc[-1])
        with open('C:/Users/dawig/Desktop/Data698/Maryland/python_files/county_edges_first_last_match_rerun.csv','a') as edge_writer:
               writer = csv.writer(edge_writer)
               writer.writerow(edge_matches_as_data_frame.iloc[0])
               writer.writerow(edge_matches_as_data_frame.iloc[-1])
        edge_writer.close()
        
       # with open('person.csv', 'w') as csvFile:
    #writer = csv.writer(csvFile)
   # writer.writerows(csvData)

#csvFile.close()
            
value_to_check = [16.4,34.71,22.86,63.76,4.23,28.88,47,22.88, 23.24, 23.6, 23.96, 24.32]       

#circ_edge = circle_edge_finder(test_data.iloc[0],value_to_check)
#test_data.apply(circle_edge_finder,args=[value_to_check], axis=1)
#circ_edge.list_printer()
print('up')
print( {'start':11,'end':47} in test_data_tester)
#import county_edges_stage_2 to create hash search for values
county_edges_set = []
with open('C:/Users/dawig/Desktop/Data698/Maryland/python_files/county_edges_stage_2.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        lat_val = float(row['latitude']) * 1.3
        lat_val = round(lat_val,2)
        lat_val = lat_val / 1.3
        long_val = float(row['longitude']) * 1.3
        long_val = round(long_val,2)
        long_val = long_val / 1.3
        county_edges_set.append({'latitude': lat_val, 'longitude': long_val, 'bool' : row['bool']})
county_edges_set = [d for d in county_edges_set if d['bool'] =='1']

#create circle edge set
circle_edge_set = []
circle_edge_set_y = []
circle_edge_set_b = []
circle_edge_set_b_y = []
circle_edge_set_blank = [0] *144
for circ_point in range(0,144):
    circle_edge_set.append((-77.21+.32*(math.cos(1.25*circ_point*math.pi/180))))
    circle_edge_set_y.append(39.15+.32*(math.sin(1.25*circ_point*math.pi/180)))
    circle_edge_set_b.append((-77.21+.32*(math.cos(1.25*(circ_point+144)*math.pi/180))))
    circle_edge_set_b_y.append(39.15+.32*(math.sin(1.25*(circ_point+144)*math.pi/180)))
#start set with start and end points at opposite ends of circle
circle_points_set = pd.DataFrame({'x_points' : circle_edge_set,\
                                'y_points' : circle_edge_set_y,\
                                'x_points_end' : circle_edge_set_b,\
                                'y_points_end' : circle_edge_set_b_y},\
                                 columns=['x_points','y_points','x_points_end','y_points_end'])

circle_points_set.apply(circle_edge_finder,args=[value_to_check,'x_points','x_points_end','y_points','y_points_end'], axis=1)

#print(county_edges_set)

a_lat = round(39.1375*4,2)/4
a_long = round(76.97*4,2)/4
a_dict = {'latitude': a_lat, 'longitude': a_long, 'bool':'1'}

#print(county_edges_set)


#def simple_function(row):
#    return row['start']+row['end']
#print(simple_function(test_data.iloc[2]))
#create a new column after apply
#rectangles_df.apply(calculate_area, axis=1)
#rectangles_df['area'] = rectangles_df.apply(calculate_area, axis=1)
#rectangles_df