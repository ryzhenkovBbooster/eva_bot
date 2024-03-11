import json

import requests
from dotenv import load_dotenv
import os


load_dotenv()

API = os.getenv('HR_SCANNER')

def post_test_api(email):
    tests = 2


    # email = 'sellcringe@yandex.ru'
    # url = f'https://hrscanner.ru/api/get-vacs?api_key={API}'

    data = {
        'email': email,
        'api_key': API,
        'part': tests
    }

    getUsers = f'https://hrscanner.com/api/create_participant'

    responce = requests.post(getUsers, data=data)

    responce = json.loads(responce.text)
    print(responce)
    try:
        if responce['status'] == 1:
            return responce['test_url']['2']

        return False
    except Exception as err:
        return False
    # responce = responce.json()['participants']

def get_tests(email):

    getUsers = f'https://hrscanner.ru/api/search_participant?email={email}&api_key={API}&part=2,3'
    try:

        responce = requests.get(getUsers)
        if responce.json()['participants']:
            pass
        else:
            return False

    except:

        return False

    responce = responce.json()['participants']
    responce = responce[0]

    if responce['status'] == 'COMPLETED':
        if responce['tests_finish']['TOOLS'] and responce['tests_finish']['LOGIS']:

            tools = responce['tests_finish']['TOOLS'] + '&format=pdf'
            logis = responce['tests_finish']['LOGIS'] + '&format=pdf'

            return (tools, logis)

        else:
            return 'tests is not completed'
    else:
        return 'tests is not completed'

