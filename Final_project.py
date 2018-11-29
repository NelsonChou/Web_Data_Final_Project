#Web Data Analytics- Final Project

import pandas as pd
import urllib
import bs4 as bs
from bs4 import SoupStrainer
from bs4 import BeautifulSoup
import os
os.chdir('D:\\Master Program\\03. Begin\\Course\\09. Web Data Analytics\\Project')

#Part 1: Scraping all Yelp review for Mexican restaurants in Seattle
url='https://www.yelp.com/search?cflt=mexican&find_loc=Seattle' #Yelp Seattle Mexican restaurant 1st page
url_yelp='https://www.yelp.com'

html=urllib.request.urlopen(url).read().decode('utf-8')
soup=bs.BeautifulSoup(html)

#Restaurant name and subink are under below long class
soup=soup.find_all('a', class_='lemon--a__373c0__1_OnJ link__373c0__29943 link-color--blue-dark__373c0__1mhJo link-size--inherit__373c0__2JXk5')
soup=soup[5:] #restaurant information begins from 6 elements onward

#for i in 

sub_link=soup[0].attrs['href'] #sublink of the first restaurant
restaurant_page_link=url_yelp+sub_link

html_restaurant=urllib.request.urlopen(restaurant_page_link).read().decode('utf-8')
soup_restaurant=bs.BeautifulSoup(html_restaurant)
restaurant_name=soup_restaurant.find_all('h1', class_='biz-page-title')[0].getText()
restaurant_name=restaurant_name.replace('\n','')
restaurant_name=restaurant_name.strip()

#create a loop to capture all user ids
user_id=[]
urls=[]
reviewer_name=[]
reviews_list=[]
index_count=0
ending_index=0
last_page=False
page_count=20 #second page review start with 20

while last_page==False:

    while html_restaurant[ending_index:].find('class="review review--with-sidebar') !=-1:
        index_count=0
        remaining=html_restaurant[ending_index:]
        index_loop=remaining.find('class="review review--with-sidebar')
        index_count+=index_loop #capture the last index location
        remaining=remaining[index_loop:]
        index_loop=remaining.find('user_id:')

        index_count+=index_loop #capture the last index location
        remaining=remaining[index_loop:]
        index_loop=remaining.find(':')

        index_count+=index_loop #capture the last index location
        remaining=remaining[index_loop+1:]
        index_loop=remaining.find('"')
        index_count+=1
        
        #locator to search for user name
        user=remaining[:index_loop]
        urls='<a class="user-display-name js-analytics-click" href="/user_details?userid='+user+'"'
        
        #get user name
        index=html_restaurant.find(urls)
        remaining=html_restaurant[index:]
        index_start=remaining.find('>')+1
        index_end=remaining.find('</')
        reviewer=remaining[index_start:index_end]
        reviewer_name.append(reviewer)
        
        #get reviews
        index=html_restaurant.find(urls) #start from user name
        remaining=html_restaurant[index:]
        index=remaining.find('<p lang="en">')
        remaining=remaining[index:]
        index=remaining.find('>')+1
        remaining=remaining[index:]
        index=remaining.find('</p>')
        remaining=remaining[:index]
        reviews=remaining.replace('<br>','') #replace <br> with space
        reviews_list.append(reviews)
        
        ending_index+=index_count+index_loop
        
    index = html_restaurant.find('pagination-links_anchor">Next</span>')
        
    if index==-1:
        last_page=True
    else:
        link=restaurant_page_link+'?start='+str(page_count)
        html_restaurant=urllib.request.urlopen(link).read().decode('utf-8')
        page_count+=20 #add 20 for next page's link
        ending_index=0 #reset ending_index for next page's search

