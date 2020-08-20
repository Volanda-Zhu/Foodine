# Merging Data
# merge.py merges all the data scraped from four websites into a single dataframe
# putting 4 websites' info for a restaurant in a single row
# it also generates the 'suggested_rating' based on the ratings and review numbers of 4 websites
# finally it generates two columns naming 'latitude' and 'longitude' based on the address str for the restaurant

# # Merging Data

import pandas as pd
import numpy as np
import re
from geopy.exc import GeocoderTimedOut
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim

# function that gets the alphabetic substring of a str
def get_alpha_str(s):
    result = ''.join(re.split(r'[^A-Za-z]', s))
    return result

#load data from scrapedData into 4 DataFrames each for one website
yelp=pd.read_excel(".\data\ScrapedData.xlsx", sheet_name = "Yelp_clean")
zomato=pd.read_excel(".\data\ScrapedData.xlsx", sheet_name = "Zomato_raw")
dzdp=pd.read_excel(".\data\ScrapedData.xlsx", sheet_name = "Dazhongdianping_clean")
trip_advisor=pd.read_excel(".\data\ScrapedData.xlsx", sheet_name = "Tripadvisor_clean")

# reomove ' Pittsburgh' in zomato['name']
zomato['name'] = zomato['name'].map(lambda x: x[:-11])
zomato['name'] = zomato['name'].map(lambda x: x.strip())

#rename columns
yelp = yelp.rename(columns={'Name':'name','Address':'address','number of reviews': 'yelp_rev_num'})
zomato=zomato.rename(columns={'rate':'zomato_rating','cusin style':'cuisine_style',
                       'vote number':'zomato_rev_num','first review':'zomato_review'})
trip_advisor=trip_advisor.rename(columns={'restaurant_name':'name','ratings':'ta_rating',
                       'n_review':'ta_rev_num','comments':'ta_review'})

#remove '-' in zomato['rating']
zomato[zomato['zomato_rating']=='-']=np.nan

#creating match column for the purpose of merging data

dzdp['match']=dzdp['name'].map(lambda x: get_alpha_str(str(x))[:5].lower())
# zomato['match1']=zomato['address'].map(lambda x: str(x)[:7].lower())
zomato['match']=zomato['name'].map(lambda x: get_alpha_str(str(x))[:5].lower())
# trip_advisor['match']=trip_advisor['address'].map(lambda x: str(x)[:10].lower())
# yelp['match']=yelp['address'].map(lambda x: str(x)[:13].lower())
yelp['match']=yelp['name'].map(lambda x: get_alpha_str(str(x))[:5].lower())


# merge data from 4 dataFrame into merge
#the basic table is zomato
merge1= pd.merge(zomato,
                yelp[['name','yelp_rating','yelp_rev_num','yelp_review']],on='name', how='left')
merge2= pd.merge(merge1,
                trip_advisor[['name','ta_rating','ta_rev_num','ta_review']],on='name', how='left')
merge= pd.merge(merge2,
               dzdp[['name','dzdp_rating']],on='name',how='left')

#remove duplicated rows
merge = merge.drop_duplicates(subset=['name', 'address'], keep='first')

#copy merge and fill np.nan cells with 0 to calculate suggested_rating
merge_copy=merge.copy()
merge_copy=merge_copy.fillna(0)

#calculate suggested_rating
merge['suggested_rating']=(merge_copy['zomato_rating']*merge_copy['zomato_rev_num']+merge_copy['yelp_rating']*merge_copy['yelp_rev_num']
                           +merge_copy['ta_rating']*merge_copy['ta_rev_num'])/(merge_copy['yelp_rev_num']
                                                                     +merge_copy['ta_rev_num']+merge_copy['zomato_rev_num'])
merge = merge.round({'suggested_rating': 1})

#reset index
merge= merge.reset_index(drop=True)

# adding latitude and longitude columns in merge

# function that gets the latitude and longitude based on the address string
def do_geocode(address):
    geolocator = Nominatim()
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    try:
        return  geolocator.geocode(address)
    except GeocoderTimedOut:
        return do_geocode(address)

#generate latitude and longitude value for each restaurant and update merge table
latitude=[]
longitude=[]
for i in range(len(merge)):
    print(i)
    k=0
    location=do_geocode(str(merge['address'][i]).split(',')[0]+' Pittsburgh')
    if(location is not None):
        latitude.append(location.latitude)
        longitude.append(location.longitude)
        k=1

    if(k==0):
        latitude.append(0)
        longitude.append(0)


merge['latitude']=pd.Series(latitude)
merge['longitude']=pd.Series(longitude)
merge.to_csv('merge_data_final.csv')