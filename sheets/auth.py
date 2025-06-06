import gspread_asyncio
from google.oauth2.service_account import Credentials
from bot.config import GOOGLE_SERVICE_ACCOUNT_FILE

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_creds():
    return Credentials.from_service_account_file(
        GOOGLE_SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )

def get_agcm():
    return gspread_asyncio.AsyncioGspreadClientManager(get_creds)
