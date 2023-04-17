# remember_the_weight

## Description

This bot 

## Requirements

* python3
* aiogram == 2.25.1
* aiogram_dialog == 1.9.0
* matplotlib == 3.7.1

## Usage

0. Create bot in telegram using https://t.me/BotFather, command: /newbot. After you fill in bot name you will get it's uniqe token, we'll need it later. Then in dialog with BotFather use /mybots command, choose bot from previous step, press 'Edit bot', 'Edit commands', then send this (so your bot will have useful menu with commands):

```
start - show this help page
add_record - add new record
add_skipped_record - add record for a past day
del_record_1_hour - delete last record that is not older than 1 hour
show_week - show weight dynamic for last 7 days
show_month - show weight dynamic for last month
show_n_days - show as many days as you want
cancel - cancel any action
```

1. Clone this repo, go to repo dir

`git clone https://github.com/SozinovD/remember_the_weight; cd remember_the_weight`

2. Install requirements

`python3 -m pip install -r requirements.txt`

3. Rename 'config.py.empty' to 'config.py' and fill in bot token

`mv config.py.empty config.py; nano config.py`

After you are done with it press CTRL+S to save file and CTRL+X to exit nano

4. Make **main.py** executable and run it

```
chmod +x main.py
./main.py
```