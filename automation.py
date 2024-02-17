import os.path
import csv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import cal_id

SCOPES = ['https://www.googleapis.com/auth/calendar']

def automate():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('API_Credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    try:
        service = build('calendar', 'v3', credentials=creds)

        # Define the calendar ID where the events will be created
        calendar_id = cal_id  # Or another calendar ID

        # Read the CSV file
        with open('raw_data.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)  # Skip the header row

            for row in reader:
                job_name, start_time, end_time = row
                event = {
                    'summary': job_name,
                    'start': {'dateTime': start_time, 'timeZone': 'America/New_York'},
                    'end': {'dateTime': end_time, 'timeZone': 'America/New_York'},
                }

                # Insert the event into the calendar
                event = service.events().insert(calendarId=calendar_id, body=event).execute()
                print(f'Event created: {event.get("htmlLink")}')

    except HttpError as error:
        print('An error occurred:', error)
        if True:
            pass
