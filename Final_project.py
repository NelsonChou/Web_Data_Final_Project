#Web Data Analytics- Final Project

import pandas as pd
import urllib
import bs4 as bs
from bs4 import SoupStrainer
from bs4 import BeautifulSoup
import os
os.chdir('D:\\Master Program\\03. Begin\\Course\\09. Web Data Analytics\\Project')


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

soup_restaurant.find_all('address')
