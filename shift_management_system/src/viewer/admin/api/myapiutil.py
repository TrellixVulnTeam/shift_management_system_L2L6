import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'site-packages'))

import myboto3util
import json
import boto3
import botocore
import calc
import jwt

region = os.environ.get("REGION", "ap-northeast-1")
env = os.environ.get("ENV")
dest_s3_prefix = os.environ.get("DEST_S3_PREFIX")
dest_s3_prefix_pay_per_hour = os.environ.get("DEST_S3_PREFIX_PAY_PER_HOUR", "pay_per_hour")
dest_s3_prefix_regular_holiday = os.environ.get("DEST_S3_PREFIX_REGULAR_HOLIDAY", "regular_holiday")
dest_s3_prefix_limit_hours = os.environ.get("DEST_S3_PREFIX_LIMIT_HOURS", "limit_hours")
dest_s3_prefix_day_of_week_limit_hours = os.environ.get("DEST_S3_PREFIX_DAY_OF_WEEK_LIMIT_HOURS", "day_of_week_limit_hours")
bucket_name_data_user = os.environ.get("BUCKET_NAME_DATA_USER")
bucket_name_data_admin = os.environ.get("BUCKET_NAME_DATA_ADMIN")
user_pool_id = os.environ.get("USER_POOL_ID")

config = botocore.client.Config(signature_version='s3v4')
s3_client = boto3.client('s3', region_name=region, config=config)
s3_resource = boto3.resource('s3', region_name=region, config=config)
cognito = boto3.client('cognito-idp', region_name=region, config=config)
s3_bucket_data_user = s3_resource.Bucket(bucket_name_data_user)
s3_bucket_data_admin = s3_resource.Bucket(bucket_name_data_admin)

default_common_pay_per_hour = 1700

def fetch_all_users_in_group(user_pool_id: str, group_name: str):
    def list_users_in_group(UserPoolId: str, GroupName: str, Limit: int, NextToken: str=None):
      if NextToken:
        return cognito.list_users_in_group(
            UserPoolId=UserPoolId,
            GroupName=GroupName,
            Limit=Limit,
            NextToken=NextToken,
        )
      else:
        return cognito.list_users_in_group(
            UserPoolId=UserPoolId,
            GroupName=GroupName,
            Limit=Limit,
        )

    Users = []
    try:
        response = list_users_in_group(
            UserPoolId=user_pool_id,
            GroupName=group_name,
            Limit=60,
        )
        Users += response['Users']
        NextToken = response.get('NextToken', None)

        while NextToken != None:
          response = list_users_in_group(
              UserPoolId=user_pool_id,
              GroupName=group_name,
              Limit=60,
              NextToken=NextToken,
          )
          Users += response['Users']
          NextToken = response.get('NextToken', None)

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            pass
        else:
            raise e

    return Users

def explode_yyyymmdd(yyyymmdd: str):
  splited = yyyymmdd.split('-')
  return splited[0].lstrip().rstrip(), splited[1].lstrip().rstrip(), splited[2].lstrip().rstrip()

def pluck_yyyy_mm_dd(data: dict):
  yyyy = data['start'][0:4].lstrip().rstrip()
  mm = data['start'][5:7].lstrip().rstrip()
  dd = data['start'][8:10].lstrip().rstrip()
  return yyyy, mm, dd

def gen_s3_common_pay_per_hour_key():
  return f'{dest_s3_prefix_pay_per_hour}/{env}/common.json'

def gen_s3_pay_per_hour_key(user_id: str):
  return f'{dest_s3_prefix_pay_per_hour}/{env}/{user_id}.json'

def gen_s3_username_key(user_id: str):
  return f'username/{user_id}/username.json'

def gen_s3_regular_holiday_data_key(yyyy: str, mm: str):
  return f'{dest_s3_prefix_regular_holiday}/{env}/{yyyy}/{mm}/data.json'

def gen_s3_limit_hours_key(yyyy: str, mm: str):
  return f'{dest_s3_prefix_limit_hours}/{env}/{yyyy}/{mm}/data.json'

def gen_s3_day_of_week_limit_hours_key(day: str, hours: float=None):
  return f'{dest_s3_prefix_day_of_week_limit_hours}/{env}/{day}.json'

