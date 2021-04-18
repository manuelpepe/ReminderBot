from typing import Optional, List
from datetime import datetime, timedelta, time
from discord import Guild, Role, TextChannel
from reminderbot.db import DB


class Reminder:
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

    def __init__(
         self,
         id: int,
         name: str,
         message: str,
         every: int,
         last_at: Optional[str],
         guild_id: int,
         channel_id: int,
         offhours_start: time,
         offhours_end: time,
         db: DB = None
        ):
        self.id = id
        self.name = name
        self.message = message
        self.every = every
        self.last_at = last_at
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.offhours_start = offhours_start
        self.offhours_end = offhours_end
        self.db = db
    
    def in_off_hours(self, now: Optional[time] = None):
        if now is None:
            now = datetime.now().time()
        if self.offhours_start > self.offhours_end:
            return now >= self.offhours_start or now <= self.offhours_end
        else:
            return now >= self.offhours_start and now <= self.offhours_end

    def is_time(self):
        if self.in_off_hours():
            return False
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
            if ch.id == self.channel_id:
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

    def _parse_db_args(self,          
         id: int,
         name: str,
         message: str,
         every: int,
         last_at: Optional[str],
         guild_id: int,
         channel_id: int,
         offhours_start: time,
         offhours_end: time,
         db: DB = None
        ):
        offhours_start_time = time(*offhours_start.split(':'))
        offhours_end_time = time(*offhours_end.split(':'))
        return (id, name, message, every, last_at, guild_id, channel_id, offhours_start_time, offhours_end_time)

    def get(self, id: int) -> Reminder:
        pass

    def get_reminders(self, guild_id: int) -> List[Reminder]:
        return [Reminder(*self._parse_db_args(args), db = self.db) for args in self.db.get_reminders(guild_id)]
    
    def create_reminder(self, guild_id: int, name: str, every: int, message: str, channel_id: int):
        self.db.create_reminder(guild_id, name, every, message, channel_id, None, None)
    