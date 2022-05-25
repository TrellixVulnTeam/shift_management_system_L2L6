from datetime import datetime, timedelta, timezone
import math

def now(datetime_format):
    jst = timezone(timedelta(hours=+9), 'JST')
    _now = ('{0:' + datetime_format + '}').format(datetime.now(jst))
    return _now

def datetime_2_str(dt: datetime, datetime_format: str):
    _now = ('{0:' + datetime_format + '}').format(dt)
    return _now

def my_floor(x: float, n: int) -> float:
  # n は 切り捨てしたい桁
  return math.floor(x * 10 ** n) / (10 ** n)

def str_2_datetime(yyyymmdd: str, datetime_format: str):
    return datetime.strptime(yyyymmdd, datetime_format)

def find_value_from_list(listt :list, callback) -> dict:
    for l in listt:
        if callback(l):
            return l

def is_empty(val: str) -> bool:
    if val is None:
        return True
    if type(val) is str:
        if len(val.strip()) == 0:
            return True
    elif type(val) is int:
        return val == 0
    elif type(val) is float:
        return val == 0.0
    elif type(val) is list:
        return len(val) == 0
    elif type(val) is dict:
        return len(val.keys()) == 0
    return False

def zero_padd(val, digits: int) -> str:
    return str(val).zfill(digits)

def to_int(value: str) -> int:
    try:
        return int(value)
    except ValueError as e:
        pass

def get_last_day_of_month(yyyymm: str):
    for day in range(31, 0, -1):
        try:
            yyyymmdd = f'{yyyymm}{zero_padd(day, 2)}'
            datetime.strptime(yyyymmdd, "%Y%m%d")
            return day
        except ValueError as e:
            if not str(e) == 'day is out of range for month':
                raise

def yyyymm_2_datetime(yyyymm: str, format: str='%Y%m'):
    return datetime.strptime(yyyymm, format)

def org_round(value, base):
    return round(value * base) / base