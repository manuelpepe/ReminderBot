from typing import Optional
from discord import Guild, Role

def role_exists(guild: Guild, name: str, prefix: str = "") -> bool:
    prefixed = f"{prefix}{name}"
    for role in guild.roles:
        if role.name == prefixed:
            return True
    return False

def get_role(guild: Guild, name: str, prefix: str = "") -> Optional[Role]:
    prefixed = f"{prefix}{name}"
    for role in guild.roles:
        if role.name == prefixed:
            return role
    return None

async def create_role(guild: Guild, name: str, prefix: str = "", reason: str = "Not specified") -> bool:
    prefixed = f"{prefix}{name}"
    return await guild.create_role(name=prefixed, reason=reason)