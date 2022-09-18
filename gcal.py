from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import secrets


# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/calendar.events'
]


# Choose the colors (1 to 10 ) -- 11 is missing (#dc2127 : red)
# https://coolors.co/a4bdfc-7ae7bf-dbadff-ff887c-fbd75b-ffb878-46d6db-e1e1e1-5484ed-51b749
colors = {
    'a faire':      '4',
    'en cours' :    '5',
    'fait':         '2',
    'a bosser':     '3',
    'oops':         '8',
    'evalue':       '11',
    'evalue-rendu': '10',
}

timezone = "America/Montreal"


def init_gcal():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except:
                print("Auth error, please relaunch the script")
                os.remove("token.json")
                os._exit(0)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)


service = init_gcal()

def get_color(evaluated, state):
    if evaluated:
        if state == 'fait':
            return colors['evalue-rendu']
        return colors['evalue']
    
    try:
        return colors[state]
    except:
        return None


def add_hw(h):
    new_event = service.events().insert(
        calendarId=secrets.GCAL_ID,
        body={
            "end": {
                "dateTime": f"{h['date']}T{h['hour_end']}:00",
                "timeZone": timezone
            },
            "start": {
                "dateTime": f"{h['date']}T{h['hour_start']}:00",
                "timeZone": timezone
            },
            "summary": h['title'],
            "colorId": get_color(h['evaluated'], h['state'])
        }
    ).execute()

    # Return the calendar event ID
    return new_event['id']


def remove_hw(event_id):
    deleted_event = service.events().delete(
        calendarId=secrets.GCAL_ID,
        eventId=event_id
    ).execute()


def edit_hw(h):
    edited_event = service.events().update(
        calendarId=secrets.GCAL_ID,
        eventId=h['gcal_id'],
        body={
            "end": {
                "dateTime": f"{h['date']}T{h['hour_end']}:00",
                "timeZone": timezone
            },
            "start": {
                "dateTime": f"{h['date']}T{h['hour_start']}:00",
                "timeZone": timezone
            },
            "summary": h['title'],
            "colorId": get_color(h['evaluated'], h['state'])
        }
    ).execute()
