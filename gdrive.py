from __future__ import print_function
import os.path
import os
from datetime import datetime as dt
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
            'https://www.googleapis.com/auth/drive.file']

class Drive:
    def __init__(self):
        """
        Inisiasi Google Drive, pastikan kalian sudah login ke akun joricop di browser raspi
        """
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('drive', 'v3', credentials=creds)
    
        
    def make_folder(self):
        """
        Membuat Folder di google drive untuk menyimpan foto foto pada sesi pemrotetan  ini
        """
        folder_metadata = {
            "name": dt.now().strftime("Raspberry Pi 3:  %d-%m-%y %H:%M"),
            "mimeType": "application/vnd.google-apps.folder"
        }
        folder  = self.service.files().create(body=folder_metadata, fields="id").execute()
        self.folder = folder.get("id")
    
    def upload(self, filename):
        """
        Upload foto yang tersimpan di memory
        """
        file_metadata = {
            "name": filename,
            "parents": [self.folder]
        }
        media = MediaFileUpload(filename, resumable=True)
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"File {filename} Uploaded")
        return file.get('id')

if __name__ == '__main__':
    drive_service = Drive()
    drive_service.make_folder()
    for file in os.listdir("to_upload"):
        drive_service.upload(file)
