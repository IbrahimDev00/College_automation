import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_calendar():
    """Authenticate and return the Google Calendar service."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    try:
        service = build("calendar", "v3", credentials=creds)
        return service
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def add_events(assignments, dates):
    """Add events to Google Calendar."""
    service = authenticate_calendar()
    if not service:
        print("[ERROR] Could not authenticate Google Calendar service.")
        return
    
    for assignment, date in zip(assignments, dates):
        event = {
            'summary': assignment,
            'start': {
                'date': date,  # Format: YYYY-MM-DD
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'date': date,  # Format: YYYY-MM-DD
                'timeZone': 'Asia/Kolkata',
            },
        }
        try:
            service.events().insert(calendarId='primary', body=event).execute()
            print(f"[SUCCESS] Event added: {assignment} on {date}")
        except HttpError as error:
            print(f"[ERROR] An error occurred while adding event: {error}")
