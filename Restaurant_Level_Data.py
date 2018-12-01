#for restaurant level data
import os
path = "C:\\Users\\micha\\OneDrive\\Desktop\\Web Data Analytics\\Project"
os.chdir(path)

import pandas as pd
import urllib
import time
import random
from random import choice #to pick a random item from a list
import bs4 as bs 
from bs4 import SoupStrainer
from bs4 import BeautifulSoup
from urllib.request import FancyURLopener #to create the headless browser

import pandas as pd
file_name = "Restaurant_Links.csv"
link_df = pd.read_csv(path+'\\'+file_name,delimiter= ',') 
link_df.head()
range(len(link_df))

df_restaurant_info = pd.DataFrame()

for i in range(len(link_df)):
    RestNames=[]
    RestLinks=[]
    RestAddress=[]
    RevCount=[]
    business_info_yesno_list=[]
    business_info_all=[]
    RestPrice =[]
    Price_Not_Found='F'
    user_agents = [
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
    ]

# These are the user agents for each of different browsers. Here we are using five, but it can be any number of user agents


    class MyOpener(FancyURLopener, object):
        version = choice(user_agents)

    myopener = MyOpener()
    page=myopener.open(link_df['RestLinks'][i])
    html = page.read().decode('utf-8')
    soup = bs.BeautifulSoup(html, 'html5lib')

    #get Restaurant name 
    restaurant_name = link_df['RestNames'][i]
    RestNames.append(restaurant_name)
    print(restaurant_name)

    #get Restaurant link    
    RestLinks.append(link_df['RestLinks'][i])

    #get Restaurant address
    address=soup.find_all('address')[1].getText().replace('\n','').strip()
    RestAddress.append(address)
    print(address)
    
    #get Review Counts till now    
    review_count=soup.find_all('span', class_='review-count rating-qualifier')[0].getText()
    review_count=review_count.replace('\n','').strip().split(' ')[0]
    RevCount.append(review_count)
    print(review_count)

    #get price range and calculate average spent    
    try:
        price_range=soup.find_all('dd', class_='nowrap price-description')[0].getText()
        print(price_range)
        price_range=price_range.replace('\n','').strip()
        price_range_length = price_range.split('-')
        if len(price_range_length) > 1:
            price_range=(int(price_range[1:].split('-')[0])+int(price_range[1:].split('-')[1]))/2 #take mean value
        else:
            price_range= int(price_range[1:].split(' ')[1][1:])  
    except:
        price_range='NA'
        print(price_range)
        Price_Not_Found='T'

    RestPrice.append(price_range)


    #get business info: only need to get once from the main page
    business_info=soup.find_all('dt', class_='attribute-key')
    if(business_info[0].getText()) == 'Today':
        if Price_Not_Found=='F':
            business_info=soup.find_all('dt', class_='attribute-key')[2:]
        elif Price_Not_Found=='T':
            business_info=soup.find_all('dt', class_='attribute-key')[1:]
    else:
        if Price_Not_Found=='F':
            business_info=soup.find_all('dt', class_='attribute-key')[1:]
        elif Price_Not_Found=='T':
            business_info=soup.find_all('dt', class_='attribute-key')[0:]
    
    for i in range(len(business_info)):
        business_info_clean=business_info[i].getText()
        business_info_clean=business_info_clean.replace('\n','').strip()
        business_info_all.append(business_info_clean)
    print(business_info_all)    

    #get yes, no, casual for business info- not done yet: Nelson
    index_final=html.find('<h3>More business info</h3>')
    
    while html[index_final:].find('<dt class="attribute-key">')!=-1:
        index1=html[index_final:].find('<dt class="attribute-key">')
        index_final+=index1
        index2=html[index_final:].find('<dd>')
        index_final+=index2
        index3=html[index_final:][5:].find('\n')
        business_info_yesno_list.append(html[index_final+5:][:index3].strip())
    print(business_info_yesno_list)    
    
    #write result to restaurant info dataframe
    for j in range(len(business_info_yesno_list)):
        df_restaurant_info=df_restaurant_info.append({'Restaurant name':restaurant_name, 'Address':address, 'Business info':business_info_all[j],'Yes/No':business_info_yesno_list[j], 'Review counts':review_count, 'Price range':price_range},ignore_index=True)

    # Take a random sleep after scrape 1 page, between 2 to 7 second
    sleep=random.randint(2,7)
    time.sleep(sleep)
