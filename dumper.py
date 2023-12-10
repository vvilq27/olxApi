import requests
import json
import time
from Flat import Flat
from datetime import datetime
from correctFile import correctFile
import os


# &distance=15 for area search
# /api/v1/offers/?offset=0&limit=40&category_id=14&region_id=6&city_id=7691&distance=15&sort_by=filter_float_price%3Aasc&filter_float_m%3Afrom=25&filter_float_m%3Ato=35
urls = [
#slaske
# 'https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=15&region_id=6&filter_float_price%3Afrom={}&sort_by=filter_float_price%3Aasc'	
#slaske
# 'https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=15&region_id=6&filter_float_m%3Afrom=25&filter_float_m%3Ato=45&filter_float_price%3Afrom={}&sort_by=filter_float_price%3Aasc'		
#swietok
# 'https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=15&region_id=13&filter_float_m%3Afrom=25&filter_float_m%3Ato=45&filter_float_price%3Afrom={}&sort_by=filter_float_price%3Aasc',	
#malop
# 'https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=15&region_id=4&filter_float_price%3Afrom={}&sort_by=filter_float_price%3Aasc'

# krk
# 'https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=15&region_id=4&city_id=8959&sort_by=filter_float_price%3Aasc&filter_float_m%3Afrom=25&filter_float_m%3Ato=45&filter_float_price%3Afrom={}'
# krk
# 'https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=15&region_id=4&city_id=8959&sort_by=filter_float_price%3Aasc&filter_float_price%3Afrom={}'


# wwa
# 'https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=15&region_id=2&city_id=17871&filter_float_m%3Afrom=25&filter_float_m%3Ato=42&filter_float_price%3Afrom={}&sort_by=filter_float_price%3Aasc' # wawa

# mieszkania kupno
#kato
# 'https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=14&region_id=6&city_id=7691&distance=30&sort_by=filter_float_price%3Aasc&filter_float_m%3Afrom=25&filter_float_m%3Ato=40&&filter_float_price%3Afrom={}'
#wwa
# 'https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=14&region_id=2&city_id=17871&sort_by=filter_float_price%3Aasc&&filter_float_price%3Afrom={}'
# krk
# 'https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=14&region_id=2&city_id=17871&sort_by=filter_float_price%3Aasc&&filter_float_price%3Afrom={}'

]

dictUrls = {
	'buy_krk':'https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=14&region_id=4&city_id=8959&sort_by=filter_float_price%3Aasc&&filter_float_price%3Afrom={}',
	'buy_katw_radius30':'https://www.olx.pl/api/v1/offers/?offset=0&limit=40&category_id=14&region_id=6&city_id=7691&distance=30&sort_by=filter_float_price%3Aasc&filter_float_price%3Afrom={}',
	# 'buy_piotrkw_radius50':'https://www.olx.pl/api/v1/offers?offset=0&limit=40&category_id=14&region_id=7&city_id=13573&distance=50&sort_by=filter_float_price%3Aasc&&filter_float_price%3Afrom={}'
}


fromPrice = 40000

date = datetime.today().strftime('%Y-%m-%d')
uniqueAdIds = set()
total = 0

path = 'data/buy/' + date

if not os.path.exists(path):
	os.mkdir(path)


for url in list(ductUrls.values()):
	# url = next(iter(dictUrls.values()), None)
	data = requests.get(url.format(fromPrice))
	total = data.json()['metadata']['visible_total_count']
	print(total)

	fileName = next(iter(dictUrls.keys()))
	fileName = 'data/buy/' + date + "/" + fileName + "_" + date + '.txt'

	with open(fileName, 'w+', encoding='utf-8') as file:
		for urlKey in dictUrls:
			urlFormated = dictUrls[urlKey].format(fromPrice)

			print(".")
			while urlFormated != 'finito':
				print(".", end = '')
				data = requests.get(urlFormated)

				if len(data.json()['data']) == 0:
					print('\nno more flats in this area')
					break;

				flat = data.json()['data'][-1] 
				lastPrice = next((item['value']['value'] for item in flat['params'] if item.get('key') == 'price'), 'no data')

				flats = data.json()['data']

				idxToPop = []
				for idx, flat in enumerate(flats):
					adId = flat['id']

					if adId in uniqueAdIds:
						idxToPop.append(idx)
					else:
						uniqueAdIds.add(adId)

				for idx,i in enumerate(idxToPop):
					flats.pop(i - idx) # taking care of index shifting after pop 

				# 				TODO
				# each dump is put in its own [] need to be fixed
				# collect all flats and in the end dump them all
				json.dump(flats, file, indent=2)

				nextLink = data.json()['links'].get('next') or 'finito'
				
				if nextLink == 'finito':
					print("\nregion last price: " + str(lastPrice))
					print("last link: \n" + data.json()['links'].get('self').get('href'))

					localTotal = data.json()['metadata']['visible_total_count']
					print("remaining flats: " + str(localTotal))
					if localTotal < 1000:
						lastPrice += 1

					urlFormated = dictUrls[urlKey].format(lastPrice)
					print("get link with updated price: \n" + urlFormated)
					continue

				urlFormated = nextLink.get('href')

				time.sleep(1)

	print(total)
	# print(uniqueAdIds)
	print(len(uniqueAdIds))

	correctFile(fileName)