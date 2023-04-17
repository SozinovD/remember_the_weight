#!/usr/bin/env python3

import time
from config import bot_token

import datetime

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.utils.markdown import text
from aiogram.dispatcher import Dispatcher

from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.input_file import InputFile
from aiogram.dispatcher.filters import Text

from pathlib import Path

from matplotlib import pyplot as plt

import db_handler as db
import functions as funcs

import classes

storage = MemoryStorage()
bot = Bot(bot_token)
dp = Dispatcher(bot, storage=storage)

# States
class Form(StatesGroup):
  weight = State()  # Will be represented in storage as 'Form:weight'
  weight_past = State()
  graph_n_days = State()

# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    ''' Allow user to cancel any action '''
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(commands="start")
async def show_help(message: types.Message):
  ''' Show help msg at start '''
  await message.answer(funcs.get_help_msg())

@dp.message_handler(commands="add_record")
async def do_add_record(message: types.Message):
  ''' handle 'add_record' command '''
  await Form.weight.set()
  line =  'Input your weight and an optional comment, valid examples:\n' \
          '*78.3*\n' \
          'or this:\n' \
          '*40.1 oops, i need to eat!*'
  await message.answer(line, parse_mode='Markdown')

@dp.message_handler(commands='add_skipped_record')
async def add_skipped_record(message: types.Message):
  ''' handle 'add_record' command '''
  await Form.weight_past.set()
  line =  'Input date, your weight and an optional comment, valid examples:\n' \
          '*13.02.2023 78.3*\n' \
          'or this:\n' \
          '*13.02.2023 40.1 oops, i need to eat!*'
  await message.answer(line, parse_mode='Markdown')

@dp.message_handler(commands="del_rec_1_hour")
async def del_rec_1_hour(message: types.Message):
  await message.answer(db.del_last_rec_1_day(message.from_user.id))

@dp.message_handler(commands="show_week")
async def show_week(message: types.Message):
  week_graph_path = funcs.get_graph(message.from_user.id, 7)
  week_graph = InputFile(week_graph_path)
  await message.answer_photo(photo=week_graph)

@dp.message_handler(commands='show_month')
async def show_month(message: types.Message):
  month_graph_path = funcs.get_graph(message.from_user.id, 30)
  month_graph = InputFile(month_graph_path)
  await message.answer_photo(photo=month_graph)

@dp.message_handler(commands='show_n_days')
async def show_n_days(message: types.Message):
  await Form.graph_n_days.set()
  await message.answer('Input number of days you need like so:\n40')

@dp.message_handler(state=Form.graph_n_days)
async def send_graph(message: types.Message, state: FSMContext):
  days_num = message.text
  try:
    days_num = int(days_num)
    custom_graph_path = funcs.get_graph(message.from_user.id, days_num)
    custom_graph = InputFile(custom_graph_path)
    await message.answer_photo(photo=custom_graph)
  except Exception:
    line = 'ERROR: number of days is not an integer:\n' + days_num
    await message.answer(line)
  await state.finish()

@dp.message_handler(state=Form.weight)
async def get_weight_from_user(message: types.Message, state: FSMContext):

  weight = message.text.split(' ')[0:1]
  weight = ''.join(weight)

  weight = weight.replace( ',', '.' )

  comment = message.text.split(' ')[1:]
  comment = ' '.join(comment)

  await message.reply(add_record(message.from_user.id, weight, comment))

  await state.finish()

@dp.message_handler(state=Form.weight_past)
async def get_weight_from_user_past(message: types.Message, state: FSMContext):

  date = message.text.split(' ')[0:1]
  date = ' '.join(date)

  weight = message.text.split(' ')[1:2]
  weight = ''.join(weight)

  weight = weight.replace( ',', '.' )

  comment = message.text.split(' ')[2:]
  comment = ' '.join(comment)

  await message.reply(add_record(message.from_user.id, weight, comment, date))

  await state.finish()

def add_record(user_id, weight, comment, date=None):
  try:
    weight = float(weight)
  except Exception:
    line = 'ERROR: weight is not a number:\n' + weight    
    return line

  new_rec = classes.Record()

  new_rec.set_user_id(user_id)
  if date != None:
    try:
      date_ts = float(time.mktime(datetime.datetime.strptime(date, "%d.%m.%Y").timetuple()))
    except Exception as e:
      return e
    print('date_ts', date_ts)
    new_rec.set_date_ts(round(date_ts, 0))
  else:
    new_rec.set_date_ts(round(time.time(), 0))
  new_rec.set_weight(round(weight, 2))
  new_rec.set_comment(comment)

  result = db.add_rec(new_rec)
  if result == new_rec:
    line = 'Record added:\n\n'
    line += funcs.make_rec_readable(new_rec)
  else:
    line = result
  return line



if __name__ == '__main__':

  Path("graphs").mkdir(parents=True, exist_ok=True)

  db_started = db.start()
  print('Start db:', db_started)

  executor.start_polling(dp)
