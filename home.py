import requests
import json
import time



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

			# for param in params:
			# 	if param['key'] == 'rent':
			# 		rent = param['value']['key']

			# if rent == -1:
			# 	isRentIncluded = any(item.get('key') == 'rent' for item in params)
			# 	if isRentIncluded == False:
			# 		#print(json.dumps(params, indent=1))
			# 		rent = 'no data'

			if any(item.get('key') == 'm' for item in params):
				size = next((item['value']['key'] for item in params if item.get('key') == 'm'), None)
			
			record = str(idx) + ". " + city + " " + " " + region + "[" + str(regionId) + "]\n" + \
			str(price) + "\t" + str(rent)+ "\t" + str(size) + "\t" + str(previousPrice) + "\t" + str(promoted) + "\t" + str(urgent) + \
			"\n" + url + "\n"

			if urgent:
				print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
				print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
				print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

			print(record)
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


