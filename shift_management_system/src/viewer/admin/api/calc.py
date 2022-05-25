from datetime import datetime, timedelta, timezone
import math

def calc_meisai(yyyymm: str, data: list, pay_per_hour: int):
  meisai = {
    'kintai': {
      'roudouNisuu': 0,
      'souroudouJikan': 0,
    },
    'sikyuu': {
      'kihonKyuu': 0,
      'fusyuurouKoujo': 0,
      'souSikyuuGaku': 0,
      'kazeiTaisyouGaku': 0,
    },
    'koujo': {
      'kaigoHoken': 0,
      'kenkouHoken': 0,
      'kouseiNenkin': 0,
      'koyouHoken': 0,
      'syakaiHokenGoukei': 0,
      'syotokuZei': 0,
      'jyuuminZei': 0,
      'seimeiHokenRyou': 0,
      'tsumitateKin': 0,
      'hensai': 0,
      'koujoKei': 0,
    },
  }

  convertYYYYMM = datetime.strptime(yyyymm, "%Y-%m")
  int_last_day = get_last_day_of_month(yyyymm)

  # 労働時間
  hours = 0
  #sec = 0

  roudouNisuu = 0
  for d in data:
    key = d['key']
    if len(key) != 10:
      continue
    roudouNisuu += 1
    start = datetime.strptime(d['start'], "%Y-%m-%d %H:%M")
    end   = datetime.strptime(d['end'], "%Y-%m-%d %H:%M")
    delta = (end - start)
    sec = delta.total_seconds()
    hours += sec / 60 / 60
    #hours += math.floor(sec / 60 / 60)
  # 秒数を時間に変換
  meisai['sikyuu']['kihonKyuu'] = pay_per_hour
  meisai['sikyuu']['souSikyuuGaku'] = math.floor(pay_per_hour * hours)

  # 勤怠
  meisai['kintai']['roudouNisuu'] = roudouNisuu
  meisai['kintai']['souroudouJikan'] = hours

  # 控除計
  koujo_kei = 0
  for _attribute in meisai['koujo']:
    if _attribute != 'koujoKei':
      koujo_kei += meisai['koujo'][_attribute]
  meisai['koujo']['koujoKei'] = koujo_kei

  return meisai

def get_last_day_of_month(yyyymm: str):
    for day in range(31, 0, -1):
        try:
            yyyymmdd = f'{yyyymm}-{zero_padd(day, 2)}'
            datetime.strptime(yyyymmdd, "%Y-%m-%d")
            return day
        except ValueError as e:
            if not str(e) == 'day is out of range for month':
                raise

def zero_padd(val, digits: int) -> str:
    return str(val).zfill(digits)

if __name__ == '__main__':
  import json
  data = json.loads('[{"key": "2021-04-05 ", "name": "09:00～17:30", "start": "2021-04-05 09:00", "end": "2021-04-05 17:30"}, {"key": "2021-04-06 ", "name": "09:00～17:30", "start": "2021-04-06 09:00", "end": "2021-04-06 17:30"}, {"key": "2021-04-07 ", "name": "09:00～17:30", "start": "2021-04-07 09:00", "end": "2021-04-07 17:30"}, {"key": "2021-04-08 ", "name": "09:00～17:30", "start": "2021-04-08 09:00", "end": "2021-04-08 17:30"}, {"key": "2021-04-09 ", "name": "09:00～17:30", "start": "2021-04-09 09:00", "end": "2021-04-09 17:30"}]')
  result = calc_meisai(yyyymm='2021-04', data=data, pay_per_hour=1700)
  from pprint import pprint
  pprint(result)