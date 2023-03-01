import requests
import json

def get_openai_key(api_key):
    p = json.dumps({"api_key":api_key}).encode('utf-8')
    openai_key = request.post(requests.post(url, data=p)
    return openai_key
