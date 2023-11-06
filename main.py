import uvicorn
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import psycopg2

app = FastAPI()


class Team(BaseModel):
    name: str
    number_of_players: Optional[int] = 11
    coach: str


load_dotenv()

try:
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    cursor = conn.cursor()
    print("Connected to database")
except Exception as e:
    print("Unable to connect to database", e)


@app.get("/")
def home():
    return {"message": "WELCOME HERE"}


@app.get("/teams")
def get_teams():
    try:
        cursor.execute("""SELECT * FROM team """)
        teams = cursor.fetchall()
        return {"data": teams}
    except Exception as error:
        print(error)
        return {"message": "Unable to fetch teams"}


@app.get("/teams/{team_id}")
def get_team(team_id: int):
    try:
        cursor.execute("""SELECT * FROM team WHERE team_id = %s""", (team_id,))
        team = cursor.fetchone()
        return {"data": team}
    except Exception as error:
        print(error)
        return {"message": "Unable to fetch team"}