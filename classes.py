from dataclasses import dataclass

@dataclass
class Record:
  ''' Class for db records '''
  id: int               # sequential number
  user_id: int          # user that sent this record
  date_ts: int          # when record was done
  weight: float         # weight itself
  measure: set          # usually kg
  comment: str          # a comment for record

  def __init__(self):
    self.id = 0
    self.user_id = ''
    self.date_ts = ''
    self.weight = 0.0
    self.measure = 'kg'
    self.comment = ''

  def set_id(self, id: int):
    self.id = int(id)

  def set_user_id(self, user_id: int):
    self.user_id = int(user_id)

  def set_date_ts(self, date_ts: int):
    self.date_ts = int(date_ts)

  def set_weight(self, weight: float):
    self.weight = float(weight)

  def set_measure(self, measure: str):
    self.measure = str(measure)

  def set_comment(self, comment: str):
    self.comment = str(comment)

  def get_arr(self):
    arr = []
    arr.append(['user_id', int(self.user_id)])
    arr.append(['date_ts', int(self.date_ts)])
    arr.append(['weight', float(self.weight)])
    arr.append(['measure', str(self.measure)])
    arr.append(['comment', self.comment])
    return arr

  def get_obj_from_arr(self, arr):
    obj = Record()
    obj.set_id(arr[0])
    obj.set_user_id(arr[1])
    obj.set_date_ts(arr[2])
    obj.set_weight(arr[3])
    obj.set_measure(arr[4])
    obj.set_comment(arr[5])
    return obj