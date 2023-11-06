import uvicorn
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
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
        return {"message": "Unable to fetch teams", "error": error}


@app.get("/teams/{team_id}")
def get_team(team_id: int):
    try:
        cursor.execute("""SELECT * FROM team WHERE team_id = %s""", (team_id,))
        team = cursor.fetchone()
        return {"data": team}
    except Exception as error:
        return {"message": "Unable to fetch team", "error": error}


@app.post("/teams", status_code=status.HTTP_201_CREATED)
def create_team(team: Team):
    try:
        cursor.execute(
            """INSERT INTO team (name, number_of_players, coach) VALUES (%s, %s, %s) RETURNING * """,
            (team.name, team.number_of_players, team.coach),
        )
        new_team = cursor.fetchone()
        conn.commit()
        return {"data": new_team}
    except Exception as error:
        return {"message": "Unable to create team", "error": error}


@app.put("/teams/{team_id}")
def update_team(team_id: int, new_team: Team):
    try:
        cursor.execute("""SELECT * FROM team WHERE team_id = %s""", (team_id,))
        team = cursor.fetchone()
        if team:
            cursor.execute(
                """UPDATE team SET name = %s, number_of_players = %s, coach = %s WHERE team_id = %s RETURNING * """,
                (new_team.name, new_team.number_of_players, new_team.coach, team_id),
            )
            updated_team = cursor.fetchone()
            conn.commit()
            return {"data": updated_team}
        else:
            return {"message": "Team not found"}
    except Exception as error:
        return {"message": "Unable to update team", "error": error}


@app.delete("/teams/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(team_id: int):
    try:
        cursor.execute("""SELECT * FROM team WHERE team_id = %s""", (team_id,))
        team = cursor.fetchone()
        if team:
            cursor.execute("""DELETE FROM team WHERE team_id = %s""", (team_id,))
            conn.commit()
            return {"message": "Team deleted successfully"}
        else:
            return {"message": "Team not found"}
    except Exception as error:
        return {"message": "Unable to delete team", "error": error}
