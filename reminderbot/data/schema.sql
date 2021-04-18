/*
CREATE DATABASE IF NOT EXISTS ReminderBot;
USE ReminderBot;
*/

CREATE TABLE IF NOT EXISTS reminder (
    id INTEGER,
    name TEXT UNIQUE,
    message TEXT,
    every INTEGER,
    last_at TEXT,
    guild_id INTEGER,
    channel_id INTEGER,
    PRIMARY KEY(id),
    FOREIGN KEY(guild_id) REFERENCES guild(id)
);

CREATE TABLE IF NOT EXISTS guild (
    id INTEGER,
    PRIMARY KEY(id)
);