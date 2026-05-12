import requests
import boto3


url = "http://98.82.174.234:5000"


res = requests.get(url+'/api/headers')
print(res.json())
print(res.status_code)
