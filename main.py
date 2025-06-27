from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bot.bot import teams_bot_router
from digest.weekly_summary import schedule_weekly_digest
from dashboard.routes import dashboard_router
from auth.middleware import verify_token
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(verify_token)

app.include_router(teams_bot_router, prefix="/bot")
app.include_router(dashboard_router, prefix="/dashboard")

schedule_weekly_digest()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
