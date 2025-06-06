from fastapi import APIRouter
from sheets.auth import get_agcm
from bot.config import GOOGLE_SHEET_ID
import datetime

dashboard_router = APIRouter()

@dashboard_router.get("/missing")
async def get_missing_updates():
    agcm = get_agcm()
    agc = await agcm.authorize()
    sh = await agc.open_by_key(GOOGLE_SHEET_ID)
    ws = await sh.worksheet("Standups")
    records = await ws.get_all_records()

    today = datetime.date.today().isoformat()
    users_today = set(row.get("Name") for row in records if row.get("Date") == today)
    all_users = set(row.get("Name") for row in records if row.get("Name"))
    missing = sorted(all_users - users_today)

    return {"date": today, "missing_users": missing}
