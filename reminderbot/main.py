import asyncio
import json
import logging
from pathlib import Path

import discord
from discord.ext import commands

from reminderbot.db import DB

FILEPATH = Path(__file__).parent.absolute()

def config_load():
    with open(FILEPATH / Path('data/config.json'), 'r') as doc:
        return json.load(doc)


def create_bot():
    config = config_load()
    return Bot(config=config,
               description=config['description'])
     

async def run(bot):
    config = config_load()
    db = DB(bot)
    try:
        await bot.start(config['token'])
    except KeyboardInterrupt:
        await bot.logout()


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            command_prefix=self.get_prefix_,
            description=kwargs.pop('description')
        )
        self.config = kwargs.get('config')
        self.loop.create_task(self.load_extensions())


    async def get_prefix_(self, bot, message):
        prefix = ['!']
        return commands.when_mentioned_or(*prefix)(bot, message)

    async def load_extensions(self):
        """ Load all .py files in /cogs/ as cog extensions. """
        await self.wait_until_ready()
        print("Loading extensions...")
        cogs = [x.stem for x in (FILEPATH / Path('cogs')).glob('*.py')]
        for extension in cogs:
            try:
                self.load_extension(f'reminderbot.cogs.{extension}')
                print(f'OK - {extension}')
            except Exception as e:
                error = f'\n '
                print(f'ERROR - {extension}:')
                PRINT(f"{type(e).__name__} : {e}")
        print("Done loading extensions")

    async def on_message(self, message):
        if message.author.bot:
            return  # ignore bots
        await self.process_commands(message)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    bot = create_bot()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(bot))
