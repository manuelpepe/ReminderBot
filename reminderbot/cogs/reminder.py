import asyncio

import discord
from discord.ext import commands
import reminderbot.roles as roles
import reminderbot.reminders as reminders


def get_channel_from_guild(guild, channel_id):
    for ch in guild.channels:
        if ch.id == channel_id:
            return ch
    return None


class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = self.bot.config['role_prefix']
        self.store = reminders.ReminderStore(self.bot)
        self.bot.loop.create_task(self.check_reminders_and_send())

    async def check_reminders_and_send(self, *args):
        while True:
            for guild in self.bot.guilds:
                rems = self.store.get_reminders(guild.id)
                for rem in rems:
                    if rem.time_has_passed():
                        channel_id = self.store.get_reminders_channel_id(guild.id)
                        channel = get_channel_from_guild(guild, channel_id)
                        role = rem.get_role(guild, self.prefix)
                        if role is None or role is None:
                            # TODO: Log warnings/errors
                            continue
                        await channel.send(f"{role.mention} - {rem.message}")
                        rem.update()
                        await asyncio.sleep(1)
            await asyncio.sleep(60)


    @commands.command(name="new-reminder")
    async def new_reminder(self, ctx, name: str, hours: int, message: str):
        """ <name: str> <hours: num> <message: str> Create new reminder """
        if not ctx.author.permissions_in(ctx.channel).manage_roles:
            return await ctx.send("No tenes permisos para crear reminders. \nNecesitas 'Manage Roles' para usar este comando.")
        if roles.role_exists(ctx.guild, name, self.prefix):
            role = roles.get_role(ctx.guild, name, self.prefix)
            suggestion = f"!addme {name}"
            return await ctx.send(f"El reminder ya existe. Subscribite con {suggestion}")
        else:
            log = f"Requested by {ctx.author.mention}"
            role = await roles.create_role(ctx.guild, name, self.prefix, log)
            self.store.create_reminder(ctx.guild.id, name, hours, message)
            print("Created reminder")
            return await ctx.send("Nuevo reminder creado.")

    @commands.command()
    async def addme(self, ctx, name):
        """ <reminder_name: str> Subscribe to a reminder. """
        if not roles.role_exists(ctx.guild, name, self.prefix):
            return await ctx.send(f"El reminder {name} no existe.")
        role = roles.get_role(ctx.guild, name, self.prefix)
        if not role in ctx.author.roles:
            await ctx.author.add_roles(role)
        return await ctx.send(f"Ya sos parte de las notificaciones para el reminder {name}")


def setup(bot):
    bot.add_cog(Reminder(bot))
