"""
@author: Xiaoyu Zhu
"""
#please download the chromedriver before excecuting
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
import csv
import re
import os,sys
from selenium.common.exceptions import NoSuchElementException 

#open the new window and get the url
options = webdriver.ChromeOptions()
options.add_argument('headless')
target_url = 'https://www.tripadvisor.com/Restaurants-g53449-Pittsburgh_Pennsylvania.html'
driver = webdriver.Chrome('.\chromedriver_win32\chromedriver.exe', options=options)
driver.get(target_url)
driver.maximize_window()
soup = BeautifulSoup(driver.page_source, 'html.parser')

# scrape by page: 60 pages in total
next_page = '//*[@id="EATERY_LIST_CONTENTS"]/div[2]/div/a'
check_last_page = '#EATERY_LIST_CONTENTS > div.deckTools.btm > div > div > a:nth-of-type(6)'
page_down = "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;"
page_list = range(int(soup.select(check_last_page)[0].get('data-page-number')))
print("Total number of page: {}".format(len(page_list)))

#Scrape the data except for ratings 

with open('url_parser.csv', 'a') as csvfile:
    fieldnames = ['restaurant_id', 'restaurant_name', 'n_review', 'rank_in_country','price','cuisine','comments']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    index = 0

    for p in page_list:
        print('the number of page = {0}/{1}'.format(p+1, len(page_list)))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for num in range(30):
            if num ==0:
                restaurant_blocks = soup.find_all('div', {"class": "listing rebrand listingIndex-1 first"})
            else:
                restaurant_blocks = soup.find_all('div', {"class": "listing rebrand listingIndex-{:}".format(num+1)})
            
           

            for element in restaurant_blocks:
                index += 1
                restaurant_name = element.find('div', {"class": "title"}).text               
                n_review = element.find('span', {"class": "reviewCount"}).text \
                if element.find('span', {"class": "reviewCount"}) else ''
                n_review = re.sub('[^0-9,]', "", n_review).replace(',','')
                rank_in_country = element.find('div', {"class": "popIndexBlock"}).text if element.find('div', {"class": "popIndexBlock"}).text else ''
                price = element.find('span',{"class":"item price"}).text if element.find('span',{"class":"item price"}) else ''
                cuisine = element.find('a',{"class":"item cuisine"}).text if element.find('a',{"class":"item cuisine"}) else ''  
                comments = element.find('ul',{"class":"review_stubs review_snippets rebrand"}).text if element.find('ul',{"class":"review_stubs review_snippets rebrand"}) else ''
                writer.writerow(
                                {
                                    'restaurant_id':index,
                                    'restaurant_name':restaurant_name,
                                    'n_review':n_review,
                                    'rank_in_country':rank_in_country,
                                    'price':price,
                                    'cuisine':cuisine,
                                    'comments':comments
                                    
                                
                                }
                               )
        if p==0:
            driver.execute_script(page_down)
            time.sleep(5)
            driver.find_element_by_xpath(next_page).click()
            time.sleep(8)
        else:
            try:
                
                driver.execute_script(page_down)
                time.sleep(5)
                driver.find_element_by_xpath('//*[@id="EATERY_LIST_CONTENTS"]/div[2]/div/a[2]').click()
                time.sleep(8)
            except:
                print('in the end')
            

driver.quit()


#Scrape the ratings:
with open('TripAdvisor_1.csv', 'a') as csvfile:
    fieldnames = ['ratings']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    a=[]
                  
    for i in range(0,60):
        container = driver.find_elements_by_xpath("//div[contains(@class,'listing rebrand listingIndex')]")
        num_page_items = len(container)
        for j in range(num_page_items):
        # to save the rating
            string = container[j].find_element_by_xpath(".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute("class")
            data = string.split("_")
            a.append(data)
            writer.writerow({'ratings':data[3]})
        # to change the page
        if i==0:
                driver.execute_script(page_down)
                time.sleep(5)
                driver.find_element_by_xpath(next_page).click()
                time.sleep(8)
        else:
            try:
                
                driver.execute_script(page_down)
                time.sleep(5)
                driver.find_element_by_xpath('//*[@id="EATERY_LIST_CONTENTS"]/div[2]/div/a[2]').click()
                time.sleep(8)
            except:
                print('in the end')    
    driver.close() 

XPATH_RATING = './/span[contains(@class,ui_bubble_rating)]/@alt'
raw_rating = restaurant.xpath(XPATH_RATING)
rating=''
rating = ''.join(raw_rating).replace('of 5 bubbles','').strip() \
if raw_rating else None


