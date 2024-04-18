# import libraries
import requests
import itertools
import json

# url given from case_study
api = 'https://www.common.com/cmn-api/listings/common'


# function which pull data from an api url
def pull_data(api_url):
	response = requests.get(api_url)
	return response.json()


# run the pull_data function
data_p = pull_data(api)


# create Class for Property
class Property:
	def __init__(self, property_id, name, marketing_name, currency_code, full_address, street_address, city, state_code,
	             postal_code, country_code, longitude, latitude,
	             belonged_city, description, neighborhood_name, neighborhood_description):
		self.property_id = property_id
		self.name = name
		self.marketing_name = marketing_name
		self.currency_code = currency_code
		self.full_address = full_address
		self.street_address = street_address
		self.city = city
		self.state_code = state_code
		self.postal_code = postal_code
		self.country_code = country_code
		self.longitude = longitude
		self.latitude = latitude
		self.belonged_city = belonged_city
		self.description = description
		self.neighborhood_name = neighborhood_name
		self.neighborhood_description = neighborhood_description


# create Class for Unit
class Unit:
	def __init__(self, unit_id, property_id, room_number, bedrooms, listing_sqft, unit_sqft,
	             occupancy_type, availability_date, minimum_stay, minimum_price, maximum_price):
		self.unit_id = unit_id
		self.property_id = property_id
		self.room_number = room_number
		self.bedrooms = bedrooms
		self.listing_sqft = listing_sqft
		self.unit_sqft = unit_sqft
		self.occupancy_type = occupancy_type
		self.availability_date = availability_date
		self.minimum_stay = minimum_stay
		self.minimum_price = minimum_price
		self.maximum_price = maximum_price


# create Class for Pricing
class Pricing:
	def __init__(self, unit_id, name, months, amount, concession_description):
		self.unit_id = unit_id
		self.name = name
		self.months = months
		self.amount = amount
		self.concession_description = concession_description


# create Class for Fee
class Fee:
	def __init__(self, unit_id, name, description, amount, is_mandatory, is_refundable):
		self.unit_id = unit_id
		self.name = name
		self.description = description
		self.amount = amount
		self.is_mandatory = is_mandatory
		self.is_refundable = is_refundable


# function which parses each item and transforms it from raw API data into structured data
def transform_data(data):
	# create empty lists to put data
	properties = []
	units = []
	pricings = []
	fees = []

	# go through item in data and parse
	# items are semi-structured data
	for item in data:
		try:
			# find the sub-dictionaries for parsing to other classes
			addr_dict = item.get('address', {})
			pricing_data = item.get('pricing', {})

			# create instance of Property class
			prop = Property(
				property_id=item.get('propertyId', ''),
				name=item.get('propertyName', ''),
				marketing_name=item.get('marketingName', ''),
				currency_code=item.get('currencyCode', ''),
				full_address=addr_dict.get('fullAddress', ''),
				street_address=addr_dict.get('streetAddress', ''),
				city=addr_dict.get('city', ''),
				state_code=addr_dict.get('stateCode', ''),
				postal_code=addr_dict.get('postalCode', ''),
				country_code=addr_dict.get('countryCode', ''),
				latitude=addr_dict.get('latitude', 0),
				longitude=addr_dict.get('longitude', 0),
				belonged_city=addr_dict.get('belongedCity', ''),
				description=item.get('description', ''),
				neighborhood_name=item.get('neighborhood', ''),
				neighborhood_description=item.get('neighborhoodDescription', '')
			)
			properties.append(prop)

			# create instance of Unit class
			unit = Unit(
				unit_id=item.get('id', ''),
				property_id=item.get('propertyId', ''),
				room_number=addr_dict.get('roomNumber', ''),
				bedrooms=item.get('bedrooms', 0),
				listing_sqft=item.get('listingSqft', 0),
				unit_sqft=item.get('unitSqft', 0),
				occupancy_type=item.get('occupancyType', ''),
				availability_date=item.get('availableDate', ''),
				minimum_stay=pricing_data.get('minimumStay', 0),
				minimum_price=pricing_data.get('minimumPrice', 0),
				maximum_price=pricing_data.get('maximumPrice', 0),
			)
			units.append(unit)

			# create instance of Pricing class
			for pricing_item in pricing_data.get('monthlyPricing', []):
				pricing = Pricing(
					unit_id=item.get('id', ''),
					name=pricing_item.get('name', ''),
					months=pricing_item.get('months', 0),
					amount=pricing_item.get('amount', 0),
					concession_description=pricing_item.get('concessionsApplied', [])
				)
				pricings.append(pricing)

			# create instance of Fees class
			for fee_item in item.get('fees', []):
				fee = Fee(
					unit_id=item.get('id', ''),
					name=fee_item.get('name', ''),
					description=fee_item.get('description', ''),
					amount=fee_item.get('amount', 0),
					is_mandatory=fee_item.get('isMandatory', False),
					is_refundable=fee_item.get('isRefundable', False)
				)
				fees.append(fee)

		# error handling
		except KeyError as e:
			print(f"Missing key in data: {e}")

	return properties, units, pricings, fees


# run the transform_data function
data_t = transform_data(data_p)

# convert the tuple of lists into a list of lists
# so it can be serialized
data_t = list(itertools.chain(*data_t))


# serialize the data in json format
def serialize_to_json(data, filename):
	with open(filename, 'w') as f:
		json.dump([obj.__dict__ for obj in data], f, indent=4)


# run the serialize_to_json function
# specifying the tmp folder so people without permission can write to the Docker container
serialize_to_json(data_t, 'output/results.json')
