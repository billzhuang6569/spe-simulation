import argparse
import sqlite3
from engine.turnloop import TurnEngine


def _open_db(path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, message TEXT)"
    )
    return conn

def main(argv=None):
    parser = argparse.ArgumentParser(prog='lucidity')
    subparsers = parser.add_subparsers(dest='command')

    start_parser = subparsers.add_parser('start', help='Start the simulation')
    start_parser.add_argument('--dummy', action='store_true', help='Run in dummy mode')
    start_parser.add_argument('--turns', type=int, default=10, help='Number of turns to run')
    start_parser.add_argument('--log', type=str, help='Path to SQLite log file')

    replay_parser = subparsers.add_parser('replay', help='Replay a saved session')
    replay_parser.add_argument('log', help='Path to SQLite log file')
    replay_parser.add_argument('--ws', action='store_true', help='Serve events over WebSocket')

    args = parser.parse_args(argv)

    if args.command == 'start':
        if args.dummy:
            engine = TurnEngine(turns=args.turns)
            db = None
            if args.log:
                db = _open_db(args.log)
            try:
                for event in engine.run_dummy():
                    print(event)
                    if db:
                        db.execute("INSERT INTO events (message) VALUES (?)", (event,))
                        db.commit()
            finally:
                if db:
                    db.close()
        else:
            raise NotImplementedError('Game logic not implemented yet')
    elif args.command == 'replay':
        if args.ws:
            from lucidity.ws import create_replay_app
            import uvicorn

            app = create_replay_app(args.log)
            uvicorn.run(app, host='127.0.0.1', port=8000, log_level='warning')
        else:
            db = _open_db(args.log)
            cursor = db.execute("SELECT message FROM events ORDER BY id")
            for (message,) in cursor.fetchall():
                print(message)
            db.close()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
