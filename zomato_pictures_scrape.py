#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 12:19:30 2019
@author: jiangchang
"""
from bs4 import BeautifulSoup
import requests
import urllib.request
import os

# create a folder to save pictures
folder = os.getcwd() + '.\images_scraped\\'
if not os.path.exists(folder):
    os.makedirs(folder)

# Function to save image from a url
def dl_jpg(url, file_path, file_name):
    fullpath = file_path + file_name + '.jpg'
    urllib.request.urlretrieve(url, fullpath)

# Prepare Scraping
url = 'https://www.zomato.com/pittsburgh/restaurants'
agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
source = requests.get(url, headers=agent).text
soup = BeautifulSoup(source, 'lxml')
# Find the number of pages then loop the crapying in all pages
totalpage = int(soup.find('div', class_ = "pagination-number").find_all('b')[1].text)

for i in range(1,totalpage + 1):
    url = 'https://www.zomato.com/pittsburgh/restaurants' + '?page=' + str(i)
    print(url)
    try:
        source = requests.get(url, headers=agent).text
    except:
        break
    soup = BeautifulSoup(source, 'lxml')
    
    # Find the unit block that contain info for each restaurant
    for article in soup.find_all('div', class_ = "search-snippet-card"):       
        # find restaurant link each info and write into CSV   
        resLink = article.find('a', class_ = "result-title")['href']
        # get the link for individual restaurant
        print(resLink)
        #Scrape individual website
        agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        source = requests.get(resLink, headers=agent).text
        soup = BeautifulSoup(source, 'lxml')
        
        # Scrape the restautrant name
        try:
            name = soup.find('div', class_ = "segment").find('h1', class_ = "res-name").a['title'][:-11]
        except:
            name = None
        
        # Scrape image address
        try:
            image = soup.find('div', class_ = "res-header-overlay").find('div', class_ = "photosContainer").a.div["data-original"]
        except:
            image = None
        
        # save the image named after restaurant name
        try:
            dl_jpg(image, 'images_scraped/', name)
            print("image saved")
        except:
            print("no image found")
            continue
        
        
        
      
            

        
        
        
     
        
        
        
        
        
        
        
        
        

    