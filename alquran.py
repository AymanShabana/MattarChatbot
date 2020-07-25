import requests
from playsound import playsound

api_url_base = 'http://api.alquran.cloud/v1/'
cdn_url_base = 'http://cdn.alquran.cloud/media/'

def get_all_reciters():
    api_url = api_url_base + 'edition?format=audio&language=ar'
    response = requests.get(api_url)
    if response.status_code == 200:
        reciters = list()
        for item in response.json()['data']:
            reciters.append(item['name'])
        return reciters
    return None

def get_identifier(reciter):
    api_url = api_url_base + 'edition?format=audio&language=ar'
    response = requests.get(api_url)
    if response.status_code == 200:
        for item in response.json()['data']:
            if reciter == item['name']:
                return item['identifier']
    return None

def get_surah_number(surah):
    api_url = api_url_base + 'surah'
    response = requests.get(api_url)
    if response.status_code == 200:
        for item in response.json()['data']:
            if surah == item['name'][5:]:
                return item['number']
    return None

def get_number_of_ayahs(surah_number):
    api_url = '{0}surah/{1}'.format(api_url_base, surah_number)
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()['data']['numberOfAyahs']
    return None

def get_absolute_ayah_number(surah_number, relative_ayah_number):
    api_url = '{0}ayah/{1}:{2}'.format(api_url_base, surah_number, relative_ayah_number)
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()['data']['number']
    return None

def play_ayah(identifier, absolute_ayah_number):
    playsound('https://cdn.islamic.network/quran/audio/{0}/{1}/{2}.mp3'.format(128, identifier, absolute_ayah_number))
