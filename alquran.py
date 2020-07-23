import requests

api_url_base = 'http://api.alquran.cloud/v1/'
primary_cdn_url_base = 'http://cdn.alquran.cloud/media/'

def get_all_reciters():
    api_url = api_url_base + 'edition?format=audio&language=ar'
    response = requests.get(api_url)
    if response.status_code == 200:
        reciters = list()
        for item in response.json()['data']:
            reciters.append(item['name'])
        return reciters
    return None
