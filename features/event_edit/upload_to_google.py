from google.oauth2 import service_account
from googleapiclient.discovery import build

# 设置Google Drive API凭证
SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = '/py-fullcalendar/features/file.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

def upload_file_to_drive(file_metadata, media):
    try:
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        print(f"File ID: {file.get('id')}")
    except Exception as e:
        print(f"An error occurred: {e}")
        file = None
    return file
