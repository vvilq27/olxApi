class Flat:
	def __init__(self, city, region, regionId, price, rent, size, previousPrice, promoted, urgent, url):
		self.city = city 
		self.region = region
		self.regionId = regionId
		self.price = price
		self.rent = rent
		self.size = size
		self.previousPrice = previousPrice
		self.promoted = promoted
		self.urgent = urgent
		self.url = url

	def __str__(self):
		return f"City: {self.city}, Region: {self.region}, Region ID: {self.regionId}\n" \
			f"Price: {self.price}, Rent: {self.rent}, Size: {self.size}, " \
			f"Previous Price: {self.previousPrice}, Promoted: {self.promoted}, Urgent: {self.urgent}\n"\
			f"URL: {self.url}"



