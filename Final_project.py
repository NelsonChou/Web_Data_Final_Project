#Web Data Analytics- Final Project

import pandas as pd
import urllib
import bs4 as bs
from bs4 import SoupStrainer
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import random
import time
from urllib.request import FancyURLopener  # This is library that helps us create the headless browser
from random import choice #This library helps pick a random item from a list

#variables
reviewer_city_list=[]
reviewer_list=[]
reviews_list=[]
reviews_date_list=[]
business_info_yesno_list=[]
col_restaurant_info=['Restaurant name','Address','Business info','Yes/No','Review counts','Price range']
df_restaurant_info=pd.DataFrame(columns=col_restaurant_info)

#part 1: scrap all restaurant link: Lotto
user_agents = [
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
]

# These are the usr agents for each of different browsers. Here we are using five, but it can be any number of user agents
RestNames = []
RestLinks = []

p = 0 # set the first page
last_page = False 

while last_page == False:
    class MyOpener(FancyURLopener, object):
        version = choice(user_agents)

    myopener = MyOpener()
    page=myopener.open('https://www.yelp.com/search?find_desc=Mexican&find_loc=Seattle,+WA&start=' + str(p*30))
    html = page.read().decode('utf-8')

    soup = bs.BeautifulSoup(html, 'html5lib')
    for biz in soup.find_all('span', class_='indexed-biz-name'):
        RestNames.append(biz.find('a', class_='biz-name js-analytics-click').getText())
        RestLinks.append('https://www.yelp.com' + biz.find('a', class_='biz-name js-analytics-click').get('href')) # get the quotes, get rid of the quote marks.

    if soup.find_all('span', class_='pagination-label responsive-hidden-small pagination-links_anchor') == []: # see if there is a 'next' button
        last_page = True # if not, then it is the last page, the loop stops.
    else:
        p += 1 # otherwise, go to next page.
        
    # Take a random sleep after scrape 1 page, between 2 to 7 second
    sleep=random.randint(2,7)
    time.sleep(sleep)



#part 2: scrap restaurant details
url='https://www.yelp.com/search?cflt=mexican&find_loc=Seattle' #Yelp Seattle Mexican restaurant 1st page
url_yelp='https://www.yelp.com'

html=urllib.request.urlopen(url).read().decode('utf-8')
soup=bs.BeautifulSoup(html)

#Restaurant name and subink are under below long class
soup=soup.find_all('a', class_='lemon--a__373c0__1_OnJ link__373c0__29943 link-color--blue-dark__373c0__1mhJo link-size--inherit__373c0__2JXk5')
soup=soup[5:] #restaurant information begins from 6 elements onward

#for i in 

sub_link=soup[0].attrs['href'] #sublink of the first restaurant
restaurant_page_link=url_yelp+sub_link+'?start='+str(0)

html_restaurant=urllib.request.urlopen(restaurant_page_link).read().decode('utf-8')
soup_restaurant=bs.BeautifulSoup(html_restaurant)

####################
###Restaurant's part
####################

#get restaurant name
restaurant_name=soup_restaurant.find_all('h1', class_='biz-page-title')[0].getText()
restaurant_name=restaurant_name.replace('\n','').strip()

#get address
address=soup_restaurant.find_all('address')[1].getText()
address=address.replace('\n','').strip()

#get review count: maybe useless once we break down
review_count=soup_restaurant.find_all('span', class_='review-count rating-qualifier')[0].getText()
review_count=review_count.replace('\n','').strip().split(' ')[0]

#get price range and calculate average spent
price_range=soup_restaurant.find_all('dd', class_='nowrap price-description')[0].getText()
price_range=price_range.replace('\n','').strip()
price_range=(int(price_range[1:].split('-')[0])+int(price_range[1:].split('-')[1]))/2 #take mean value

#get business info: only need to get once from the main page
business_info=soup_restaurant.find_all('dt', class_='attribute-key')[2:]
business_info_all=[]

for i in range(len(business_info)):
    business_info_clean=business_info[i].getText()
    business_info_clean=business_info_clean.replace('\n','').strip()
    business_info_all.append(business_info_clean)

