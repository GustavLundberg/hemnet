import requests
import unicodedata
import pandas as pd
import time
import random
import re

from bs4 import BeautifulSoup


# Get list of details page urls, given a search page url
def get_urls_detail_pages(search_page_url):
	
	page = requests.get(search_page_url)
	results = BeautifulSoup(page.content, 'html.parser')
	housing_elems = results.find_all('a', class_ = 'js-listing-card-link listing-card')	
	lst_details_urls = []

	for housing_elem in housing_elems:
		#print(housing_elem['href'])
		lst_details_urls.append(housing_elem['href'])

	return lst_details_urls


# Converts a price string to an integer price
def price_str_to_int(price_str):

	price = [x for x in price_str if x in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']]
	price = ''.join(price)
	price = int(price)

	return price

# Get data from a single detail page view
def get_details(url):

	details = {}
	details['url'] = url

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
	price = price_str_to_int(price)
	details['price'] = price

	dt = info_div.find_all('dt', class_ = 'property-attributes-table__label')
	dd = info_div.find_all('dd', class_ = 'property-attributes-table__value')

	dt = [x.text.strip() for x in dt]
	dd = [x.text.strip() for x in dd]

	dt = dt[:-1]
	dd = dd[:-1]

	attributes = {key: value for key, value in zip(dt, dd)}
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


# Get details of multiple properties found on a given a list of detail page urls
def get_details_multiple(lst_details_urls, sleep_time = 2):

	# Adding details for the first property
	details = get_details(lst_details_urls[0])
	details = {key: [value] for key, value in details.items()}
	df = pd.DataFrame.from_dict(details)

	# Adding details for the rest of the properties
	for i, details_url in enumerate(lst_details_urls[1:]):

		details = get_details(details_url)
		df = df.append(details, ignore_index = True)
		time.sleep(random.uniform(0, sleep_time))

	return df


# Scraping the sold prices from the sold page (containing a list of properties)
def sold_price(sold_page_url):

	page = requests.get(sold_page_url)
	results = BeautifulSoup(page.content, 'html.parser')

	locations = results.find_all('div', class_ = 'sold-property-listing__location')
	sizes = results.find_all('div', class_ = 'sold-property-listing__size')
	prices = results.find_all('div', class_ = 'sold-property-listing__price')

	location_lst = []
	size_lst = []
	price_lst = []
	i = 0

	for location, size, price in zip(locations, sizes, prices):

		#print('location = \n', location)
		#print('----------------------------------------')
		#print('size = \n', size)
		#print('----------------------------------------')
		#print('price = \n', price)
		#print('----------------------------------------')

		location_lst.append(location.find('span', class_ = 'item-result-meta-attribute-is-bold item-link').text)
		size_lst.append(size.find('div', class_ = 'sold-property-listing__subheading sold-property-listing--left').text)
		price_lst.append(price.find('span', class_ = 'sold-property-listing__subheading sold-property-listing--left').text)

	#print(len(location_lst), location_lst)
	#print(len(size_lst), size_lst)
	#print(len(price_lst), price_lst)

	sold_dict = {'location': location_lst, 'size': size_lst, 'price': price_lst}

	df = pd.DataFrame(sold_dict)
	df['size'] = df['size'].apply(lambda x: unicodedata.normalize('NFKD', x))
	#print(df.info())
	#print(df.head())

	df['size'] = df['size'].apply(lambda x: x.split()[0])
	df['price'] = df['price'].apply(price_str_to_int)

	return df


# Given a url of either search page overview or sold page overview, the number of pages is returned
def get_num_pages(url):

	# Finding the number of pages with results in the search page view
	page = requests.get(url)
	results = BeautifulSoup(page.content, 'html.parser')
	pagination_div = results.find('div', class_ = 'pagination')

	try:

		pages = pagination_div.find_all('a', class_ = 'button')
		pages = [page.text for page in pages]
		if pages[-1] == 'Nästa':
			pages = pages[:-1]
		pages = [int(page) for page in pages]
		pages = max(pages)
		print('[INFO] Number of pages = ', pages)

	except:

		pages = 1
		print('[INFO] Only one page with results')

	return pages


url = 'https://www.hemnet.se/salda/bostader?item_types%5B%5D=bostadsratt&location_ids%5B%5D=17989&page=1'
url = 'https://www.hemnet.se/bostader?location_ids%5B%5D=17989'
p = get_num_pages(url)
print('Pages = ', p)

if __name__ == '__main__':

	url = 'https://www.hemnet.se/bostader?location_ids%5B%5D=17989&item_types%5B%5D=bostadsratt'

	# # Finding the number of pages with results in the search page view
	# page = requests.get(url)
	# results = BeautifulSoup(page.content, 'html.parser')
	# pagination_div = results.find('div', class_ = 'pagination')

	# try:

	# 	pages = pagination_div.find_all('a', class_ = 'button')
	# 	pages = [page.text for page in pages]
	# 	if pages[-1] == 'Nästa':
	# 		pages = pages[:-1]
	# 	pages = [int(page) for page in pages]
	# 	pages = max(pages)
	# 	print('[INFO] Number of pages = ', pages)

	# except:

	# 	pages = 1
	# 	print('[INFO] Only one page with results')

	# lst_details_urls = []
	# t0 = time.time()

	# for page in range(1, pages+1):

	# 	if page > 1:
	# 		break

	# 	print(page)
	# 	url_w_page = f'{url}&page={page}'
	# 	print(url_w_page)
	# 	lst_details_urls.extend(get_urls_detail_pages(url_w_page))


	# df = get_details_multiple(lst_details_urls, sleep_time = 3)
	# t1 = time.time()

	# # Find position of column 'Pris/m^2' and rename the it
	# matches = [re.match('Pris', x) is not None for x in list(df.columns)]
	# index = matches.index(True)
	# df.rename(columns = {df.columns[index]: 'Kvadratmeterpris'}, inplace = True)

	# t_tot = t1-t0
	# print('Time taken = ', t_tot)
	# print(df.head())

	# path = '/py_scripts/df.pkl' # Path inside the docker container, to which a volume has been mounted
	# # df.to_pickle(path)

	
	# ### Getting sold prices ###
	# sold_page_url = 'https://www.hemnet.se/salda/bostader?location_ids%5B%5D=17989'
	# df_sold = sold_price(sold_page_url)
	# print(df_sold)
	# path_sold = '/'.join(path.split('/')[:-1]) + '/' + 'df_sold.pkl' # Creates a path in the same directory as path with the name df_sold
	# df_sold.to_pickle(path_sold)