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

	try:

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

	except:
		print(f'Not able to successfully get the details of the property at - {url}')

	return details


# Get details of multiple properties found on a given a list of detail page urls
def get_details_multiple(lst_details_urls, sleep_time = 2, max_per_page = 9999):

	# Adding details for the first property
	details = get_details(lst_details_urls[0])
	details = {key: [value] for key, value in details.items()}
	df = pd.DataFrame.from_dict(details)

	# Adding details for the rest of the properties
	for i, details_url in enumerate(lst_details_urls[1:]):


		# If we just want to test the function, and not extract every single property on the page
		if i > max_per_page:
			break

		details = get_details(details_url)
		df = df.append(details, ignore_index = True)
		time.sleep(random.uniform(0, sleep_time))

	return df


# Scraping the sold prices from the sold page (containing a list of properties)
def get_sold_price(sold_page_url):

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

		location_lst.append(location.find('span', class_ = 'item-result-meta-attribute-is-bold item-link').text)
		size_lst.append(size.find('div', class_ = 'sold-property-listing__subheading sold-property-listing--left').text)
		price_lst.append(price.find('span', class_ = 'sold-property-listing__subheading sold-property-listing--left').text)

	sold_dict = {'location': location_lst, 'size': size_lst, 'price': price_lst}

	df = pd.DataFrame(sold_dict)
	df['size'] = df['size'].apply(lambda x: unicodedata.normalize('NFKD', x))
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

def data_prep(df, type):

	if type == 'active':
		
		df['area'] = df['area'].apply(lambda x: 'Ön' if re.match('(\s|^)(Ön|ön).*', x) else x)
		df['area'] = df['area'].apply(lambda x: re.sub('(,|/|\(|\-).*$', '', x).strip())
		df['Antal rum'] = df['Antal rum'].apply(lambda x: str.split(x)[0])
		df['Boarea'] = df['Boarea'].apply(lambda x: float(str.split(x)[0].replace(',', '.')))
		df['Byggår'] = df['Byggår'].apply(lambda x: x if isinstance(x, str) else 2020)										# Assuming that property without Byggår is newly built
		df['Byggår'] = df['Byggår'].apply(lambda x: x.split('-')[-1] if isinstance(x, str) else x)							# Using the latest year as Byggår
		df['Balkong'] = df['Balkong'] == 'Ja'
		df['Förening'] = df['Förening'].apply(lambda x: re.sub('\n\nOm föreningen', '', x) if isinstance(x, str) else None)
		df['Avgift'] = df['Avgift'].apply(lambda x: price_str_to_int(x) if isinstance(x, str) else -1)
		df['Driftkostnad'] = df['Driftkostnad'].apply(lambda x: price_str_to_int(x) if isinstance(x, str) else -1)
		df['Kvadratmeterpris'] = df['Kvadratmeterpris'].apply(lambda x: price_str_to_int(x) if isinstance(x, str) else -1)
		df['visits'] = df['visits'].apply(lambda x: price_str_to_int(x) if isinstance(x, str) else -1)
		df['days_available'] = df['days_available'].apply(lambda x: price_str_to_int(x) if isinstance(x, str) else -1)
		df['avg_daily_visits'] = df.apply(lambda x: round(x['visits'] / max(1, x['days_available']), 2), axis = 1) 			# Feature engineering

		try:	
			f['Uteplats'] = df['Uteplats'] == 'Ja'

		except:
			print('[INFO] The column Uteplats does not exist')

	elif type == 'sold':

		df['size'] = df['size'].apply(lambda x: float(x.replace(',', '.')))

	return df


if __name__ == '__main__':

	sleep_time = 3
	max_per_page = 2 # Only extracting data from a limited number of properties per page
	t = time.asctime()
	t = t.replace(' ', '-')
	path = f'/py_scripts/dataframes/df_{t}.pkl' # Path inside the docker container, to which a volume has been mounted

	### Start - Scraping the active advertisements ###

	url = 'https://www.hemnet.se/bostader?location_ids%5B%5D=17989&item_types%5B%5D=bostadsratt'
	pages = get_num_pages(url)

	lst_details_urls = []
	t0 = time.time()

	# Getting a list of urls to the detail page for all the pages of the search page url = url
	for page in range(1, pages+1):

		url_w_page = f'{url}&page={page}'
		print(url_w_page)
		lst_details_urls.extend(get_urls_detail_pages(url_w_page))


	df = get_details_multiple(lst_details_urls, sleep_time = sleep_time, max_per_page = max_per_page)
	t1 = time.time()

	# Find position of column 'Pris/m^2' and rename it
	matches = [re.match('Pris', x) is not None for x in list(df.columns)]
	index = matches.index(True)
	df.rename(columns = {df.columns[index]: 'Kvadratmeterpris'}, inplace = True)

	t_tot = t1-t0
	print('Time taken scraping active advertisements = ', t_tot)

	# Formatting the data
	#try:
	#	df = data_prep(df, type = 'active')

	#except:
	#	print('Error in data_prep for dataframe df')

	# Serialization
	df.to_pickle(path)

	### End - Scraping the active advertisements ###

	### Start - Scraping the sold property prices ###

	url_sold = 'https://www.hemnet.se/salda/bostader?item_types%5B%5D=bostadsratt&location_ids%5B%5D=17989'
	pages_sold = get_num_pages(url_sold)


	df_sold = None # Initializing the dataframe used in the following loop
	for page in range(1, pages_sold+1):

		url_sold_w_page = f'{url_sold}&page={page}'

		# First time, create df_sold
		if df_sold is None:
			df_sold = get_sold_price(url_sold_w_page)
			print('First')

		else:
			time.sleep(random.uniform(0, sleep_time))
			df_sold = df_sold.append(get_sold_price(url_sold_w_page), ignore_index = True)
			print('Rest')

	print(df_sold)
	print(df_sold.info())

	# Formatting the data
	#try:
	#	df_sold = data_prep(df_sold, type = 'sold')

	#except:
	#	print('Error in data_prep for dataframe df_sold')

	# Serialization
	path_sold = '/'.join(path.split('/')[:-1]) + '/' + f'df_sold_{t}.pkl' # Creates a path in the same directory as path with the name df_sold
	df_sold.to_pickle(path_sold)

	### End - Scraping the sold property prices ###
	