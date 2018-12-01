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

url=link_df["RestLinks"][0]
html=urllib.request.urlopen(url).read().decode('utf-8')
soup=bs.BeautifulSoup(html)

#get reviewer's name
reviewers= soup.find_all('li', class_='user-name')
for i in range(len(reviewers)):
    reviewer_name=soup.find_all('li', class_='user-name')[i].getText().replace('\n','')
    reviewer_city=soup.find_all('li', class_='user-location responsive-hidden-small')[i].getText().replace('\n','') 
    review_date=soup.find_all('span', class_='rating-qualifier')[i+1].getText().replace('\n','').strip().split("            ")[0]
    elite=soup.find('li', class_="is-elite responsive-small-display-inline-block").getText().replace('\n','')
    review=soup.find_all('p', lang='en')[0].getText()
    print(reviewer_name,'\n',reviewer_city,'\n', review_date,'\n', elite,'\n', review)
