class Region:
	def __init__(self, city, region, regionId, lat, lon):
		self.city = city
		self.region = region
		self.regionId = regionId
		self.lat = lat
		self.lon = lon

	def toDict(self):
		return {
			"name": self.region,
			"city": self.city,
			"lat": self.lat,
			"lon": self.lon,
			"regionId": self.regionId
		}

class Flat:
	def __init__(self, city, regionName, regionId, price, rent, size, previousPrice, promoted, urgent, lat, lon, url,  description = ''):

		self.region = Region(city, regionName, regionId, lat, lon)

		# self.city = city 
		# self.region = region
		# self.regionId = regionId
		self.price = price
		self.rent = rent
		self.size = size
		self.previousPrice = previousPrice
		self.promoted = promoted
		self.urgent = urgent
		# self.lat = lat
		# self.lon = lon
		self.url = url
		self.description = description


	# def toJson(self, previousPrice = '-'):
	# 	return {
	# 		"region":{
	# 			"name": self.region,
	# 			"city": self.city,
	# 			"lat": self.lat,
	# 			"lon": self.lon,
	# 			"regionId": self.regionId
	# 		},
	# 		"pricing":{
	# 			"price": self.price,
	# 			"previousPrice": previousPrice,
	# 			"rent": self.rent,
	# 			"size": self.size,
	# 			"promoted": self.promoted,
	# 			"urgent": self.urgent
	# 		},
	# 		"url": self.url,
	# 		"description": self.description			
	# 	}

	def toDict(self):
		# return f"{self.city}, {self.region} [{self.regionId}]\n" \
		# 	f"{self.price}\t{self.rent}\t{self.size}\tPrevious Price: {self.previousPrice} " \
		# 	f"Promoted: {self.promoted}, Urgent: {self.urgent}\n"\
		# 	f"{self.url}\n" 
		# 	# f">\n{self.description}"

		return {
			"region" : self.region.toDict(),
			"pricing":{
				"price": self.price,
				"previousPrice": self.previousPrice,
				"rent": self.rent,
				"size": self.size,
				"promoted": self.promoted,
				"urgent": self.urgent
			},
		}



