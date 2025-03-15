import sqlite3
from scr.utils.check_func import check_func
from datetime import datetime


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("baza.db")
        self.curs = self.conn.cursor()

    @check_func
    def init_database(self) -> None:
        # Create the bots table if it doesn't exist
        self.curs.execute(
            """
        CREATE TABLE IF NOT EXISTS bots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            _token TEXT UNIQUE NOT NULL,
            _title TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );"""
        )
        
        # Create the activity_logs table if it doesn't exist
        self.curs.execute(
            """
        CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_type TEXT NOT NULL,
            description TEXT NOT NULL,
            ip_address TEXT,
            user_agent TEXT,
            username TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );"""
        )
        
        self.conn.commit()
        
    @check_func
    def is_initialized(self) -> bool:
        """Check if the database is initialized by checking if the bots table exists"""
        try:
            self.curs.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='bots';")
            return bool(self.curs.fetchone())
        except Exception as e:
            print(f"Error checking if database is initialized: {e}")
            return False

    @check_func
    def fetch_bots(self) -> list:
        try:
            bots = []
            _bots = self.curs.execute("SELECT id, _token, _title, created_at FROM bots;").fetchall()
            for _bot in _bots:
                bots.append(
                    {
                        "id": _bot[0],
                        "token": _bot[1],
                        "title": _bot[2],
                        "created_at": _bot[3]
                    }
                )
            return bots
        except Exception as error:
            print(f"Error fetching bots: {error}")
            return error

    @check_func
    def add_bot(self, title: str, token: str) -> bool:
        try:
            self.curs.execute(
                "INSERT INTO bots (_token, _title, created_at) VALUES (?, ?, ?)",
                (token, title, datetime.now()),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            print(f"Error: Token '{token}' already exists")
            return False
        except Exception as error:
            print(f"Error adding bot: {error}")
            return False

    @check_func
    def update_bot(self, bot_id: int, title: str = None, token: str = None) -> bool:
        try:
            if title is None and token is None:
                return False

            updates = []
            values = []

            if title is not None:
                updates.append("_title = ?")
                values.append(title)
            if token is not None:
                updates.append("_token = ?")
                values.append(token)

            values.append(bot_id)
            query = f"UPDATE bots SET {', '.join(updates)} WHERE id = ?"

            self.curs.execute(query, values)
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            print(f"Error: Token '{token}' already exists")
            return False
        except Exception as error:
            print(f"Error updating bot: {error}")
            return False

    @check_func
    def delete_bot(self, bot_id: int) -> bool:
        try:
            self.curs.execute("DELETE FROM bots WHERE id = ?", (bot_id,))
            self.conn.commit()
            return True
        except Exception as error:
            print(f"Error deleting bot: {error}")
            return False

    @check_func
    def get_bot_by_id(self, bot_id: int) -> dict:
        try:
            bot = self.curs.execute("SELECT id, _token, _title, created_at FROM bots WHERE id = ?", (bot_id,)).fetchone()
            if bot:
                return {
                    "id": bot[0],
                    "token": bot[1],
                    "title": bot[2],
                    "created_at": bot[3]
                }
            return None
        except Exception as error:
            print(f"Error getting bot by id: {error}")
            return None

    @check_func
    def get_bot_by_token(self, token: str) -> dict:
        try:
            bot = self.curs.execute("SELECT id, _token, _title, created_at FROM bots WHERE _token = ?", (token,)).fetchone()
            if bot:
                return {
                    "id": bot[0],
                    "token": bot[1],
                    "title": bot[2],
                    "created_at": bot[3]
                }
            return None
        except Exception as error:
            print(f"Error getting bot by token: {error}")
            return None
            
    @check_func
    def add_activity_log(self, activity_type: str, description: str, ip_address: str = None, 
                         user_agent: str = None, username: str = None) -> bool:
        """Add a new activity log entry to the database"""
        try:
            self.curs.execute(
                """
                INSERT INTO activity_logs 
                (activity_type, description, ip_address, user_agent, username, timestamp) 
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (activity_type, description, ip_address, user_agent, username, datetime.now())
            )
            self.conn.commit()
            return True
        except Exception as error:
            print(f"Error adding activity log: {error}")
            return False
            
    @check_func
    def get_recent_activities(self, limit: int = 10) -> list:
        """Get recent activity logs from the database"""
        try:
            activities = []
            query = """
                SELECT id, activity_type, description, ip_address, username, timestamp 
                FROM activity_logs 
                ORDER BY timestamp DESC 
                LIMIT ?
            """
            logs = self.curs.execute(query, (limit,)).fetchall()
            
            for log in logs:
                activities.append({
                    "id": log[0],
                    "activity_type": log[1],
                    "description": log[2],
                    "ip_address": log[3],
                    "username": log[4],
                    "timestamp": log[5]
                })
            return activities
        except Exception as error:
            print(f"Error fetching activity logs: {error}")
            return []



