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

#for link in links:
#	print(type(link), link)

################################

# Scraping details page

url = 'https://www.hemnet.se/bostad/lagenhet-2rum-rorsjostaden-malmo-kommun-foreningsgatan-50a-16907356'
page = requests.get(url)
results = BeautifulSoup(page.content, 'html.parser')

address_div = results.find('div', class_ = 'property-address')
price_p = results.find('p', class_ = 'property-info__price qa-property-price')
info_div = results.find('div', class_ = 'property-info__attributes-and-description')


# Extracting the address and area
address = address_div.find('h1', class_ = 'qa-property-heading hcl-heading hcl-heading--size2 hcl-heading--reset-margin').text
#print(type(address), address)

area = address_div.find('span', class_ = 'property-address__area').text
#print(type(area), area)


# Extracing the price and converting to int
price = price_p.text
price = [x for x in price if x in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']]
price = ''.join(price)
price = int(price)
#print(type(price), price)




# Extracting the info attributes and description
print('-----------------------------------------------------------------')
print(type(info_div), '\n', info_div)

property_type = info_div.find('dd', class_ = 'property-attributes-table__value').text
tenure_type = info_div.find('dd', class_ = 'property-attributes-table__value').text

#print(type(tenure_type), tenure_type)

print('-----------------------------------------------------------------')

#for div in info_div.find_all('div'):
#	c = div['class']
#	if 'property-attributes-table__row' in div['class'][0]:
#		print(type(div), div)
	#print('c = ', type(c), c)
#	print('-----------------------------------------------------------------')
	#print(type(div), div)
	#div.find('dd', class_ = 'property-attributes-table__value').text

dt = info_div.find_all('dt', class_ = 'property-attributes-table__label')
dd = info_div.find_all('dd', class_ = 'property-attributes-table__value')

dt = [x.text.strip() for x in dt]
dd = [x.text.strip() for x in dd]

dt = dt[:-1]
dd = dd[:-1]

attributes = {key: value for key, value in zip(dt, dd)}
print(attributes) # Cleaning up later

description = info_div.find('div', class_ = 'property-description js-property-description property-description--long').text.strip()
print(type(description), description)

popularity = info_div.find_all('div', class_ = 'property-visits-counter__row-value')
popularity = [x.text for x in popularity]
print(popularity)

new_str = unicodedata.normalize("NFKD", popularity[0])
print(new_str)