# ReminderBot

A simple discord bot that allows users to subscribe to periodic reminders with role-based notifications.


## Usage

### Create new reminder

For example, to create a new hourly reminder to drink water. 

```
!new-reminder DrinkWater 1 "Remember to drink water!" #water-alerts
```

The above command will: 

* Create a new role for people that want to be reminded
* Assing the role to the creator
* Enable alerts (every 1 hour) to the channel #water-alerts. The alert will metnion the related @role to notify subscribers.

Only members with the "Manage Role" permission can create reminders.

### Subscribe to a reminder

With:

```
!addme DrinkWater
```

Any member can join to the reminder role to be notified when the it goes out.

### Set offhours for reminders (WIP)

To prevent reminders from going out between 11pm and 08am:

```
!set-offhours DrinkWater 23:00 08:00
```

The time is based on the computer running the bot.

## Running the bot

1. Clone the repo

```
git clone https://github.com/manuelpepe/RemindersBot.git
```

2. Init DB. There's no command for this yet. Create a sqlite3 db and run the SQL script in `reminderbot/data/schema.sql`

3. Install dependencies:

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

4. Copy sample config and edit:

```
cp remindersbot/data/sample.config.json remindersbot/data/config.json
vim remindersbot/data/config.json
```

5. Run bot:

```
python -m reminderbot.main
```