#get yes, no, casual for business info- not done yet: Nelson
index_final=html_restaurant.find('<h3>More business info</h3>')

while html_restaurant[index_final:].find('<dt class="attribute-key">')!=-1:
    index1=html_restaurant[index_final:].find('<dt class="attribute-key">')
    index_final+=index1
    index2=html_restaurant[index_final:].find('<dd>')
    index_final+=index2
    index3=html_restaurant[index_final:][5:].find('\n')
    business_info_yesno_list.append(html_restaurant[index_final+5:][:index3].strip())

#write result to restaurant info dataframe
for i in range(len(business_info_yesno_list)):
    df_restaurant_info=df_restaurant_info.append({'Restaurant name':restaurant_name, 'Address':address, 'Business info':business_info_all[i],
                                  'Yes/No':business_info_yesno_list[i], 'Review counts':review_count, 'Price range':price_range}, ignore_index=True)

##################
###Reviewer's part
##################

#set starting point: if current page number is smaller than total page number, keep going to next page
current_page=int(soup_restaurant.find_all('div', class_='page-of-pages arrange_unit arrange_unit--fill')[0].getText().strip().split(' ')[1])
total_page=int(soup_restaurant.find_all('div', class_='page-of-pages arrange_unit arrange_unit--fill')[0].getText().strip().split(' ')[3])

page_num=0

while current_page<=total_page: #if current page is smaller or equal to total page, scrap the page
    page_num+=20
    
    #get reviewer's name
    reviewer=soup_restaurant.find_all('li', class_='user-name')
    
    for i in range(len(reviewer)):
        reviewer_list.append(reviewer[i].get_text().replace('\n',''))
    
    #get review content
    reviews=soup_restaurant.find_all('p', lang='en')
    
    for i in range(len(reviews)):
        reviews_list.append(reviews[i].get_text())    
       
    #Date of review: Nelson
    index_final=0
    
    while html_restaurant[index_final:].find('<span class="rating-qualifier">')!=-1:
        index1=html_restaurant[index_final:].find('<span class="rating-qualifier">')
        index_final+=index1
        index2=html_restaurant[index_final:].find('\n')
        index_final+=index2
        index3=html_restaurant[index_final:][1:].find('\n')
        reviews_date_list.append(html_restaurant[index_final:][:index3+1].split(' ')[-1])
    
    #review city: Nelson 
    index_final=0
    
    while html_restaurant[index_final:].find('<li class="user-location responsive-hidden-small">')!=-1:
        index1=html_restaurant[index_final:].find('<li class="user-location responsive-hidden-small">')
        index_final+=index1
        index2=html_restaurant[index_final:].find('<b>')
        index_final+=index2
        index3=html_restaurant[index_final:].find('</b>')
        reviewer_city_list.append(html_restaurant[index_final:][3:index3])
        index_final+=index3
    
    #review rating on user level (the stars): Chaitali
    index_final=0
    
    while html_restaurant[index_final:].find('<div class="biz-rating biz-rating-large clearfix">')!=-1:
        index1=html_restaurant[index_final:].find('<div class="biz-rating biz-rating-large clearfix">')
        index_final+=index1
        index2=html_restaurant[index_final:].find('title')
        index_final+=index2
        index3=html_restaurant[index_final:].find('star rating')
        reviewer_rating_list.append(html_restaurant[index_final:][7:index3])
        index_final+=index3
    
    #Elite user info: Chaitali



    #find next page
    restaurant_page_link=url_yelp+sub_link+'?start='+str(page_num)
    
    html_restaurant=urllib.request.urlopen(restaurant_page_link).read().decode('utf-8')
    soup_restaurant=bs.BeautifulSoup(html_restaurant)
    
    current_page=int(soup_restaurant.find_all('div', class_='page-of-pages arrange_unit arrange_unit--fill')[0].getText().strip().split(' ')[1])
    total_page=int(soup_restaurant.find_all('div', class_='page-of-pages arrange_unit arrange_unit--fill')[0].getText().strip().split(' ')[3])
 
