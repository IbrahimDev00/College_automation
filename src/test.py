import os
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']

def test_calendar_api():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        print("[ERROR] Token not valid. Re-authenticate the app.")
        return
    
    try:
        service = build("calendar", "v3", credentials=creds)
        # Fetch 10 upcoming events to test
        events_result = service.events().list(calendarId='primary', maxResults=10).execute()
        events = events_result.get('items', [])
        if not events:
            print("No upcoming events found.")
        for event in events:
            print(f"Event: {event['summary']}")
    except HttpError as error:
        print(f"[ERROR] API call failed: {error}")

test_calendar_api()
