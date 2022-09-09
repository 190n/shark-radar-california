import json
import requests
from jinja2 import Template
from datetime import datetime
import time
import pytz

with open("stores.json", encoding='utf-8') as f:
	# Parsed from (search for "allStores=["):
	# https://www.ikea.com/us/en/products/javascripts/range-stockcheck.961382cd6f9231488e60.js
	stores = json.load(f)


def calculate_stock(availability):
	store_id = availability['classUnitKey']['classUnitCode']
	store_name = \
		[store['name'] for store in stores if store['value'] == store_id]
	if len(store_name) < 1:
		return None

	store_name = store_name[0]

	next_restock = None
	try:
		availability_info = availability['buyingOption']['cashCarry']['availability']
		quantity = int(availability_info['quantity'])
		if 'restocks' in availability_info:
			next_restock = availability_info['restocks'][0]
	except KeyError:
		quantity = 0

	return {
		'store': store_name,
		'quantity': quantity,
		'next_restock': next_restock,
	}


def get_availabilities(item_id):
	availabilities = requests.get(f'https://api.ingka.ikea.com/cia/availabilities/ru/us?itemNos={item_id}&expand=StoresList,Restocks,SalesLocations', headers={
		'Accept': 'application/json;version=2',
		'X-Client-ID': 'b6c117e5-ae61-4ef5-b4cc-e0b1e37f0631'
	})
	availabilities = availabilities.json()

	sharks = []
	for availability in availabilities['availabilities']:
		stock = calculate_stock(availability)
		if stock is None:
			continue
		sharks.append(stock)
	# sort by number in stock; stores with the same stock are sorted by closest restock
	sharks.sort(key=lambda s: s['next_restock']['earliestDate'] if s['next_restock'] else 'z')
	sharks.sort(key=lambda s: s['quantity'], reverse=True)
	return sharks

blåhaj_item_id = '90373590'
smolhaj_item_id = '70540665'

def main():
	blåhaj = get_availabilities(blåhaj_item_id)
	smolhaj = get_availabilities(smolhaj_item_id)
	with open('template.html') as template_file:
		template = Template(template_file.read())
		now = datetime.utcnow()
		iso_time = now.isoformat(timespec='milliseconds') + 'Z'
		pacific_time = pytz.timezone('America/Los_Angeles')
		local_datetime = datetime.today().astimezone(pacific_time)
		local_time = f'{local_datetime.strftime("%Y-%m-%d %I:%M:%S %p")} {pacific_time.tzname(datetime.today())}'
		print(template.render(
			iso_time=iso_time,
			local_time=local_time,
			blåhaj=blåhaj,
			smolhaj=smolhaj,
		))


main()
