"""
Adaptador Externo - Google Calendar
"""

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/calendar"]
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS", "credentials.json")
CALENDAR_ID = os.getenv("CALENDAR_ID")

try:
    credentials = service_account.Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS, scopes=SCOPES
    )
    calendar_service = build("calendar", "v3", credentials=credentials)
except Exception as e:
    print(f"⚠️ Google Calendar no inicializado: {e}")
    calendar_service = None
