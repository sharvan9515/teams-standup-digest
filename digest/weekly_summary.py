from apscheduler.schedulers.background import BackgroundScheduler
from sheets.auth import get_agcm
from bot.config import GOOGLE_SHEET_ID, TEAMS_WEBHOOK_URL
from digest.llm_summary import summarize_with_llm
import datetime
import asyncio
import httpx

def schedule_weekly_digest():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_async_summary, 'cron', day_of_week='fri', hour=18)
    scheduler.add_job(run_async_reminder, 'cron', hour=12)
    scheduler.start()

def run_async_summary():
    asyncio.run(send_weekly_digest())

def run_async_reminder():
    asyncio.run(send_missed_standup_reminders())

async def send_weekly_digest():
    agcm = get_agcm()
    agc = await agcm.authorize()
    sh = await agc.open_by_key(GOOGLE_SHEET_ID)
    ws = await sh.worksheet("Standups")
    data = await ws.get_all_values()
    summary = summarize_with_llm(data)

    await httpx.AsyncClient().post(TEAMS_WEBHOOK_URL, json={
        "text": f"\n📅 *Weekly Digest Summary*\n\n{summary}"
    })

async def send_missed_standup_reminders():
    agcm = get_agcm()
    agc = await agcm.authorize()
    sh = await agc.open_by_key(GOOGLE_SHEET_ID)
    ws = await sh.worksheet("Standups")
    records = await ws.get_all_records()
    today = datetime.date.today().isoformat()

    all_users = set([row.get("Name") for row in records if row.get("Name")])
    users_today = set([row.get("Name") for row in records if row.get("Date") == today])
    missing_users = sorted(all_users - users_today)

    if missing_users:
        message = "⏰ *Reminder*: The following users haven't submitted today's standup:\n\n"
        message += "\n".join(f"- {user}" for user in missing_users)
        await httpx.AsyncClient().post(TEAMS_WEBHOOK_URL, json={ "text": message })
