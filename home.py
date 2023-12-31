import requests
import json
import time
from Flat import Flat
from datetime import datetime

urls = [
# 'https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=15&region_id=6&filter_float_m%3Afrom=29&filter_float_m%3Ato=42&filter_float_price%3Afrom=500&filter_float_price%3Ato=1301&sort_by=filter_float_price%3Aasc',
# 'https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=15&region_id=13&filter_float_m%3Afrom=29&filter_float_m%3Ato=42&filter_float_price%3Afrom=500&filter_float_price%3Ato=1301&sort_by=filter_float_price%3Aasc',
'https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=15&region_id=4&filter_float_m%3Afrom=29&filter_float_m%3Ato=42&filter_float_price%3Afrom=500&filter_float_price%3Ato=2101&sort_by=filter_float_price%3Aasc'


# 'https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=15&region_id=4&filter_float_m%3Afrom=29&filter_float_m%3Ato=42&filter_float_price%3Afrom=500&filter_float_price%3Ato=1200&sort_by=filter_float_price%3Aasc'
# 'https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=15&region_id=2&city_id=17871&filter_float_m%3Afrom=29&filter_float_m%3Ato=42&filter_float_price%3Ato=3000&&sort_by=filter_float_price%3Aasc'
]

idxg = 1

# slaskie region_id=6
# malopolskie id 4
#swietok id 13


# userid 
#db?
# old prices varsav:
# /api/v1/offers/metadata/search/?offset=0&limit=40&category_id=15&region_id=2&city_id=17871&filter_refiners=spell_checker&facets=%5B%7B%22field%22%3A%22district%22%2C%22fetchLabel%22%3Atrue%2C%22fetchUrl%22%3Atrue%2C%22li
#krk id 8959

def filter(flat):
	rent = flat.price.rent
	price = flat.price.price
	lat = flat.region.lat
	lon = flat.region.lon

	# if rent == 'no data':
	# 	return False

	# if float(rent) + float(price) > 1500:
	# 	return False

	# if lat > 50.6 or lat < 49.8 or lon < 19.3 or lon > 21:
	# 	return False

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

	for home in homes:
		userId = home['user']['id']
		adId = home['id']
		url = home['url']
		city = home['location']['city']['name']
		region = home['location'].get('region').get('name') or 'no region'
		regionId = home['location'].get('region').get('id') or 'no reg id'


		description = home['description']
		promoted = home['promotion']['highlighted']
		urgent = home['promotion']['urgent']

		lat = home['map'].get('lat') or '-'
		lon = home['map'].get('lon') or '-'

		photos = [photo['link'].split(';')[0] for photo in home['photos']]
		photos = photos[:3]

		price = 0
		previousPrice = 0
		size = 0

		params = home['params']

		for param in params:
			if param['key'] == 'price':
				price = param['value']['value']

		previousPrice = next((item['value']['previous_value'] for item in params if item.get('key') == 'price'), '-')
		rent = next((item['value']['key'] for item in params if item.get('key') == 'rent'), 'no data')
		size = next((item['value']['key'] for item in params if item.get('key') == 'm'), 'no size')


		flat = Flat(city = city, regionName = region, regionId = regionId, price= price, rent = rent, size = size, previousPrice = previousPrice, promoted= promoted, urgent = urgent, lat = lat, lon= lon, url = url, userId = userId, adId = adId, description = description, photos = photos)

		if filter(flat) == False:
			continue

		if urgent:
			print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

		if checkAdUnique(flat) == False:
			continue

		flats.append(flat)

		idx += 1

	idxg = idx

	return data


flats = []
uniqueUrls = set()

for urlId, url in enumerate(urls):
	
	data = checkHomes(url, idxg)
	available = data.json()['metadata']['visible_total_count']
	print("total ads for region: " + str(available))

	nextLink = data.json()['links']['next'].get('href') or 'finito'
	url = nextLink

	if url != 'finito':
		while idxg <= available:
			data = checkHomes(url, idxg)
			
			nextLink = data.json()['links'].get('next') or 'finito'
			
			if nextLink == 'finito':
				print('hit ads limit')
				break;

			url = nextLink.get('href')

			time.sleep(1)

sortedFlats = sorted(flats, key=lambda flat: flat.region.lat, reverse=True)

regions = {2: [], 4:[], 6:[], 13:[]}

for flat in sortedFlats:
	regions[flat.region.regionId].append(flat.toDict())

jsonRegions = json.dumps(regions, indent = 2, ensure_ascii=False)

print(len(uniqueUrls))

date = datetime.today().strftime('%Y-%m-%d')

with open('malopol_' + date + '_img.txt', 'w+', encoding='utf-8') as file:
	file.write(jsonRegions)




