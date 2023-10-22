import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from httplib2 import Http
import pandas as pd
import numpy as np
from datetime import datetime,timedelta


SCOPES = ['https://www.googleapis.com/auth/calendar']

API_KEY='AIzaSyBbzLoF1y_ktgaosxqQyChJyACBoUOeOVo'
def main():
    
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

    try:
        # service = build('calendar', 'v3', credentials=creds)
        service = build('calendar', 'v3',credentials=creds)

        df=pd.read_excel("CodeforceCalander.xlsx")
        Summary=df['Name']
        DateTime=df['Start']
        hour= df['Length'].dt.hour
        minute=df['Length'].dt.minute
        for i in range(df.shape[0]):
            start_time=datetime.strptime(DateTime[i],'%b/%d/%Y %H:%M')
            end_time = start_time + timedelta(hours=int(hour[i]),minutes=int(minute[i]))
            TimeZone='Asia/Kolkata'

            event = {
            'summary': str(Summary[i]),
            'location': 'Delhi',
            'description': str(Summary[i]),
            'start': {
                'dateTime': str(start_time.strftime('%Y-%m-%dT%H:%M:%S'+'+05:30')),
                'timeZone': 'Asia/Kolkata',  # Corrected timezone name
            },
            'end': {
                'dateTime': str(end_time.strftime('%Y-%m-%dT%H:%M:%S'+'+05:30')),  # Corrected time format
                'timeZone': 'Asia/Kolkata',
            },
            
            'attendees': [
                {'email': 'gaurav94266@gmail.com'},
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                    ],
                },
            }


            event = service.events().insert(calendarId='primary',body=event).execute()
            print(f"Event created: {event.get('htmlLink')}")

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()
