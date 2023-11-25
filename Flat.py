class Flat:
	def __init__(self, city, region, regionId, price, rent, size, previousPrice, promoted, urgent, lat, lon, url):
		self.city = city 
		self.region = region
		self.regionId = regionId
		self.price = price
		self.rent = rent
		self.size = size
		self.previousPrice = previousPrice
		self.promoted = promoted
		self.urgent = urgent
		self.lat = lat
		self.lon = lon
		self.url = url

	def __str__(self):
		return f"{self.city}, {self.region} [{self.regionId}]\n" \
			f"{self.price}\t{self.rent}\t{self.size}\tPrevious Price: {self.previousPrice} " \
			f"Promoted: {self.promoted}, Urgent: {self.urgent}\n"\
			f"{self.url}"



