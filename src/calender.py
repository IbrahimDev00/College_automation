from datetime import datetime, timedelta
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define the scope for Google Calendar API
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
                "client.json", SCOPES
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
        # Convert date to ISO format with time (start and end of the day)
        start_time = f"{date}T00:00:00+05:30"  # Midnight IST
        end_time = f"{date}T23:59:59+05:30"   # End of the day IST

        event = {
            'summary': assignment,
            'start': {
                'dateTime': start_time,  # Properly formatted start time
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': end_time,  # Properly formatted end time
                'timeZone': 'Asia/Kolkata',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},  # Reminder 1 day before
                    {'method': 'popup', 'minutes': 10},       # Popup 10 minutes before
                ],
            },
        }

        try:
            event_result = service.events().insert(calendarId='primary', body=event).execute()
            print(f"[SUCCESS] Event added: {assignment} on {date}")
            print(f"Event created: {event_result.get('htmlLink')}")
        except HttpError as error:
            print(f"[ERROR] An error occurred while adding event: {error}")
