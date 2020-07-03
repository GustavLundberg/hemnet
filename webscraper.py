import requests
#from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.hemnet.se/bostader?location_ids%5B%5D=17989&item_types%5B%5D=bostadsratt'
page = requests.get(url)
results = BeautifulSoup(page.content, 'html.parser')

#housing_elems = results.find_all('li', class_ = 'normal-results__hit js-normal-list-item')
#print(type(housing_elems), len(housing_elems), '\n', housing_elems[0])

housing_elems = results.find_all('a', class_ = 'js-listing-card-link listing-card')

links = []

for housing_elem in housing_elems:
	links.append(housing_elem['href'])

for link in links:
	print(type(link), link)

################################

# Scraping details page

url = 'https://www.hemnet.se/bostad/lagenhet-2rum-rorsjostaden-malmo-kommun-foreningsgatan-50a-16907356'
page = requests.get(url)
results = BeautifulSoup(page.content, 'html.parser')

address_div = results.find_all('div', class_ = 'property-address')
price_div = results.find_all('p', class_ = 'property-info__price qa-property-price')
info_div = results.find_all('div', class_ = 'property-info__attributes-and-description')

print('-----------------------------------------------------------------')
print(type(address_div), '\n', address_div)
print('-----------------------------------------------------------------')
print(type(price_div), '\n', price_div)
print('-----------------------------------------------------------------')
print(type(info_div), '\n', info_div)

