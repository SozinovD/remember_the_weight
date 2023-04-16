#!/usr/bin/env python3

import classes

import time
from datetime import datetime
import sqlite3_requests as db_requests

from tables import tables_arr

import time

def start():
  ''' Connect to db, create if it doesn't exist, return conn obj '''
  return db_requests.check_init()

def add_rec(new_rec):
  ''' Add new record to db, return result '''
  fields_arr = new_rec.get_arr()
  # print(fields_arr)
  result = db_requests.add_record_to_db('records', fields_arr)
  if type(result) == type(list()):
    last_rec = get_last_n_recs(fields_arr[0][1], 1)[0]
    # print('last_rec', last_rec)
    new_rec.set_id(last_rec.id)
    return new_rec
  else:
    return result

def get_new_rec_num():
  ''' Get last record num, return +1 '''
  try:
    last_rec_num = db_requests.select('records')[-1][0]
    new_rec_num = int(last_rec_num) + 1
  except Exception as e:
    new_rec_num = 1
  return new_rec_num

def get_recs_all():
  ''' Return all records from db in array '''
  rec_all_arr = []
  recs = db_requests.select('records')
  new_rec = classes.Record()
  for rec in recs:
    rec_all_arr.append(new_rec.get_obj_from_arr(rec))
  return rec_all_arr

def get_recs_by_filter(user_id, filters=None):
  ''' Return record selected by 'field':'value' for one user_id in array '''
  recs_arr = []
  filt = 'user_id="' + str(user_id) + '"'
  if filters != None:
    filt += ' AND ' + filters
  recs = db_requests.select('records', '*', filt)
  print('get_recs_by_filter: ', recs)
  new_rec = classes.Record()
  for rec in recs:
    recs_arr.append(new_rec.get_obj_from_arr(rec))
  return recs_arr

def get_last_n_recs(user_id, rec_num):
  recs_arr = []
  min_num = get_new_rec_num() - rec_num
  recs_arr = get_recs_by_filter(user_id, 'id >= ' + str(min_num))
  return recs_arr

def del_last_rec_1_hour(user_id, forced=False):
  ''' Delete last record if it was made less then hour ago '''
  last_rec = get_last_n_recs(user_id, 1)[0]
  # if more than 1 hour passed
  if round(time.time(), 0) - last_rec.date_ts > 3600 and forced == False:
    return 'Can\'t delete record older than 1 hour'
  filters = 'id="' + str(last_rec.id) + '"'
  result = db_requests.del_records_from_db('records', filters)
  if result == filters:
    result = 'Record deleted'
  return result
