# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 14:33:44 2019

@author: dawig
"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt
import math
edge_add_set = pd.read_csv(r'C:/Users/dawig/Desktop/Data698/Maryland/python_files/county_edges_stage_2.csv')

circle_edge_set = []
circle_edge_set_y = []
circle_edge_set_b = []
circle_edge_set_b_y = []
circle_edge_set_blank = [0] *18

#round points in data so points can be found equivalent if they're near enough
for index in range(0,len(edge_add_set)):
    edge_add_set.iloc[index,0]=edge_add_set.iloc[index,0]*4
    edge_add_set.iloc[index,1]=edge_add_set.iloc[index,1]*-4  
    edge_add_set.iloc[index,0]=round(edge_add_set.iloc[index,0],2)
    edge_add_set.iloc[index,1]=round(edge_add_set.iloc[index,1],2)  
    edge_add_set.iloc[index,0]=edge_add_set.iloc[index,0]/4
    edge_add_set.iloc[index,1]=edge_add_set.iloc[index,1]/4

#create circle edge set
for circ_point in range(0,18):
    circle_edge_set.append((-77.21+.32*(math.cos(10*circ_point*math.pi/180))))
    circle_edge_set_y.append(39.15+.32*(math.sin(10*circ_point*math.pi/180)))
    circle_edge_set_b.append((-77.21+.32*(math.cos(10*(circ_point+18)*math.pi/180))))
    circle_edge_set_b_y.append(39.15+.32*(math.sin(10*(circ_point+18)*math.pi/180)))

#start set with start and end points at opposite ends of circle
circle_points_set = pd.DataFrame({'x_points' : circle_edge_set,\
                                'y_points' : circle_edge_set_y,\
                                'x_points_end' : circle_edge_set_b,\
                                'y_points_end' : circle_edge_set_b_y},\
                                 columns=['x_points','y_points','x_points_end','y_points_end'])

class edge_point_finder():
    def __init__(self,circle_edge_set):
        #self.__point_set = point_set
        self.__circle_edge_set = circle_edge_set
        self.__x_start = 0
        self.__x_end = 0
        self.__y_start = 0
        self.__y_end = 0
        
    
    

"""

#create points on a circle
x_val_set<-rep(0,36)
y_val_set<-rep(0,36)
for (i in c(1:36)){
x_val_set[i]<-(-77.21+.32*(cos(10*i*pi/180)))
y_val_set[i]<-(39.15+.32*(sin(10*i*pi/180)))
}
x_val_set
y_val_set
#transfer points to same rounding as edge data
x_val_set<-x_val_set*4
y_val_set<-y_val_set*4
x_val_set<-round(x_val_set,2)
y_val_set<-round(y_val_set,2)
x_val_set<-x_val_set/4
y_val_set<-y_val_set/4"""