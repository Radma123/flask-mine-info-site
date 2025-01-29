import requests

def get_all_gpts() -> list:
    data = requests.get('http://127.0.0.1:1337/v1/models')

    gpts = []
    for i in data.json()['data']:
        gpts.append(i['id'])

    return gpts
