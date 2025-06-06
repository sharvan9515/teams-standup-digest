from .auth import get_agcm
from bot.config import GOOGLE_SHEET_ID
import datetime

async def write_standup_to_sheet(user, yesterday, today, blockers):
    agcm = get_agcm()
    agc = await agcm.authorize()
    sh = await agc.open_by_key(GOOGLE_SHEET_ID)
    try:
        ws = await sh.worksheet("Standups")
    except Exception:
        ws = await sh.add_worksheet(title="Standups", rows="100", cols="6")
        await ws.append_row(["Name", "Yesterday", "Today", "Blockers", "Timestamp", "Date"])

    now = datetime.datetime.now()
    await ws.append_row([user, yesterday, today, blockers, str(now), now.date().isoformat()])
