#!/usr/bin/env python3

import time
from config import bot_token
from config import db_filename as db_name

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.utils.markdown import text
from aiogram.dispatcher import Dispatcher

from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

import db_handler as db
import functions as funcs

import classes

storage = MemoryStorage()
bot = Bot(bot_token)
dp = Dispatcher(bot, storage=storage)

# States
class Form(StatesGroup):
    weight = State()  # Will be represented in storage as 'Form:weight'


@dp.message_handler(commands="add_record")
async def do_add_record(message: types.Message):
  await Form.weight.set()
  line =  'Input your weight and an optional comment, valid examples:\n' \
          '*78.3*\n' \
          'or this:\n' \
          '*40.1 oops, i need to eat!*'
  await message.answer(line, parse_mode='Markdown')

@dp.message_handler(commands="show_last")
async def do_add_record(message):
  await message.reply('later2')

@dp.message_handler(commands='show_all')
async def do_add_record(message):
  await message.reply('later3')

@dp.message_handler(state=Form.weight)
async def get_weight_from_user(message: types.Message, state: FSMContext):

  weight = message.text.split(' ')[0:1]
  weight = ''.join(weight)

  try:
    weight = float(weight)
  except Exception:
    line = 'ERROR: Amount is not a number:\n' + weight
    message.reply(line)
    return

  comment = message.text.split(' ')[1:]
  comment = ' '.join(comment)

  new_rec = classes.Record()

  new_rec.set_user_id(message.from_user.id)
  new_rec.set_date_ts(round(time.time(), 0))
  new_rec.set_weight(weight)
  new_rec.set_comment(comment)


  result = db.add_rec(db_name, new_rec)
  if result == new_rec:
    line = 'Record added:\n\n'
    line += funcs.make_rec_readable(new_rec)
  else:
    line = result
  await message.answer(line)

  await state.finish()



if __name__ == '__main__':

  db_started = db.start(db_name)
  print('Start db:', db_started)

  executor.start_polling(dp)
