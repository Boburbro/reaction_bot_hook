import sqlite3
from scr.utils.check_func import check_func


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("baza.db")
        self.curs = self.conn.cursor()

    @check_func
    def init_database(self) -> None:
        self.curs.execute(
            """
        CREATE TABLE IF NOT EXISTS bots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            _token TEXT UNIQUE NOT NULL,
            _title TEXT
        );"""
        )
        self.conn.commit()

    @check_func
    def fetch_bots(self) -> list:
        try:
            bots = []
            _bots = self.curs.execute("SELECT * FROM bots;").fetchall()
            for _bot in _bots:
                bots.append(
                    {
                        "id": _bot[0],
                        "token": _bot[1],
                        "title": _bot[2],
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
                "INSERT INTO bots (_token, _title) VALUES (?, ?)",
                (token, title),
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
            bot = self.curs.execute("SELECT * FROM bots WHERE id = ?", (bot_id,)).fetchone()
            if bot:
                return {
                    "id": bot[0],
                    "token": bot[1],
                    "title": bot[2]
                }
            return None
        except Exception as error:
            print(f"Error getting bot by id: {error}")
            return None

    @check_func
    def get_bot_by_token(self, token: str) -> dict:
        try:
            bot = self.curs.execute("SELECT * FROM bots WHERE _token = ?", (token,)).fetchone()
            if bot:
                return {
                    "id": bot[0],
                    "token": bot[1],
                    "title": bot[2]
                }
            return None
        except Exception as error:
            print(f"Error getting bot by token: {error}")
            return None

    def close(self) -> None:
        """Close database connection"""
        self.conn.close()

    def __del__(self):
        """Destructor to ensure connection is closed"""
        self.conn.close()

