from typing import Optional, List
from datetime import datetime, timedelta
from discord import Guild, Role, TextChannel
from reminderbot.db import DB


class Reminder:
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

    def __init__(self, id: int, name: str, message: str, every: int, last_at: Optional[str], guild_id: int, db: DB = None):
        self.id = id
        self.name = name
        self.message = message
        self.every = every
        self.last_at = last_at
        self.guild_id = guild_id
        self.db = db

    def time_has_passed(self):
        if not self.last_at:
            return True
        last = datetime.strptime(self.last_at, self.DATETIME_FORMAT)
        now = datetime.now()
        return now - last >= timedelta(hours=self.every)

    def update(self):
        self.last_at = datetime.strftime(datetime.now(), self.DATETIME_FORMAT)
        self.save()

    def role_name(self, prefix: str = "") -> str:
        return f"{prefix}{self.name}"

    def save(self):
        """ Save to DB """
        if not self.db:
            raise RuntimeError("Database unavailable")
        self.db.save_reminder(self.id, self.last_at)

    def get_channel(self, guild: Guild) -> Optional[TextChannel]:
        for ch in guild.channels:
            if ch.id == self.guild_id:
                return ch
        return None

    def get_role(self, guild: Guild, prefix: str = "") -> Optional[Role]:
        for role in guild.roles:
            if role.name == self.role_name(prefix):
                return role
        return None



class ReminderStore:
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    def get(self, id: int) -> Reminder:
        pass

    def get_reminders(self, guild_id: int) -> List[Reminder]:
        return [Reminder(*args, db = self.db) for args in self.db.get_reminders(guild_id)]
    
    def get_reminders_channel_id(self, guild_id: int) -> int:
        return self.db.get_reminders_channel_id(guild_id)

    def create_reminder(self, guild_id: int, name: str, every: int, message: str):
        self.db.create_reminder(guild_id, name, every, message)