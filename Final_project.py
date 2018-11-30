#Web Data Analytics- Final Project

import pandas as pd
import urllib
import bs4 as bs
from bs4 import SoupStrainer
from bs4 import BeautifulSoup
import os
os.chdir('D:\\Master Program\\03. Begin\\Course\\09. Web Data Analytics\\Project')

#variables
reviewer_city_list=[]
reviewer_list=[]
reviews_list=[]
reviews_date_list=[]
business_info_yesno_list=[]

#part 1: scrap all restaurant link: Lotto
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
# chromedriver's path must be absolute path in Mac, this is the syntax
driver = webdriver.Chrome('/Users/lotto/Documents/WebData/HW/chromedriver', options = chrome_options)

#Part 0：Scraping all the Mexican restaurant links in Seattle, WA. Save it in to a list.
RestLinks = []

page = 0 # set the first page
last_page = False 

while last_page == False:

    driver = webdriver.Chrome('/Users/lotto/Documents/WebData/HW/chromedriver', options = chrome_options) 
    driver.get('https://www.yelp.com/search?find_desc=Mexican&find_loc=Seattle,+WA&start=' + str(page*30)) # the format of the url
    assert 'Yelp' in driver.title # Wait for the page to load
    html = driver.page_source # Get the html of the page
    driver.quit() # Close the browser

    soup = bs(html, 'html.parser')

    for quote in soup.find_all('div', class_='quote'):
        Quote.append(quote.find('span', class_='text').getText()[1:-1]) # get the quotes, get rid of the quote marks.


    if soup.find_all('li', class_='next') == []: # see if there is a 'next' button
        last_page = True # if not, then it is the last page, the loop stops.
    else:
        page += 1 # otherwise, go to next page.


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
restaurant_page_link=url_yelp+sub_link

html_restaurant=urllib.request.urlopen(restaurant_page_link).read().decode('utf-8')
soup_restaurant=bs.BeautifulSoup(html_restaurant)

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

#get reviewer's name
reviewer=soup_restaurant.find_all('li', class_='user-name')

for i in range(len(reviewer)):
    reviewer_list.append(reviewer[i].get_text().replace('\n',''))

#get review content
reviews=soup_restaurant.find_all('p', lang='en')

for i in range(len(reviews)):
    reviews_list.append(reviews[i].get_text())    
   
################
#To be continued
################

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

#get yes, no, casual for business info- not done yet: Nelson
index_final=html_restaurant.find('<h3>More business info</h3>')

while html_restaurant[index_final:].find('<dt class="attribute-key">')!=-1:
    index1=html_restaurant[index_final:].find('<dt class="attribute-key">')
    index_final+=index1
    index2=html_restaurant[index_final:].find('<dd>')
    index_final+=index2
    index3=html_restaurant[index_final:][5:].find('\n')
    business_info_yesno_list.append(html_restaurant[index_final+5:][:index3].strip())

#review rating on user level (the stars): Chaitali


#Elite user info: Chaitali



#Need to travel through all the pages for all above basically
