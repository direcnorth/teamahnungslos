import requests
import json
from alarm import Alarm
import datetime

class HttpEquipment:

	thing = "TEAM2"

	url_auth = "https://fabeagleiot.ais-automation.com/ords/C16818_006/cloudconnect/oauth/token"
	url_ping = "https://fabeagleiot.ais-automation.com/ords/C16818_006/cloudconnect/api/monitoring/v1/ping"
	url_alarms = "https://fabeagleiot.ais-automation.com/ords/C16818_006/cloudconnect/api/monitoring/v1/things/{}/alarms".format(thing)
	url_events = "https://fabeagleiot.ais-automation.com/ords/C16818_006/cloudconnect/api/monitoring/v1/things/{}/events".format(thing)
	url_process_value = "https://fabeagleiot.ais-automation.com/ords/C16818_006/cloudconnect/api/monitoring/v1/things/{}/processdata".format(thing)
	
	cred = "aHNqZ0F0WEZ2c01tNmtnU19xaFU3dy4uOno1VElvekRFMkFkaGVCRW11VVBLZEEuLg=="
	
	def get_time(self):
		return datetime.datetime.now().isoformat()
	
	def ping(self):
		headers = self.token
		payload = "Ping"
		response = requests.get(self.url_ping, headers=headers, params=payload)
		return response.text
	
	def get_token(self):
		headers = {
			"content-type": "application/x-www-form-urlencoded",
			"authorization": "Basic {}".format(self.cred)
		}
		
		payload = {
			"grant_type": "client_credentials"
		}
		
		response_auth = requests.post(self.url_auth, headers=headers, params=payload)
		
		print(response_auth.text)
		
		response_json = json.loads(response_auth.text)
		
		self.token = {
			"content-type": "application/json",
			"authorization": "Bearer {}".format(response_json["access_token"])
		}

	def post_alarm(self, alarm, action=2):
		headers = self.token
		payload = {
			'id': alarm.value,
			'action': action
		}
		
		return requests.post(self.url_alarms, headers=headers, json=payload).text

	def post_event(self, event):
		headers = self.token
		payload = {
			'id': event
		}
		
		return requests.post(self.url_events, headers=headers, json=payload).text
		
	def post_process_value(self, value):
		headers = self.token
		payload = {
			"data":
				[
					{
						"id": "COUNTER",
						"value": value
					}
				]
		}
		
		return requests.post(self.url_process_value, headers=headers, json=payload).text
