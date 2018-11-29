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

soup_restaurant.find_all('address')
