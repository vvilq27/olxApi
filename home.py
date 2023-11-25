import requests
import json
import time
from Flat import Flat

url2 = 'https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=15&filter_float_m%3Afrom=29&filter_float_m%3Ato=42&filter_float_price%3Afrom=500&filter_float_price%3Ato=1301&filter_refiners=spell_checker&suggest_filters=true&sl=186a1f64a04x51a512d9'
url = 'https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=15&region_id=4&filter_float_m%3Afrom=29&filter_float_m%3Ato=42&filter_float_price%3Afrom=500&filter_float_price%3Ato=1301'

urls = [
'https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=15&region_id=6&filter_float_m%3Afrom=29&filter_float_m%3Ato=42&filter_float_price%3Afrom=500&filter_float_price%3Ato=1301',
'https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=15&region_id=4&filter_float_m%3Afrom=29&filter_float_m%3Ato=42&filter_float_price%3Afrom=500&filter_float_price%3Ato=1301'
]

idxg = 1

# slaskie region_id=6
# malopolskie id 4

# userid + region
#remove duplicates
#db?
# old prices varsav


def checkHomes(url, idx):
	global idxg

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

			if rent == 'no data':
				continue

			if float(rent) + float(price) > 1200:
				continue

			if lat > 51.6 or lat < 49.8:
				continue

			if any(item.get('key') == 'm' for item in params):
				size = next((item['value']['key'] for item in params if item.get('key') == 'm'), None)

			flat = Flat(city, region, regionId, price, rent, size, previousPrice, promoted, urgent, lat, lon, url)

			if urgent:
				print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

			print(idx, end = ". ")
			print(flat)
			# print(str(lat) + " n " + str(lon) + " e")
			print()
			idx += 1

			# file.write(record)

	idxg = idx

	return data


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

			

print("total records: " + str(available))


