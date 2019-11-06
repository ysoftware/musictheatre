#!/usr/bin/python

from core import isNewCommand, checkAccess, isNewSeeds, getTime
from session import saveConfig, loadConfig, send, reply, auth
import random
import re
import requests
import json

URL = 'https://history.muffinlabs.com/date'

def load_today():
	return json.loads(requests.get(URL).text)

def renew():

	today_json = load_today()

	today_out = ('')

	# DAT WORKS

	for event in today_json['data']['Events']:
		choice = random.randint(0,15)
		if choice == 1:
			if event['year'] is not None:
				if event['text'] is not None:
					today_out = today_out + ('In year '+event['year']+'-'+event['text']+'\n')

	for birth in today_json['data']['Births']:
			choice = random.randint(0,45)
			if choice == 1:
					if birth['year'] is not None:
							if birth['text'] is not None:
							today_out = today_out + (birth['text']+' was born in '+birth['year']+'\n')

	for death in today_json['data']['Deaths']:
			choice = random.randint(0,25)
			if choice == 1:
			if death['year'] is not None:
						if death['text'] is not None:
							today_out = today_out + ('In year '+death['year']+' died '+death['text']+'\n')

	return today_out

def today(bot, update):
		if not isNewCommand(update):
		return
	message = renew()
	send(bot, message.encode('utf-8'))
