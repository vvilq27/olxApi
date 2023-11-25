import requests
import json
import time
from Flat import Flat

url2 = 'https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=15&filter_float_m%3Afrom=29&filter_float_m%3Ato=42&filter_float_price%3Afrom=500&filter_float_price%3Ato=1301&filter_refiners=spell_checker&suggest_filters=true&sl=186a1f64a04x51a512d9'
url = 'https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=15&region_id=4&filter_float_m%3Afrom=29&filter_float_m%3Ato=42&filter_float_price%3Afrom=500&filter_float_price%3Ato=1301'

urls = [
'https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=15&region_id=6&filter_float_m%3Afrom=29&filter_float_m%3Ato=42&filter_float_price%3Afrom=500&filter_float_price%3Ato=1301',
'https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=15&region_id=13&filter_float_m%3Afrom=29&filter_float_m%3Ato=42&filter_float_price%3Afrom=500&filter_float_price%3Ato=1301',
'https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=15&region_id=4&filter_float_m%3Afrom=29&filter_float_m%3Ato=42&filter_float_price%3Afrom=500&filter_float_price%3Ato=1301'
]

idxg = 1

# slaskie region_id=6
# malopolskie id 4
#swietok id 13

# userid + region
#remove duplicates
#db?
# old prices varsav


def filter(flat):
	rent = flat.rent
	price = flat.price
	lat = flat.lat
	lon = flat.lon

	if rent == 'no data':
		return False

	# if float(rent) + float(price) > 1200:
	# 	return False

	if lat > 51.6 or lat < 49.8 or lon < 19.3 or lon > 21:
		return False

	return True

def checkAdUnique(flat):
	global uniqueUrls

	if flat.url in uniqueUrls:
		return False
	else:
		uniqueUrls.add(flat.url)


def checkHomes(url, idx):
	global idxg
	global flats
	

	data = requests.get(url)
	homes = data.json()['data']

	print("homes amnt: " + str(len(homes)))

	with open('homesData2.txt', 'a+') as file:

		for home in homes:
			url = home['url']
			city = home['location']['city']['name']
			region = home['location'].get('region').get('name') or 'no region'
			regionId = home['location'].get('region').get('id') or 'no reg id'


			promoted = home['promotion']['highlighted']
			urgent = home['promotion']['urgent']

			lat = home['map'].get('lat') or '-'
			lon = home['map'].get('lon') or '-'

			price = 0
			previousPrice = 0
			size = 0

			params = home['params']

			for param in params:
				if param['key'] == 'price':
					price = param['value']['value']

			previousPrice = next((item['value']['previous_value'] for item in params if item.get('key') == 'price'), None)

			rent = next((item['value']['key'] for item in params if item.get('key') == 'rent'), 'no data')

			if any(item.get('key') == 'm' for item in params):
				size = next((item['value']['key'] for item in params if item.get('key') == 'm'), None)


			flat = Flat(city, region, regionId, price, rent, size, previousPrice, promoted, urgent, lat, lon, url)

			if filter(flat) == False:
				continue

			if urgent:
				print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

			if checkAdUnique(flat) == False:
				continue

			flats.append(flat)

			idx += 1

			# file.write(record)

	idxg = idx

	return data

flats = []
uniqueUrls = set()

data = checkHomes(url, idxg)
available = data.json()['metadata']['visible_total_count']

nextLink = data.json()['links']['next'].get('href') or 'finito'
url = nextLink

if url != 'finito':
	while idxg <= available:
		data = checkHomes(url, idxg)
		
		nextLink = data.json()['links'].get('next') or 'finito'
		
		if nextLink == 'finito':
			break;

		url = nextLink.get('href')

		time.sleep(0.5)



sortedFlats = sorted(flats, key=lambda x: x.lat, reverse=True)

for idx, flat in enumerate(sortedFlats):
	print(idx, end = ". ")
	print(flat)
	print(flat.lat)
	print(flat.lon)
	print()

print("total records: " + str(available))


