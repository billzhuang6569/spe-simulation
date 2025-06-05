import sqlite3
from fastapi import FastAPI, WebSocket


def create_replay_app(log_path: str) -> FastAPI:
    """Return a FastAPI app that streams events from a log file."""
    app = FastAPI()

    @app.websocket("/ws")
    async def replay_ws(ws: WebSocket):
        await ws.accept()
        db = sqlite3.connect(log_path)
        cursor = db.execute("SELECT message FROM events ORDER BY id")
        for (message,) in cursor.fetchall():
            await ws.send_text(message)
        await ws.close()
        db.close()

    return app