def gen_s3_data_key(user_id: str, yyyy: str, mm: str):
  return f'{dest_s3_prefix}/{env}/{user_id}/{yyyy}/{mm}/data.json'

def gen_s3_lockfile_key(user_id: str, yyyy: str, mm: str):
  return f'{dest_s3_prefix}/{env}/{user_id}/{yyyy}/{mm}/lock'

def gen_s3_meisai_key(user_id: str, yyyy: str, mm: str):
  return f'{dest_s3_prefix}/{env}/{user_id}/{yyyy}/{mm}/meisai.json'

def gen_s3_meisai_memo_key(user_id: str, yyyy: str, mm: str):
  return f'{dest_s3_prefix}/{env}/{user_id}/{yyyy}/{mm}/memo.json'

def is_locked(user_id: str, yyyy: str, mm: str) -> bool:
  return myboto3util.s3_file_exists(bucket_name=bucket_name_data_user, filename=gen_s3_lockfile_key(user_id=user_id, yyyy=yyyy, mm=mm))

def fetch_username(user_id: str):
  key = gen_s3_username_key(user_id)
  dest = f'/tmp/{key}'
  download_succeeded = myboto3util.download_s3_file(bucket_name_data_user, key, dest)

  if (download_succeeded):
      with open(dest, 'r') as f:
          return json.load(f)['username']

def fetch_regular_holiday_data(yyyy: str, mm: str):
  key = gen_s3_regular_holiday_data_key(yyyy=yyyy, mm=mm)
  dest = f'/tmp/{key}'
  download_succeeded = myboto3util.download_s3_file(bucket_name_data_admin, key, dest)

  json_data = []
  if download_succeeded:
      with open(dest, 'r') as f:
          json_data += json.load(f)

  return json_data

def fetch_limit_hours_data(yyyy: str, mm: str):
  key = gen_s3_limit_hours_key(yyyy=yyyy, mm=mm)
  dest = f'/tmp/{key}'
  download_succeeded = myboto3util.download_s3_file(bucket_name_data_admin, key, dest)
  json_data = []
  if download_succeeded:
      with open(dest, 'r') as f:
          json_data += json.load(f)
  return json_data

