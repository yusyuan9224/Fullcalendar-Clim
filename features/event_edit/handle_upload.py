import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
from nicegui import ui

SERVICE_ACCOUNT_FILE = 'features/file.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)

UPLOADS_FOLDER_ID = '11JRvyN10ozWinjrG1KXPrZ7WNV6vr7Nu'

def create_folder(folder_name, parent_folder_id=UPLOADS_FOLDER_ID):
    try:
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_folder_id]
        }
        folder = drive_service.files().create(body=file_metadata, fields='id').execute()
        print(f"Created folder with ID: {folder.get('id')}")
        return folder.get('id')
    except Exception as e:
        print(f"Failed to create folder: {e}")
        raise

def upload_file_to_drive(file_path, folder_id):
    try:
        file_metadata = {
            'name': os.path.basename(file_path),
            'parents': [folder_id]
        }
        media = MediaFileUpload(file_path, resumable=True)
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"Uploaded file with ID: {file.get('id')}")
        return file.get('id')
    except Exception as e:
        print(f"Failed to upload file: {e}")
        raise

def handle_upload(file, title: str, folder_id=None):
    if not title:
        ui.notify('Please enter the title before uploading attachments.', color='red')
        return None

    try:
        if folder_id is None:
            folder_id = create_folder(title)
        file_path = f'uploads/{title}/{file.name}'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(file.content.read())

        print(f"Saved file to: {file_path}")
        upload_file_to_drive(file_path, folder_id)
        print(f"Uploaded {file.name} to Google Drive.")
        ui.notify(f'File uploaded to folder {title}')
        return folder_id
    except Exception as e:
        print(f"Error during file upload: {e}")
        ui.notify(f"Failed to upload file: {e}", color='red')
        return None
    
def get_files_in_folder(folder_id):
    try:
        query = f"'{folder_id}' in parents and trashed=false"
        results = drive_service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])
        return items
    except Exception as e:
        print(f"Failed to get files: {e}")
        return []

def get_file_download_link(file_id):
    return f"https://drive.google.com/uc?id={file_id}&export=download"

