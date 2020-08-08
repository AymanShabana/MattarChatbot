import requests
from flask import session

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
    aya = 'https://cdn.islamic.network/quran/audio/{0}/{1}/{2}.mp3'.format(64, identifier, absolute_ayah_number)
    if session.get('ayat') is not None:
        session['ayat'] = session['ayat'] + [aya]
    else:
        session['ayat'] = [aya]

def get_tafseer_list():
    api_url = 'http://api.quran-tafseer.com/tafseer/'
    response = requests.get(api_url)
    if response.status_code == 200:
        tafseerList = list()
        bigt=response.json()
        for item in bigt:
            temp = item['name']
            tafseerList.append(temp)
        return tafseerList[0:8]
    return None

def get_tafseer_verse(tafseer_id,sura_number,ayah_number):
    api_url = 'http://api.quran-tafseer.com/tafseer/{0}/{1}/{2}'.format(tafseer_id,sura_number,ayah_number)
    response = requests.get(api_url)
    if response.status_code == 200:
        tafseer = response.json()['text']
        return tafseer
    return None

def get_tafseer_range(tafseer_id,sura_number,ayah_number_from,ayah_number_to):
    tafseer = ''
    for i in range(int(ayah_number_from),int(ayah_number_to)+1):
        tafseer += str(get_tafseer_verse(tafseer_id,sura_number,str(i)))+" "
    return tafseer