def fetch_day_of_week_limit_hours_data(day: str=None):
  rtn = []
  for _day in [ 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun' ]:
    if day is None or day == _day:
      key = gen_s3_day_of_week_limit_hours_key(day=_day)
      dest = f'/tmp/{key}'
      download_succeeded = myboto3util.download_s3_file(bucket_name_data_admin, key, dest)

      if download_succeeded:
          with open(dest, 'r') as f:
              rtn.append({ _day: json.load(f)['hours'] })

  return rtn

def register_limit_hours(yyyy: str, mm: str, dd: str, hours: float):
  key = gen_s3_limit_hours_key(yyyy=yyyy, mm=mm)
  dest = f'/tmp/{key}'
  download_succeeded = myboto3util.download_s3_file(bucket_name_data_admin, key, dest)

  json_data = []
  if download_succeeded:
      with open(dest, 'r') as f:
          json_data += json.load(f)

  data_key = f'{yyyy}-{mm}-{dd}'

  exists = False
  for a_json_data in json_data:
      if data_key == a_json_data['key']:
          a_json_data['yyyymmdd'] = yyyy+mm+dd
          a_json_data['hours'] = hours
          exists = True
          break

  if not exists:
      json_data.append({
          'key': data_key,
          'yyyymmdd': yyyy+mm+dd,
          'hours': hours,
      })

  s3_bucket_data_admin.put_object(
      Key=key,
      Body=json.dumps(json_data, ensure_ascii=False).encode("utf-8")
      )

  return json_data

def register_day_of_week_limit_hours(day: str, hours: float):
  s3_bucket_data_admin.put_object(
      Key=gen_s3_day_of_week_limit_hours_key(day=day, hours=hours),
      Body=json.dumps({ "hours": hours }, ensure_ascii=False).encode("utf-8")
      )

def register_regular_holiday(json_data: list, yyyymmdd: str):
  yyyy, mm, dd = explode_yyyymmdd(yyyymmdd)

  exists = False
  for _yyyymmdd in json_data:
      if _yyyymmdd == yyyymmdd:
          exists = True
          break

  if not exists:
      json_data.append(yyyymmdd)

  s3_bucket_data_admin.put_object(
      Key=gen_s3_regular_holiday_data_key(yyyy=yyyy, mm=mm),
      Body=json.dumps(json_data, ensure_ascii=False).encode("utf-8")
      )

  return json_data

def unregister_regular_holiday(json_data: list, yyyymmdd: str):
  yyyy, mm, dd = explode_yyyymmdd(yyyymmdd)

  for index, _yyyymmdd in enumerate(json_data):
      if _yyyymmdd == yyyymmdd:
        del json_data[index]
        break

  s3_bucket_data_admin.put_object(
      Key=gen_s3_regular_holiday_data_key(yyyy=yyyy, mm=mm),
      Body=json.dumps(json_data, ensure_ascii=False).encode("utf-8")
      )

  return json_data

def fetch_all_users_shift_data(yyyy: str, mm: str):
  key = gen_s3_data_key(yyyy=yyyy, mm=mm)
  dest = f'/tmp/{key}'

def fetch_shift_data(user_id: str, yyyy: str, mm: str):
  key = gen_s3_data_key(user_id=user_id, yyyy=yyyy, mm=mm)
  dest = f'/tmp/{key}'
  download_succeeded = myboto3util.download_s3_file(bucket_name_data_user, key, dest)
  #print('fetch_shift_data', download_succeeded, 'dest', dest)

  json_data = []
  if download_succeeded:
      with open(dest, 'r') as f:
          json_data += json.load(f)

  return json_data

def fetch_shift_data_with_date(user_id: str, yyyy: str, mm: str, dd: str):
  shift_data = fetch_shift_data(user_id=user_id, yyyy=yyyy, mm=mm)
  target = f'{yyyy}-{mm}-{dd}'
  for an_data in shift_data:
    if is_date_equals(left=target, right=an_data['key']):
      return an_data
  return None

def is_date_equals(left: str, right: str) -> bool:
  splited1 = left.split('-')
  l_yyyy = splited1[0].strip()
  l_mm = splited1[1].strip()
  l_dd = splited1[2].strip()
  splited2 = right.split('-')
  r_yyyy = splited2[0].strip()
  r_mm = splited2[1].strip()
  r_dd = splited2[2].strip()
  return l_yyyy == r_yyyy and l_mm == r_mm and l_dd == r_dd

def put_history(user_id: str):
  # adminリスト用ファイルput
  s3_bucket_data_user.put_object(
      Key=f'history/{env}/{user_id}',
      Body=''
      )

def fetch_meisai(user_id: str, yyyy: str, mm: str):
  key = gen_s3_meisai_key(user_id=user_id, yyyy=yyyy, mm=mm)
  dest = f'/tmp/{key}'
  download_succeeded = myboto3util.download_s3_file(bucket_name_data_user, key, dest)

  json_data = {}
  if download_succeeded:
      with open(dest, 'r') as f:
          json_data = json.load(f)

  return json_data

def fetch_memo(user_id: str, yyyy: str, mm: str):
  key = gen_s3_meisai_memo_key(user_id=user_id, yyyy=yyyy, mm=mm)
  dest = f'/tmp/{key}'
  download_succeeded = myboto3util.download_s3_file(bucket_name_data_user, key, dest)

  json_data = {}
  if download_succeeded:
      with open(dest, 'r') as f:
          json_data = json.load(f)

  return json_data

def recalc_meisai_value(key: str, attribute: str, value: int, meisai: dict):
  meisai[key][attribute] = value
  if key == 'koujo':
    koujo_kei = 0
    for _attribute in meisai[key]:
      if _attribute != 'koujoKei':
        koujo_kei += meisai[key][_attribute]
    meisai[key]['koujoKei'] = koujo_kei
  return meisai

def update_meisai_memo(user_id: str, yyyy: str, mm: str, memo: str):
  s3_bucket_data_user.put_object(
      Key=gen_s3_meisai_memo_key(user_id=user_id, yyyy=yyyy, mm=mm),
      Body=json.dumps({ 'memo': memo }, ensure_ascii=False).encode("utf-8")
      )

def calc_meisai(userid: str, yyyy: str, mm: str, json_data: list):
  return calc.calc_meisai(yyyymm=f'{yyyy}-{mm}', data=json_data, pay_per_hour=fetch_pay_per_hour(userid=userid))

def update_meisai(user_id: str, yyyy: str, mm: str, meisai: dict):
  s3_bucket_data_user.put_object(
      Key=gen_s3_meisai_key(user_id=user_id, yyyy=yyyy, mm=mm),
      Body=json.dumps(meisai, ensure_ascii=False).encode("utf-8")
      )
  return meisai

def gen_datahash(user_id: str, yyyy: str, mm: str):
  """
  import hashlib
  json_data = fetch_shift_data(user_id=user_id, yyyy=yyyy, mm=mm)
  return hashlib.md5(json.dumps(json_data, sort_keys = True).encode("utf-8")).hexdigest()
  """
  import hashlib
  timestamp = myboto3util.s3_get_last_modified_timestamp(bucket_name_data_user, gen_s3_data_key(user_id=user_id, yyyy=yyyy, mm=mm))
  return hashlib.md5(''.join(str(timestamp)).encode()).hexdigest()

def register_date(user_id: str, json_data: list, input_data: dict, dryrun: bool=False):
  name = input_data['name']
  yyyy, mm, dd = pluck_yyyy_mm_dd(input_data)
  data_key = f'{yyyy}-{mm}-{dd}'

  exists = False
  for a_json_data in json_data:
      if data_key == a_json_data['key']:
          a_json_data['name'] = name
          a_json_data['start'] = input_data['start']
          a_json_data['end'] = input_data['end']
          exists = True
          break

  if not exists:
      json_data.append({
          'key': data_key,
          'name': name,
          'start': input_data['start'],
          'end': input_data['end'],
      })

  if not dryrun:
    s3_bucket_data_user.put_object(
        Key=gen_s3_data_key(user_id=user_id, yyyy=yyyy, mm=mm),
        Body=json.dumps(json_data, ensure_ascii=False).encode("utf-8")
        )

  return json_data

def unregister_date(user_id: str, json_data: list, input_data: dict):
  yyyy, mm, dd = pluck_yyyy_mm_dd(input_data)
  data_key = f'{yyyy}-{mm}-{dd}'

  for index, a_json_data in enumerate(json_data):
    if is_date_equals(data_key, a_json_data['key']):
        del json_data[index]
        break

  s3_bucket_data_user.put_object(
      Key=gen_s3_data_key(user_id=user_id, yyyy=yyyy, mm=mm),
      Body=json.dumps(json_data, ensure_ascii=False).encode("utf-8")
      )

  return json_data

def is_data_locked(env: str, userid: str, yyyy: str, mm: str):
    return myboto3util.s3_file_exists(bucket_name=bucket_name_data_user, filename=gen_s3_lockfile_key(user_id=userid, yyyy=yyyy, mm=mm))

def pluck_login_username(headers):
    jwt_token = headers.get("Authorization")
    result = jwt.decode(jwt_token, verify=False)
    return result['cognito:username']

def is_cognito_user_enable(cognito_user_id: str)-> bool:
    response = cognito.admin_get_user(
        UserPoolId=user_pool_id,
        Username=cognito_user_id,
    )
    return response is not None and 'Enabled' in response and response['Enabled'] == True

def fetch_pay_per_hour(userid: str):
  key = gen_s3_pay_per_hour_key(userid)
  dest = f'/tmp/{key}'
  download_succeeded = myboto3util.download_s3_file(bucket_name_data_admin, key, dest)
  if (download_succeeded):
    with open(dest, 'r') as f:
      return json.load(f)['pay_per_hour']
  else:
    return fetch_common_pay_per_hour()

def fetch_common_pay_per_hour():
  key = gen_s3_common_pay_per_hour_key()
  dest = f'/tmp/{key}'
  download_succeeded = myboto3util.download_s3_file(bucket_name_data_admin, key, dest)
  if (download_succeeded):
    with open(dest, 'r') as f:
      return json.load(f)['pay_per_hour']
  else:
    return default_common_pay_per_hour

def update_pay_per_hour(prefix: str, value: int):
  key = gen_s3_pay_per_hour_key(prefix)

  if value > 0:
    s3_bucket_data_admin.put_object(
        Key=key,
        Body=json.dumps({ "pay_per_hour": value }, ensure_ascii=False).encode("utf-8")
        )
  else:
    s3_client.delete_object(Bucket=bucket_name_data_admin, Key=key)