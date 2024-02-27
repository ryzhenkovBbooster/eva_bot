import json
import base64
import requests



TOKEN = 'uUToRMxPpTUOnu8e2BKv58vsDTyRES5uA6UIPYPVhVQMgnkTjp7ACPihisJT9MTGZe47ciAo3lXneolcQejz9dmA1g9sGzsDuGfq7lCpoH6gh45h2gTrnkCBM9MJZByK'
def createUser_on_skillup(email, name: dict):
    headers = {
        "Accept": "application/json; q=1.0, */*; q=0.1"
    }

    params = {
        'user': {
            "email": email,
            "first_name": name['first'],
            "last_name": name['last'],
            "group_name": ['Тестовая неделя New']
        }
    }
    encoded_params = base64.b64encode(json.dumps(params).encode('utf-8')).decode('utf-8')
    data = {
        "action": "add",
        "key": TOKEN,
        "params": encoded_params
    }

    url = f'https://skill-up.getcourse.ru/pl/api/users'

    responce = requests.post(url=url, data=data, headers=headers)
    if responce.status_code == 200:
        data = json.loads(responce.text)


        if data['result']['user_status'] == 'updated':
            return False
        else:
            return True
    else:
        return False



def update_group_user(email):
    headers = {
        "Accept": "application/json; q=1.0, */*; q=0.1"
    }

    params = {
        'user': {
            "id": 321514174,

            "group_name": ['Тестовая неделя', 'ИС']
        }
    }
    encoded_params = base64.b64encode(json.dumps(params).encode('utf-8')).decode('utf-8')
    data = {
        "action": "update",
        "key": TOKEN,
        "params": encoded_params
    }

    url = f'https://skill-up.getcourse.ru/pl/api/users'

    responce = requests.post(url=url, data=data, headers=headers)
    print(json.loads(responce.text))


# update_group_user('k.ryzhenkov@bbooster.online')