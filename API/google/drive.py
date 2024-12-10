from __future__ import print_function

import os.path
import os
from dotenv import load_dotenv
from API.google.dict_orgEmail import obj

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token_drive.json.
SCOPES = ['https://www.googleapis.com/auth/drive']
load_dotenv()


curr_file = os.path.realpath(__file__)
current_directory = os.path.dirname(curr_file)
#создает папку, нужно два параметра, id папки в которой должна находиться папка, и имя папки
def create_fodler(parent_folder, name_folder):

    # parent_folder = os.getenv('PERSONNEL_FILES')
    creds = Credentials.from_authorized_user_file(current_directory + '/token.json', SCOPES)
    service = build('drive', 'v3', credentials=creds)

    if '.dep' in name_folder or '.dm' in name_folder:
        rudiment = name_folder.split(' ')[-1]
        name_folder = name_folder.replace(f' {rudiment}', '')

    folder_metadata = {
        'name': name_folder,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_folder]  # Указываем родительскую папку
    }

    ## создание папки
    folder = service.files().create(body=folder_metadata, fields='id, webViewLink', supportsAllDrives=True).execute()
    # print('Папка ID: %s' % folder.get('id'))

    folder_id = folder['id']
    link = folder['webViewLink']
    return (link, folder_id) #функция возвращает id созданной папки


#функция копирует файл, в определенную папку, нужно два параметра имя копии файла, и id файла
def create_copy_file(name_copy: str):
    username = name_copy.split()[1] + ' ' + name_copy.split()[2]
    file_id = os.getenv('practical_task')## id файла, копию которого нужно сделать
    table_file_id = os.getenv('EVALUATION_TABLE')

    folder_to_practical_task = os.getenv('folder_to_practical_task')## папка родитель, в ней будет лежать папка с копией практических заданий
    ## создание папки в которой будет лежать копия файла
    destination_folder = create_fodler(folder_to_practical_task, name_copy)

    file_metadata = {
        'name': "ИПО на " + name_copy,
        'parents': [destination_folder[1]]
    }

    table_metadata = {
        'name': "таблица оценки на ИС",
        'parents': [destination_folder[1]]
    }
    curr_file = os.path.realpath(__file__)
    current_directory = os.path.dirname(curr_file)

    creds = Credentials.from_authorized_user_file(current_directory + '/token.json', SCOPES)
    service = build('drive', 'v3', credentials=creds)
    ## создание копии
    copied_file = service.files().copy(
        fileId=file_id, body=file_metadata, supportsAllDrives=True, fields='id, webViewLink'
    ).execute()
    copied_file_table = service.files().copy(
        fileId=table_file_id, body=table_metadata, supportsAllDrives=True, fields='id, webViewLink'
    ).execute()

    link = copied_file['webViewLink']
    table_link = copied_file_table['webViewLink']

    update_permission(copied_file['id'])

    # copy_file_id = copied_file.get('id')
    return link, username, destination_folder[1], table_link

def remove_folder_by_id_in_dep(folder_id: str, rang: str):
    creds = Credentials.from_authorized_user_file(current_directory + '/token.json', SCOPES)
    service = build('drive', 'v3', credentials=creds)
    rang = rang.split('.')[0]
    new_parent_id = obj[rang]['archiv']
    old_parent_id = obj[rang]['folder']
    try:
        service.files().update(
            fileId=folder_id,
            addParents=new_parent_id,
            removeParents=old_parent_id,
            fields='id, parents',
            supportsAllDrives=True
        ).execute()
        return True
    except Exception as err:
        print(err)
        return False


def remove_folder_by_id_in_personal(folder_id: str):
    creds = Credentials.from_authorized_user_file(current_directory + '/token.json', SCOPES)
    service = build('drive', 'v3', credentials=creds)
    new_parent_id = '1jVQhWUpaAXXMVeFsqPdn9h4kOljfvLqV'
    old_parent_id = '1kwSG0TeqKltQPnU0pjT_yw4zNyzvKOFE'
    try:
        service.files().update(
            fileId=folder_id,
            addParents=new_parent_id,
            removeParents=old_parent_id,
            fields='id, parents',
            supportsAllDrives=True
        ).execute()
        return True
    except Exception as err:
        print(err)
        return False


def remove_folder_by_id_in_IPO(ipo_folder_id: str):
    creds = Credentials.from_authorized_user_file(current_directory + '/token.json', SCOPES)
    service = build('drive', 'v3', credentials=creds)
    new_parent_id = '1nx5R3UThPzWUUB872un26aVZY_nMyEGl'
    old_parent_id = '1JuJAehyvJu0UQwOUrXU6uRV0x-hlSRgi'
    try:
        service.files().update(
            fileId=ipo_folder_id,
            addParents=new_parent_id,
            removeParents=old_parent_id,
            fields='id, parents',
            supportsAllDrives=True
        ).execute()
        return True
    except Exception as err:
        print(err)
        return False


def update_permission(file_id):
    creds = Credentials.from_authorized_user_file(current_directory + '/token.json', SCOPES)
    service = build('drive', 'v3', credentials=creds)
    permission = {
        'type': 'domain',
        'role': 'writer',
        'domain': 'bbooster.io'
    }
    return service.permissions().create(fileId=file_id, body=permission, supportsAllDrives=True).execute()


