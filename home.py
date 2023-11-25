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

	if float(rent) + float(price) > 1400:
		return False

	if lat > 50.6 or lat < 49.8 or lon < 19.3 or lon > 21:
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

	for home in homes:
		url = home['url']
		city = home['location']['city']['name']
		region = home['location'].get('region').get('name') or 'no region'
		regionId = home['location'].get('region').get('id') or 'no reg id'


		description = home['description']
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

		previousPrice = next((item['value']['previous_value'] for item in params if item.get('key') == 'price'), '-')
		rent = next((item['value']['key'] for item in params if item.get('key') == 'rent'), 'no data')
		size = next((item['value']['key'] for item in params if item.get('key') == 'm'), 'no size')


		flat = Flat(city, region, regionId, price, rent, size, previousPrice, promoted, urgent, lat, lon, url, description)

		if filter(flat) == False:
			continue

		if urgent:\

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
	
	match urlId:
		case 0:
			print('[malopolskie]')
		case 1:
			print('[swietokrzyskie]')
		case 2:
			print('[slaskie]')

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
				break;

			url = nextLink.get('href')

			time.sleep(0.5)


# sortedFlats = sorted(flats, key=lambda flat: flat.regionId)
sortedFlats = sorted(flats, key=lambda flat: flat.lat, reverse=True)

regions = {4:[], 6:[], 13:[]}

for flat in sortedFlats:
	regions[flat.regionId].append(flat)

with open('homesData2.txt', 'a+', encoding='utf-8') as file:

	for r in regions:
		print('\n\n')
		for id, flat in enumerate(regions[r]):
			print(str(id) + ". ", end= "")
			print(flat)
			print()

			file.write(str(id) + ". ")
			file.write(flat.__str__())
			file.write("\n\n")




