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

	def __str__(self):
		return f"""\t\"name\": {self.region},
	\"city\": {self.city},
	\"lat\": {self.lat},
	\"lon\": {self.lon},
	\"regionId\": {self.regionId}"""

class Price:
	def __init__(self, price, rent, size, previousPrice, promoted, urgent):
		self.price = price
		self.rent = rent
		self.size = size
		self.previousPrice = previousPrice
		self.promoted = promoted
		self.urgent = urgent

	def toDict(self):
		return {
			"price": self.price,
			"rent": self.rent,
			"size": self.size,
			"previousPrice": self.previousPrice,
			"promoted": self.promoted,
			"urgent": self.urgent
		}

	def __str__(self):
		return f"""\t\"price\": {self.price},
	\"rent\": {self.rent},
	\"size\": {self.size},
	\"previousPrice\": {self.previousPrice},
	\"promoted\": {self.promoted},
	\"urgent\": {self.urgent}"""


class Flat:
	def __init__(self, city = '', regionName = '', regionId = '', price= '', rent= '', size= '', previousPrice= '', promoted= '', urgent= '', lat= '', lon= '', url= '', description = '', json = None):

		self.region = Region(city, regionName, regionId, lat, lon)
		self.price = Price(price, rent, size, previousPrice, promoted, urgent)

		self.url = url
		self.description = description

		if json != None:
			jsonRegion = json.get('region')
			jsonPricing = json.get('pricing')

			self.region = Region(jsonRegion.get('city'), jsonRegion.get('name'), jsonRegion.get('regionId'),
                        jsonRegion.get('lat'), jsonRegion.get('lon'))

			self.price = Price(jsonPricing.get('price'), jsonPricing.get('rent'), jsonPricing.get('size'),
                        jsonPricing.get('previousPrice'), jsonPricing.get('promoted'),  jsonPricing.get('urgent'))



	def __str__(self):
		return "{\n\"region\": {\n" + f"{self.region}" + "\n}," +\
		"\n\"price\": {\n" + f"{self.price}" + "\n}\n}" 

	def toDict(self):
			return {
				"region" : self.region.toDict(),
				"pricing": self.price.toDict()
			}


	def getTotalPrice(self):
		return int(self.price.price) + int(self.price.rent);


