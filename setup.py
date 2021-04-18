#!/usr/bin/env python

from distutils.core import setup

setup(name='reminderbot',
    version='1.0',
    description='Discord Bot for perioduc role-based reminders',
    author='Manuel Pepe',
    author_email='manuelpepe-dev@outlook.com.ar',
    packages=[
        'reminderbot',
        'reminderbot.cogs'
    ],
)