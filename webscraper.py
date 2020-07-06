import requests
#from selenium import webdriver
import unicodedata
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

url = 'https://www.hemnet.se/bostader?location_ids%5B%5D=17989&item_types%5B%5D=bostadsratt'
page = requests.get(url)
results = BeautifulSoup(page.content, 'html.parser')

#housing_elems = results.find_all('li', class_ = 'normal-results__hit js-normal-list-item')
#print(type(housing_elems), len(housing_elems), '\n', housing_elems[0])

housing_elems = results.find_all('a', class_ = 'js-listing-card-link listing-card')

links = []

for housing_elem in housing_elems:
	links.append(housing_elem['href'])

# Get list of details page urls, given a search page url
def get_urls_detail_pages(search_page_url):
	
	housing_elems = results.find_all('a', class_ = 'js-listing-card-link listing-card')	
	lst_details_urls = []

	for housing_elem in housing_elems:
		lst_details_urls.append(housing_elem['href'])

	return lst_details_urls


#for link in links:
#	print(type(link), link)

################################
# Scraping details page

#url = 'https://www.hemnet.se/bostad/lagenhet-2rum-rorsjostaden-malmo-kommun-foreningsgatan-50a-16907356'

def get_details(url):

	details = {}

	page = requests.get(url)
	results = BeautifulSoup(page.content, 'html.parser')

	address_div = results.find('div', class_ = 'property-address')
	price_p = results.find('p', class_ = 'property-info__price qa-property-price')
	info_div = results.find('div', class_ = 'property-info__attributes-and-description')


	# Extracting the address and area
	address = address_div.find('h1', class_ = 'qa-property-heading hcl-heading hcl-heading--size2 hcl-heading--reset-margin').text
	details['address'] = address

	area = address_div.find('span', class_ = 'property-address__area').text
	details['area'] = area

	# Extracing the price and converting to int
	price = price_p.text
	price = [x for x in price if x in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']]
	price = ''.join(price)
	price = int(price)
	details['price'] = price

	# Extracting the info attributes and description
	#property_type = info_div.find('dd', class_ = 'property-attributes-table__value').text
	#tenure_type = info_div.find('dd', class_ = 'property-attributes-table__value').text

	#details['property_type'] = property_type
	#details['tenure_type'] = tenure_type

	dt = info_div.find_all('dt', class_ = 'property-attributes-table__label')
	dd = info_div.find_all('dd', class_ = 'property-attributes-table__value')

	dt = [x.text.strip() for x in dt]
	dd = [x.text.strip() for x in dd]

	dt = dt[:-1]
	dd = dd[:-1]

	attributes = {key: value for key, value in zip(dt, dd)}
	#print('ATTR = ', attributes)
	details.update(attributes)

	popularity = info_div.find_all('div', class_ = 'property-visits-counter__row-value')
	popularity = [x.text for x in popularity]
	
	try:
		visits = popularity[0]
		days_available = popularity[1]	
	except Exception as e:
		visits = None
		days_available = None
	
	details['visits'] = visits
	details['days_available'] = days_available	
	
	try:
		description = info_div.find('div', class_ = 'property-description js-property-description property-description--long').text.strip()
	except:
		description = None
	details['description'] = description

	return details

#for link in links:
#	print('link = ', link)
	#print(get_details('https://www.hemnet.se/bostad/lagenhet-2rum-mollevangen-malmo-kommun-simrishamnsgatan-7-b-16886300'))
#	print(get_details(link))
#	r = random.uniform(0, 5)
#	time.sleep(r)

# Get details of multiple properties found on a given a list of detail page urls
def get_details_multiple(lst_details_urls):

	# Adding details for the first property
	details = get_details(lst_details_urls[0])
	details = {key: [value] for key, value in details.items()}
	df = pd.DataFrame.from_dict(details)

	# Adding details for the rest of the properties
	for i, details_url in enumerate(lst_details_urls[1:]):

		if i > 3:
			break

		print(details_url)

		details = get_details(details_url)
		df = df.append(details, ignore_index = True)
		time.sleep(random.uniform(0, 1.5))

	return df


t0 = time.time()
lst_details_urls = get_urls_detail_pages('https://www.hemnet.se/bostader?location_ids%5B%5D=17989&item_types%5B%5D=bostadsratt')
df = get_details_multiple(lst_details_urls)
t1 = time.time()

t_tot = t1-t0
print('Time taken = ', t_tot)
print(df.head())

path = '/py_scripts/df.pkl' # Path inside the docker container, to which a volume has been mounted
df.to_pickle(path)
df2 = pd.read_pickle(path)
print(df2.head())



# details = get_details('https://www.hemnet.se/bostad/lagenhet-2rum-rorsjostaden-malmo-kommun-foreningsgatan-50a-16907356')
# #print(details)
# details_first = {key: [value] for key, value in details.items()}
# #print(details)

# df = pd.DataFrame.from_dict(details_first)
# print(df.head())

# df = df.append(details, ignore_index = True)
# print('------------------------------------------------------')
# print(df.head())