#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 12:19:30 2019
@author: jiangchang
"""
from bs4 import BeautifulSoup
import requests
import csv

# Creating CSV for writing data
csv_file = open('zomato_scrape.csv','w',encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['name', 'rate', 'area', 'vote number','phone number', 'cusin style', 'cost', 'address','first review'])

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
        
        # Scrape each info and write all info into csv file
        try:
            name = soup.find('div', class_ = "segment").find('h1', class_ = "res-name").a['title'][:-11]
        except:
            name = None
        
        try:
            rate = soup.find('div', class_ = "segment").find('div', class_ = "rating-div")['aria-label']
        except:
            rate = None
        
        try:
            area = soup.find('div', class_ = "segment").find('div', class_ = "mb5").a.text.strip()
        except:
            area = None
        
        try:
            voteNum = soup.find('div', class_ = "segment").find('span', itemprop = "ratingCount").text.strip()
        except:
            voteNum = None
        
        try:
            phone = soup.find('div', class_ = "segments").find('span', class_ = "tel").text.strip()
        except:
            phone = None
        
        try:
            style = soup.find('div', class_ = "segments").find('div', class_ = "res-info-group").a.text
        except:
            style = None
        
        try:
            cost = soup.find('div', class_ = "segments").find('span', itemprop = "priceRange").text
        except:
            cost = None
        
        try:
            address = soup.find('div', class_ = "segments").find('div', class_ = "res-main-address").span.text
        except:
            address = None
        
        try:
            review1pt = soup.find('div', class_ = "zs-following-list").find('div', class_ = "rev-text").find('div', class_ = "ttupper")['aria-label']
            review1ct = soup.find('div', class_ = "zs-following-list").find('div', class_ = "rev-text").text.strip()[5:].strip()
            reviewcontent = review1pt + ":  " + review1ct
        except:
            reviewcontent = None
            
        csv_writer.writerow([name, rate, area, voteNum, phone,style, cost, address, reviewcontent])
        
csv_file.close()
    