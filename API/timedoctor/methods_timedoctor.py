import os

import requests

TOKEN = os.getenv("TIME_DOCTOR_API")

def inviteUser(email, name):
    company_id = 'ZVcKbVtuvprvM6lL'
    url = f"https://api2.timedoctor.com/api/1.1/invitations?company={company_id}&token={TOKEN}"

    # query = {
    #     "company": "string",
    #     "token": "YOUR_API_KEY_HERE"
    # }

    payload = {
        "name": name,
        "email": email,
        "role": "user",
        # "employeeId": "string",
        "noSendEmail": "false",
        # "onlyProjectIds": [
        #     "string"
        # ]
    }

    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(response.json())
        return response.json()
    except:
        return False
