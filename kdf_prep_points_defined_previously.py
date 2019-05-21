# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 12:54:42 2019

@author: dawig
"""

import numpy as np, pandas as pd, matplotlib.pyplot as plt
import math
import copy

kernel_points = pd.read_csv(r'C:/Users/dawig/Desktop/Data698/Maryland/kernels/school_bus_blank.csv')
school_bus_set = pd.read_csv(r'C:/Users/dawig/Desktop/Data698/Maryland/accidents_unique.csv')
school_bus_set = school_bus_set.loc[:,['Latitude','Longitude']]


#set sectors for kernel
kernel_points = kernel_points.assign(lat_sector=pd.Series((kernel_points['latitude'] - 38.9418) / .000794).values)
kernel_points['lat_sector'] = kernel_points['lat_sector'].apply(lambda x: math.floor(x))

kernel_points = kernel_points.assign(long_sector=pd.Series((kernel_points['longitude'] + 76.91439) / -.0000793).values)
kernel_points['long_sector'] = kernel_points['long_sector'].apply(lambda x: math.ceil(x))

#set sectors for experience
school_bus_set = school_bus_set.assign(lat_sector=pd.Series((school_bus_set['Latitude'] - 38.9418) / .000794).values)
school_bus_set = school_bus_set.dropna()
school_bus_set['lat_sector'] = school_bus_set['lat_sector'].apply(lambda x: math.floor(x))

school_bus_set = school_bus_set.assign(long_sector=pd.Series((school_bus_set['Longitude'] + 76.91439) / -.0000793).values)
school_bus_set['long_sector'] = school_bus_set['long_sector'].apply(lambda x: math.ceil(x))

#-----------------------------------
"""
----class to calculate kernel density
----select nearby point sectors   - scan a strip at a time
----calculate distance
----add to kernel
----divide by sum to make density sum to 1
"""
class kernel_density:
    def __init__(self,kernel_set,estimator_inputs,long_column):
        self.__kernel_points = kernel_set 
        self.__estimator_inputs = estimator_inputs
        self.__secondary_estimator_inputs = estimator_inputs
        self.__longitude_group = long_column
        self.__kernel_lat = 0
        self.__kernel_long = 0
        self.__estimator_lat = 0
        self.__estimator_long = 0
        #self.__latitude_group = lat_column
        self.__lat_sector_fed_in = 2400
        #choose a vertical stripe of the kernel points and the raw estimator
        self.__estimator_column_chooser() 
        self.__kernel_column_chooser()
        self.__kernel_adder()
    def __estimator_column_chooser(self):
        """This function chooses a vertical column of the estimator to set a kernel from."""
        column_set_low = self.__longitude_group - 120
        self.__estimator_inputs = self.__estimator_inputs[self.__estimator_inputs['long_sector'] > column_set_low]
        column_set_high = self.__longitude_group + 120
        self.__estimator_inputs = self.__estimator_inputs[self.__estimator_inputs['long_sector'] < column_set_high]
        return self.__estimator_inputs
    def __estimator_lat_chooser(self):
        lat_set_low = self.__lat_sector_fed_in - 14
        self.__secondary_estimator_inputs = self.__estimator_inputs[self.__estimator_inputs['lat_sector'] > lat_set_low]
        lat_set_high = self.__lat_sector_fed_in + 14
        self.__secondary_estimator_inputs = self.__secondary_estimator_inputs[self.__secondary_estimator_inputs['lat_sector'] < lat_set_high]
        return self.__secondary_estimator_inputs
    def __kernel_column_chooser(self):
        column_set = self.__longitude_group
        self.__kernel_points = self.__kernel_points[self.__kernel_points['long_sector'] == column_set]
        return self.__kernel_points
    def __kernel_adder(self):
        df_iter = 0
        for lat_sector, point in self.__kernel_points.iterrows():
            if point['kernel_raw'] < 0 :
                point['kernel_raw'] = 0
                self.__lat_sector_fed_in = point['lat_sector']
                self.__estimator_lat_chooser()  
                print(point)
                self.__kernel_lat = point['latitude']
                self.__kernel_long = point['longitude']
                kernel_sum = 0
                for column, row in self.__secondary_estimator_inputs.iterrows():
                    self.__estimator_lat = row['Latitude']
                    self.__estimator_long = row['Longitude']
                    kernel_addition_val = self.__kernel_estimator_calc()
                    kernel_sum = kernel_addition_val + kernel_sum
                    point['kernel_raw'] = kernel_sum
                print(point)
                print('p')
            print(point)
            self.__kernel_points.iloc[df_iter] = point
            df_iter = df_iter+1
        return self.__kernel_points
       
                    
        #if self.__kernel_points.iloc[5]['kernel_raw'] < 0:
        #    print('yes')
        #    print(len(self.__kernel_points))
        #return self.__kernel_points.iloc[5]
    def __kernel_estimator_calc(self):
        kernel_addition_value = ((self.__estimator_lat-self.__kernel_lat)**2+(self.__estimator_long-self.__kernel_long)**2)**.5
        kernel_addition_value = max((1-(kernel_addition_value/.0089)),0)
        return kernel_addition_value
    def kernel_returner(self):
        return self.__kernel_points
    def estimator_inputs_returner(self):
        return self.__estimator_inputs
    def temp_printer(self):
        for lat_sector, point in self.__kernel_points.iterrows():
            print(point['long_sector'])

a_kernel = kernel_density(kernel_points,school_bus_set,1)
kernel_set_a = a_kernel.kernel_returner()
kernel_set_a.to_csv(r'C:/Users/dawig/Desktop/Data698/Maryland/kernels/throwaway.csv')
for num in range(2,7724):
    b_kernel = kernel_density(kernel_points,school_bus_set,num)
    kernel_set_b = b_kernel.kernel_returner()
    with open('C:/Users/dawig/Desktop/Data698/Maryland/kernels/throwaway.csv', 'a') as csv_filler:
             kernel_set_b.to_csv(csv_filler, header=False)
  
#notification that file has run:           
import winsound
winsound.PlaySound('C:/Users/dawig/Desktop/Data698/hunt_for_red_verify1.wav',winsound.SND_FILENAME)
winsound.PlaySound('C:/Users/dawig/Desktop/Data698/montana2.wav',winsound.SND_FILENAME)
#print(a_kernel.kernel_returner())

#print(a_kernel.kernel_adder())
#print(a_kernel.kernel_returner())
#a_kernel.kernel_adder()
#kernel_points = kernel_points[1:15]
#print(kernel_points)
#for lat_sector, point in kernel_points.iterrows():
#    print(point['lat_sector'])











