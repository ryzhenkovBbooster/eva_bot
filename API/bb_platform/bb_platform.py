import json
import os

import requests

from dotenv import load_dotenv

from API.google.googleDirectory import generate_password

load_dotenv()

API_KEY = os.getenv("BBPLATFORM")

def create_user_in_bb(data: dict):
    url = 'https://api-my.bbooster.io/api/v1/external/user'
    headers = {
        'Content-Type': 'application/json',
        "X-Api-Key": API_KEY
    }
    password = generate_password()
    body = {
            "companyKey": "3b59fc28-90e1-466a-8ccc-c35b12ab6444",
            "email": data['email'],
            "password": password,
            "firstName": data['firstName'],
            "lastName": data['lastName'],
            "phoneNumber": "11111111112",
            "telegram": 'https://t.me/' + data['username'],

    }
    response = requests.post(url, data=json.dumps(body), headers=headers )
    print(data['email'], password)
    if response.status_code == 200:
        return {
            'email': data['email'],
            'password': password
        }
    else:
        return False




def delete_user_in_bb(data: dict):
    url = 'https://api-my.bbooster.io/api/v1/external/user'
    headers = {
        'Content-Type': 'application/json',
        "X-Api-Key": API_KEY
    }
    data = {
  "companyKey": "3b59fc28-90e1-466a-8ccc-c35b12ab6444",
  "email": data['create_email']
}
    response = requests.delete(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        return True
    return  False
