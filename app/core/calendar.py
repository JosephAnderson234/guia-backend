from google.oauth2 import service_account
from googleapiclient.discovery import build
from app.core.config import GOOGLE_CREDENTIALS

SCOPES = ["https://www.googleapis.com/auth/calendar"]

credentials = service_account.Credentials.from_service_account_file(
    GOOGLE_CREDENTIALS, scopes=SCOPES
)

calendar_service = build("calendar", "v3", credentials=credentials)
