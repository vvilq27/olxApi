import json
from Flat import Flat
import statistics
import sys

filterFlats = True
filterFlats = False

def buildFlat(home):
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


	return Flat(city = city, regionName = region, regionId = regionId, price= price, rent = rent, size = size, previousPrice = previousPrice, promoted= promoted, urgent = urgent, lat = lat, lon= lon, url = url, description = description)

def filterFlat(flat, sizeFrom = 0, sizeTo = 222):
	size = float(flat.price.size)

	if size < sizeFrom or size > sizeTo:
		return False

	# if flat.region.city == "\u0141\u00f3d\u017a":
	# 	return False

	return True


# replace in file:
#   }
# ][
#   {

#   },
#   {

data = None

fileName = sys.argv[1]
print(fileName)

with open(fileName, "r", encoding= 'utf-8') as file:
	data = file.read()

jsonData = json.loads(data)

j = jsonData
prices = []

for jsonFlat in j:
	flat = buildFlat(jsonFlat)
	if filterFlats and not filterFlat(flat, 25, 45):
		continue
	prices.append(flat.price.price)

sortedPrices = sorted(prices, key=lambda price: price)
median = sortedPrices[int(len(sortedPrices)/2)]

print(median)
print(len(sortedPrices))
print(sortedPrices[:30])
print()
print(sortedPrices[-30:])
