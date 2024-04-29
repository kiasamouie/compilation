import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv

class YouTubeUploader:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        self.api_key = os.getenv('API_KEY')
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.scopes = ['https://www.googleapis.com/auth/youtube.upload']
        self.service = self.get_authenticated_service()

    def get_authenticated_service(self):
        credentials = None
        # The file token.json stores the user's access and refresh tokens.
        if os.path.exists('token.json'):
            credentials = Credentials.from_authorized_user_file('token.json', self.scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                # Manually create the flow using the client ID and client secret from the .env file
                flow = Flow.from_client_config(
                    client_config={
                        "web": {
                            "client_id": self.client_id,
                            "client_secret": self.client_secret,
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token"
                        }
                    },
                    scopes=self.scopes)
                # Run the flow to get the credentials
                flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
                authorization_url, _ = flow.authorization_url(prompt='consent')
                print('Please go to this URL: {}'.format(authorization_url))
                
                code = input('Enter the authorization code: ')
                flow.fetch_token(code=code)
                credentials = flow.credentials
                
                # Save the credentials for the next run
                with open('token.json', 'w') as token:
                    token.write(credentials.to_json())
                    
        return build('youtube', 'v3', credentials=credentials)

    def upload_video(self, video_file, title, description, category_id, tags):
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }
        # Call the API's videos.insert method to create and upload the video.
        insert_request = self.service.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=MediaFileUpload(video_file, chunksize=-1, resumable=True)
        )
        response = insert_request.execute()
        print(f'Video id "{response["id"]}" was successfully uploaded.')