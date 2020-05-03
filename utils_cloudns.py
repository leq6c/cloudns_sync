import cloudns_api as capi
from cloudns_api.parameters import Parameters
import requests

def CloudnsUpdateRecordsBindFormat(domain, content):
	url = "https://api.cloudns.net/dns/records-import.json"
	dic = dict()
	dic["domain-name"] = domain
	dic["format"] = "bind"
	dic["content"] = content
	dic["delete-existing-records"] = 1
	params = Parameters(dic)
	res = requests.post(url, params=params.to_dict())
