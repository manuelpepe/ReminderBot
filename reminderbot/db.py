from typing import Optional
from contextlib import contextmanager
import sqlite3



class DB:
    def __init__(self, bot):
        self.bot = bot
        self.bot.db = self

    @contextmanager
    def con(self):
        con = sqlite3.connect(self.bot.config['dbname'])
        try:
            yield con
        finally:
            con.close()

    def register_guild(self, guild_id: int):
        with self.con() as con:
            cur = con.cursor()
            cur.execute("INSERT INTO guild (id) VALUES (?)", (guild_id, ))
            con.commit()
            cur.close()

    def get_reminders(self, guild_id: int):
        with self.con() as con:
            cur = con.cursor()
            return cur.execute("SELECT * FROM reminder WHERE guild_id = ?", (guild_id, )).fetchall()

    def create_reminder(
         self, 
         guild_id: int, 
         name: str, 
         every: int, 
         message: str, 
         channel_id: int, 
         offhours_start: Optional[str] = None, 
         offhours_end: Optional[str] = None
        ):
        with self.con() as con:
            cur = con.cursor()
            res = cur.execute(
                "INSERT INTO reminder (name, message, every, last_at, guild_id, channel_id, offhours_start, offhours_end) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                (name, message, every, None, guild_id, channel_id, offhours_start, offhours_end)
            )
            con.commit()
            cur.close()

    def save_reminder(self, id: int, last_at: Optional[str]):
        with self.con() as con:
            cur = con.cursor()
            res = cur.execute(
                "UPDATE reminder SET last_at = ? WHERE id = ?",
                (last_at, id)
            )
            con.commit()
            cur.close()