import db_handler as db
import datetime
from pathlib import Path
from matplotlib import pyplot as plt

help_msg = '''
This bot helps you to track your weught dynamic
There are commands below:

/start - show this help page
/add_record - add new record
/add_skipped_record - add record for a past day
/del_record_1_hour - delete last record that is not older than 1 hour
/show_week - show weight dynamic for last 7 days
/show_month - show weight dynamic for last month
/show_n_days - show as many days as you want
/cancel - cancel any action
'''

def get_help_msg():
  ''' Just return help msg '''
  return help_msg

def day_end_ts(t):
  ''' Return end of the day '''
  dt = t.replace(second=59, microsecond=59, minute=59, hour=23)
  ts = int(dt.timestamp())
  return str(ts)

def get_target_day_ts(days):
  ''' Return ts of end of the day that was N days ago '''
  today_end_ts = day_end_ts(datetime.datetime.now())
  days_ts_delta = days * 24 * 60 * 60
  target_date_ts = int(today_end_ts) - int(days_ts_delta)
  return target_date_ts

def get_graph(user_id, days):
  ''' Get graph of weight dynamic for last N days '''
  target_day_ts = get_target_day_ts(days)
  filter = 'date_ts > ' + str(target_day_ts)
  records = db.get_recs_by_filter(user_id, filter)
  
  plt.figure()
  title_tmplt = 'Weight dynamic: {date_from} - {date_to}'
  title = title_tmplt.format(date_from=datetime.datetime.utcfromtimestamp(target_day_ts).strftime('%Y-%m-%d'), 
                             date_to=datetime.datetime.today().strftime('%Y-%m-%d'))
  plt.title(title)
  plt.xlabel('Date')
  plt.ylabel('Weight (kg)')

  dates_arr = []
  weights_arr = []

  for rec in records:
    # dates_arr.append(datetime.datetime.utcfromtimestamp(rec.date_ts).strftime('%Y-%m-%d %H:00'))
    dates_arr.append(datetime.datetime.utcfromtimestamp(rec.date_ts).strftime('%Y-%m-%d'))
    weights_arr.append(rec.weight)

  plt.plot(dates_arr, weights_arr)
  plt.grid(ls=':')
  
  Path("graphs/" + str(user_id)).mkdir(parents=True, exist_ok=True)

  filename = './graphs/' + str(user_id) + '/' + str(days) + '_' + datetime.datetime.today().strftime('%Y-%m-%d_%H%M') + '.jpeg'
  plt.savefig(filename)

  return filename

def make_rec_readable(rec):
  ''' Make readable line with record info '''
  line_template = 'id = {id}\n' \
                  'date UTC: {date}\n' \
                  'weight: {weight} {measure}\n' \
                  'comment: {comment}'

  line = line_template.format(id=rec.id, date=datetime.datetime.utcfromtimestamp(rec.date_ts).strftime('%Y-%m-%d %H:%M:%S'),
                              weight=rec.weight, measure=rec.measure, comment=rec.comment )
  return line