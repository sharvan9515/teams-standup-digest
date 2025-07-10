from fastapi import APIRouter
from pydantic import BaseModel
from sheets.gsheet_writer import write_standup_to_sheet


teams_bot_router = APIRouter()


class Standup(BaseModel):
    user: str
    yesterday: str
    today: str
    blockers: str | None = None


@teams_bot_router.post("/standup")
async def submit_standup(payload: Standup):
    await write_standup_to_sheet(
        payload.user, payload.yesterday, payload.today, payload.blockers or ""
    )
    return {"status": "recorded"}
