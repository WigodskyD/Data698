# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 10:26:47 2019

@author: dawig
"""


"""This is deprecated now that it's saved as csv file indices and columns
list_long = []
for a in range(2304, 2328):
    list_long.insert(0,round(a/30,4)) 
list_lat = []
for b in range(3892, 3936,2):
    list_lat.insert(0,round(b/100,4)) 

print(len(list_long))
print(len(list_lat))"""

#area_set = np.zeros(shape=(len(list_lat),len(list_long)))
#area_set = pd.DataFrame(area_set,columns=list_long, index=list_lat)
#create csv to hold progress so calls to API do not need to be repeated
#area_set.to_csv(r'C:/Users/dawig/Desktop/Data698/Maryland/python_files/county_area.csv')
area_set = pd.read_csv('C:/Users/dawig/Desktop/Data698/Maryland/python_files/county_area.csv', skiprows=0,index_col=0)
list_long = list(area_set)
list_lat = list(area_set.index.values)

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
        

for index in range(0,22):
    for column in range(0,24):
        if area_set.loc[list_lat[index],list_long[column]]<5:
            try:
                county_test_var = lat_long_checker(list_lat[index],list_long[column])
                area_set.loc[list_lat[index],list_long[column]] = county_test_var.check_county()+5              
            except:
                print('oops. that location coud not be found')

area_set.to_csv(r'C:/Users/dawig/Desktop/Data698/Maryland/python_files/county_area.csv')

print(area_set)
print(list_long[1])