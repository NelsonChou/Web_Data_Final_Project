#For reviewer level data
import os
os.chdir('C:\\Users\\micha\\OneDrive\\Desktop\\Web Data Analytics\\Project')

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
link_df = pd.read_csv("C:\\Users\\micha\\OneDrive\\Desktop\\Web Data Analytics\\Project\\Restaurant_Links.csv",delimiter= ',') 

df_reviewer_info = pd.DataFrame()

#for i in range(len(link_df)):
for i in range(0,1):
    
    while soup.find_all('span', class_='pagination-label responsive-hidden-small pagination-links_anchor')[0].getText()=='Next':    

        #variables
        RestNames=[]
        RestLinks=[]
        reviewer_list=[]
        reviewer_city_list=[]
        review_date_list=[]
        #reviewer_reviews=[]
        review_list=[]
        yelp_elite=[]
        review_votes=[]
        review_star=[]


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

        reviewers= soup.find_all('li', class_='user-name')
        for j in range(len(reviewers)):

            #get Restaurant name 
            restaurant_name = link_df['RestNames'][i]
            RestNames.append(restaurant_name)
            print(restaurant_name)

            #get Restaurant link    
            RestLinks.append(link_df['RestLinks'][i])

            #get other reviewer details
            reviewer_name=soup.find_all('li', class_='user-name')[j].getText().replace('\n','')
            print(reviewer_name)
            reviewer_city=soup.find_all('li', class_='user-location responsive-hidden-small')[j].getText().replace('\n','') 
            print(reviewer_city)
            review_date=soup.find_all('span', class_='rating-qualifier')[j+3].getText().replace('\n','').strip().split("            ")[0]
            print(review_date)
            #elite=soup.find('li', class_="is-elite responsive-small-display-inline-block").getText().replace('\n','')
            review=soup.find_all('p', lang='en')[j].getText()
            print(review)
#             votelist =[]
#             for k in range(0,3):

#                 #x=soup.find_all('ul', class_='voting-buttons')[k].find_all('span',class_='vote-type')[k].getText()
#                 y=int(soup.find_all('ul', class_='voting-buttons')[0].find_all('span',class_='count')[0].getText().replace('','0'))
#                 votelist.append(y)
#             votes_sum=sum(votelist)    
#             print(votes_sum)

    #         #Elite user info: 
    #         index_final=0

    #         while html[index_final:].find('<li class="is-elite responsive-small-display-inline-block">')!=-1:                
    #             index1=html[index_final:].find('<li class="is-elite responsive-small-display-inline-block">')
    #             index_final+=index1
    #             index2=html[index_final:].find('<a href="/elite">')
    #             index_final+=index2
    #             index3=html[index_final:].find('</a>')
    #             #reviewer_elite_list.append(html_restaurant[index_final:][17:index3])
    #             elite=html[index_final:][17:index3]
    #             print(elite)

            df_reviewer_info=df_reviewer_info.append({'Restaurant name':restaurant_name,'Reviewer Name':reviewer_name,'Reviewer_City':reviewer_city,'Review Date':review_date,'Review':review},ignore_index=True)

            # Take a random sleep after scrape 1 page, between 2 to 7 second
            sleep=random.randint(2,7)
            time.sleep(sleep)
    
    #Get user rating and later combine with the restaurant review dataframe
    page_num=0
    
    url=link_df['RestLinks'].iloc[0]+'?start='+str(page_num)
    html=urllib.request.urlopen(url).read().decode('utf-8')
    soup=bs.BeautifulSoup(html)
    
    current_page=int(soup.find_all('div', class_='page-of-pages arrange_unit arrange_unit--fill')[0].getText().strip().split(' ')[1])
    total_page=int(soup.find_all('div', class_='page-of-pages arrange_unit arrange_unit--fill')[0].getText().strip().split(' ')[3])
    
    reviewer_rating_list=[]
    
    while current_page<=total_page:
        #review rating on user level (the stars):
        index_final=0
        page_num+=20
        
        while html[index_final:].find('<div class="biz-rating biz-rating-large clearfix">')!=-1:
            index1=html[index_final:].find('<div class="biz-rating biz-rating-large clearfix">')
            index_final+=index1
            index2=html[index_final:].find('title')
            index_final+=index2
            index3=html[index_final:].find('star rating')
            reviewer_rating_list.append(html[index_final:][7:index3])
            index_final+=index3
    
        url=link_df['RestLinks'].iloc[i]+'?start='+str(page_num)
        html=urllib.request.urlopen(url).read().decode('utf-8')
        soup=bs.BeautifulSoup(html)
        
        current_page=int(soup.find_all('div', class_='page-of-pages arrange_unit arrange_unit--fill')[0].getText().strip().split(' ')[1])
        total_page=int(soup.find_all('div', class_='page-of-pages arrange_unit arrange_unit--fill')[0].getText().strip().split(' ')[3])
        
        sleep=random.randint(2,7)
        time.sleep(sleep)

col=['Rating']
df_reviewer_rating=pd.DataFrame(reviewer_rating_list, columns=col)
    
df_reviewer_info=pd.concat(['df_reviewer_info', 'df_reviewer_rating', axis=1])
    
        
