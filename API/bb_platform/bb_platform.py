import json
import os

import requests

from dotenv import load_dotenv, set_key
from datetime import datetime
from API.google.googleDirectory import generate_password

load_dotenv()

API_SECRET = os.getenv("BB_SECRET_TOKEN")
API_KEY = os.getenv("BB_ACCESS_TOKEN")

def refresh_api_token():
    url = 'https://api-my.bbooster.io/api/v1/Authentication/client-credentials'
    headers = {
        'Content-Type': 'application/json'
    }
    body = {
        "clientId": "2",
        "clientSecret": API_SECRET
    }
    try:
        print(f"Attempting to refresh token...")
        response = requests.post(url, json=body, headers=headers)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            new_token = response_data.get('tokenAccess')
            if new_token:
                # Update environment variable in memory
                os.environ["BB_ACCESS_TOKEN"] = new_token
                global API_KEY
                API_KEY = new_token
                # Update .env file
                dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env')
                set_key(dotenv_path, "BB_ACCESS_TOKEN", new_token)
                # Save the last refresh date
                current_time = datetime.now().strftime("%Y-%m-%d")
                set_key(dotenv_path, "LAST_TOKEN_REFRESH", current_time)
                print("API token refreshed successfully")
                return True
            else:
                print("Response doesn't contain tokenAccess:", response_data.keys())
        else:
            print(f"Error refreshing token: {response.status_code}")
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
    
    print("Failed to refresh API token")
    return False

def check_token_expiration():
    dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env')
    last_refresh = os.getenv("LAST_TOKEN_REFRESH")
    print(last_refresh)
    if not last_refresh:
        # If there's no record of last refresh, do it now
        return refresh_api_token()
    
    # Check if 10 days have passed since the last refresh
    last_refresh_date = datetime.strptime(last_refresh, "%Y-%m-%d")
    current_date = datetime.now()
    days_since_refresh = (current_date - last_refresh_date).days
    
    if days_since_refresh >= 10:
        return refresh_api_token()
    
    return True


# Always check if token needs to be refreshed before making API calls
check_token_expiration()

def create_user_in_bb(data: dict):
    check_token_expiration()
    
    url = 'https://api-my.bbooster.io/api/v1/external/user'
    headers = {
        'Content-Type': 'application/json',
        "Authorization": 'Bearer ' + API_KEY
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
    response = requests.post(url, data=json.dumps(body), headers=headers)
    print(data['email'], password)
    print(response.content)
    if response.status_code == 200:
        return {
            'email': data['email'],
            'password': password
        }
    else:
        return False

def delete_user_in_bb(data: dict):
    check_token_expiration()
    
    url = 'https://api-my.bbooster.io/api/v1/external/user'
    headers = {
        'Content-Type': 'application/json',
        "Authorization": 'Bearer ' + API_KEY
    }
    data = {
        "companyKey": "3b59fc28-90e1-466a-8ccc-c35b12ab6444",
        "email": data['create_email']
    }
    response = requests.delete(url, data=json.dumps(data), headers=headers)
    print(response.content)
    if response.status_code == 200:
        return True
    return False