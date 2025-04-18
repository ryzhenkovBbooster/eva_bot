import os

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from API.google.dict_ru_eng import generate_email
import secrets
import string
import re
import logging

group_email = {
    'МК Все сотрудники(приглашение и рассылка)':'inv.mc@bbooster.online',
    'МК Департамент 1': 'div1.mc@bbooster.io',
    'МК Департамент 2': 'div2.mc@bbooster.io',
    'МК Департамент 3': 'div3.mc@bbooster.io',
    'МК Департамент 4': 'div4.mc@bbooster.io',
    'МК Департамент 5': 'div5.mc@bbooster.io',
    'МК Отдел 6': 'dep6.mc@bbooster.io',
    'МК Департамент 6a': 'div6a.mc@bbooster.io',
    'МК Департамент 6b': 'div6b.mc@bbooster.io',
    'МК Департамент 7': 'div7.mc@bbooster.io'

}
SCOPES = ['https://www.googleapis.com/auth/admin.directory.user', 'https://www.googleapis.com/auth/admin.directory.group']

curr_file = os.path.realpath(__file__)
current_directory = os.path.dirname(curr_file)

def generate_password(length=12):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

def create_user_API(name: dict, data):
    group = data['rang'].split('.')[0]
    true_name = {key: generate_email(value) for key, value in name.items()}
    true_name['givenName'] = true_name['givenName'].title()
    true_name['familyName'] = true_name['familyName'].title()
    fullname = true_name['givenName'].title() + " " + true_name['familyName'].title()

    primaryEmail = true_name['givenName'][0] + '.' + true_name['familyName'] + '@bbooster.io'
    primaryEmail = primaryEmail.lower()
    # print(true_name, primaryEmail)
    try:
        creds = Credentials.from_authorized_user_file(current_directory + '/token.json', SCOPES)
        service = build('admin', 'directory_v1', credentials=creds, cache_discovery=False)
        passsword = generate_password(12)
        result = service.users().insert(
            body={
            "primaryEmail":primaryEmail,
            'password': passsword,
            "name":true_name,
            "suspended":False,
            # "password":'new user',
            # hashFunction= "SHA-1",
            "changePasswordAtNextLogin":True,
            "orgUnitPath": '/MK',
            "includeInGlobalAddressList":True}

        ).execute()
        print(result)
        logging.info(result)
        find_group = find_department_index(group)
        if data['rang'].split('.')[1] == 'dep6':
            find_group = group_email['МК Отдел 6']

        add_to_group_google(primaryEmail, group_key=find_group)

        return (primaryEmail, passsword, fullname)

    except Exception as e:
        print(f'ERROR create_user_API : {e}')  
        logging.exception(e)
        return False



def rename_account_google_api(email, position):
    dep = position.split('.')[1]
    group = position.split('.')[0]
    index_user = None

    if 'dm' not in dep:
        index_user = search_emails_in_workspace(dep)
        print(index_user)
    if index_user is None:
        new_email = f'{dep}@bbooster.io'
    else:

        if index_user is not False:

            new_email = f'{dep}.{index_user}@bbooster.io'


    # print(new_email, group)

    creds = Credentials.from_authorized_user_file(current_directory + '/token.json', SCOPES)
    service = build('admin', 'directory_v1', credentials=creds, cache_discovery=False)
    user_info = {
        'primaryEmail': new_email
    }

    try:
        print(user_info)
        result = service.users().update(userKey=email, body=user_info).execute()
        add_to_group_google(new_email, group_email['МК Все сотрудники(приглашение и рассылка)'])




        return result['primaryEmail']



    except Exception as e:
        print(e)
        return False
def search_emails_in_workspace(filter):
    creds = Credentials.from_authorized_user_file(current_directory + '/token.json', SCOPES)

    service = build('admin', 'directory_v1', credentials=creds, cache_discovery=False)
    a = []
    try:
        results = service.users().list(domain='bbooster.io', query=f'email:{filter}*').execute()
        users = results.get('users', [])

        for user in users:
            user = user['primaryEmail']
            user: str
            if f'{filter}.' in user:

                user = user.replace(f'{filter}.', '').replace('@bbooster.io', '')

                a.append(int(user))
            continue
        if len(a) == 0:
            return 1
        largest_num = max(a)
        # print(largest_num, 'kek')
        return largest_num + 1

            # print(user['primaryEmail'])
    except Exception as e:
        print(e, 'err')
        return False

# search_emails_in_workspace('dep6')

# rename_account_google_api('dep2.1@bbooster.online', 'dep2')


def add_to_group_google(email, group_key):
    creds = Credentials.from_authorized_user_file(current_directory + '/token.json', SCOPES)
    service = build('admin', 'directory_v1', credentials=creds, cache_discovery=False)


    member_info = {
        'email': email,
        'role': 'MEMBER'
    }
    try:
        result = service.members().insert(groupKey=group_key, body=member_info).execute()
        return result
    except Exception as e:
        print(e)
        return False


def find_department_index(department_string):
    # Используем регулярное выражение для поиска числа и опциональной буквы после него
    match = re.search(r'\d+[a-z]*', department_string)

    if match:
        index = match.group(0)


        for key in group_email:
            # Проверяем, содержит ли ключ словаря этот индекс
            if re.search(rf'\b{index}\b', key):
                print(group_email[key])

                return group_email[key]
        return False
    else:
        return False

# rename_account_google_api('dep2.1@bbooster.online', 'div1.dm2')
# add_to_group_google('dep2.1@bbooster.online', 'div2.mc@bbooster.online')
def remove_user_by_email(user_key: str):
    creds = Credentials.from_authorized_user_file(current_directory + '/token.json', SCOPES)
    service = build('admin', 'directory_v1', credentials=creds, cache_discovery=False)
    try:
        service.users().delete(userKey=user_key).execute()
        return True
    except Exception as err:
        print(err)
        return False


