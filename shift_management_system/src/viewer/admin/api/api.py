import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'site-packages'))

import logging
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from pprint import pprint
import boto3
import botocore
import json
import myutil
import myapiutil
from myboto3util import *
from datetime import datetime, timedelta, timezone
import urllib.request

region = os.environ.get("REGION", "ap-northeast-1")
env = os.environ.get("ENV")
project_name = os.environ.get("PROJECT_NAME")
bucket_name_data_admin = os.environ.get("BUCKET_NAME_DATA_ADMIN")
bucket_name_data_user = os.environ.get("BUCKET_NAME_DATA_USER")
bucket_name_viewer_website = os.environ.get("BUCKET_NAME_VIEWER_WEBSITE", "")
bucket_name_viewer_website_dev = os.environ.get("BUCKET_NAME_VIEWER_WEBSITE_DEV", "")
dest_s3_prefix = os.environ.get("DEST_S3_PREFIX")
viewer_website_domain = os.environ.get("VIEWER_WEBSITE_DOMAIN", "")
viewer_website_domain_dev = os.environ.get("VIEWER_WEBSITE_DOMAIN_DEV", "")
user_pool_id = os.environ.get("USER_POOL_ID")
user_pool_client_id = os.environ.get("USER_POOL_CLIENT_ID")
id_pool_id = os.environ.get("ID_POOL_ID")
is_admin = os.environ.get('IS_ADMIN', 'false') == 'true'

config = botocore.client.Config(signature_version='s3v4')
s3_client = boto3.client('s3', region_name=region, config=config)
s3_resource = boto3.resource('s3', region_name=region, config=config)

cognito = boto3.client('cognito-idp')

s3_bucket_data_admin = s3_resource.Bucket(bucket_name_data_admin)
s3_bucket_data_user = s3_resource.Bucket(bucket_name_data_user)

tmp_password = 'Easypass1'

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

def avoid_cors():
    CORS(app, resources={r"/test*": {"origins": "*"}})
    CORS(app, resources={r"/app_hash*": {"origins": "*"}})
    CORS(app, resources={r"/check_data_updated*": {"origins": "*"}})
    CORS(app, resources={r"/get_user*": {"origins": "*"}})
    CORS(app, resources={r"/list_user*": {"origins": "*"}})
    CORS(app, resources={r"/list_shift*": {"origins": "*"}})
    CORS(app, resources={r"/lock_shift*": {"origins": "*"}})
    CORS(app, resources={r"/unlock_shift*": {"origins": "*"}})
    CORS(app, resources={r"/register_user*": {"origins": "*"}})
    CORS(app, resources={r"/update_user*": {"origins": "*"}})
    CORS(app, resources={r"/enable_user*": {"origins": "*"}})
    CORS(app, resources={r"/disable_user*": {"origins": "*"}})
    CORS(app, resources={r"/delete_user*": {"origins": "*"}})
    CORS(app, resources={r"/fetch_limit_hours_data*": {"origins": "*"}})
    CORS(app, resources={r"/fetch_day_of_week_limit_hours_data*": {"origins": "*"}})
    CORS(app, resources={r"/register_day_of_week_limit_hours*": {"origins": "*"}})
    CORS(app, resources={r"/register_limit_hours*": {"origins": "*"}})
    CORS(app, resources={r"/register_date*": {"origins": "*"}})
    CORS(app, resources={r"/unregister_date*": {"origins": "*"}})
    CORS(app, resources={r"/fetch_data*": {"origins": "*"}})
    CORS(app, resources={r"/fetch_username*": {"origins": "*"}})
    CORS(app, resources={r"/server_info*": {"origins": "*"}})
    CORS(app, resources={r"/update_meisai_value*": {"origins": "*"}})
    CORS(app, resources={r"/update_meisai_memo*": {"origins": "*"}})
    CORS(app, resources={r"/fetch_regular_holiday_data*": {"origins": "*"}})
    CORS(app, resources={r"/register_regular_holiday*": {"origins": "*"}})
    CORS(app, resources={r"/unregister_regular_holiday*": {"origins": "*"}})
    CORS(app, resources={r"/fetch_pay_per_hour*": {"origins": "*"}})
    CORS(app, resources={r"/update_pay_per_hour*": {"origins": "*"}})
avoid_cors()

debug = True if os.environ.get('DEBUG', "false") == "true" else False

logging.basicConfig()
logger = logging.getLogger(__name__)

if debug:
    app.logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    #print('setLogLevel DEBUG')
else:
    app.logger.setLevel(logging.WARN)
    logger.setLevel(logging.WARN)
    #print('setLogLevel WARN')

@app.route('/test', methods=['OPTIONS'])
def options(event=None, context=None):
    response = make_response(jsonify({}))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response

@app.route('/test', methods=['GET'])
def test(event=None, context=None):
    response = make_response(jsonify({ 'test': 'test' }))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response

@app.route('/server_info', methods=['GET'])
def server_info(event=None, context=None):
    result = {}
    for key in os.environ.keys():
        if key in ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_SESSION_TOKEN', 'ADMIN_USER_LIST']:
            continue
        result[key] = os.environ.get(key, '')
    response = make_response(jsonify(result))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response

@app.route('/app_hash', methods=['GET'])
def app_hash(event=None, context=None):
    result = {}
    lines = []
    last_modified_timestamp = 0.0
    def fetch_index_html_contents(bucket: str):
        lines = []
        def download_from_s3bucket(bucket: str, key: str, dest: str):
            #print("[Debug] downloading... bucket: {} / key: {} / dest: {}".format(bucket, key, dest))
            try:
                s3_resource.Bucket(bucket).download_file(key, dest)
            except botocore.exceptions.ClientError as e:
                #print("[Error] something wrong with download: {} ".format(e.response['Error']))
                raise
            #print("[Debug] done.")
            return dest
        dst = download_from_s3bucket(bucket, 'index.html', '/tmp/index.html')
        with open(dst, 'r') as f:
            lines.extend(f.readlines())
        return lines

    def fetch_index_html_contents(parsed_url) -> str:
        html_url = f'{parsed_url.scheme}://{parsed_url.netloc}/{parsed_url.path}'
        request = urllib.request.Request(url=html_url, method='GET')
        with urllib.request.urlopen(request) as response:
            return response.read().decode('utf-8')
        return ''

    def get_last_modified_timestamp(bucket: str, key: str) -> float:
        try:
            response = s3_client.head_object(Bucket=bucket, Key=key)
            return response['LastModified']
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                return 0.0
            else:
                raise e

    if request.args.get('origin'):
        origin = request.args.get('origin')
        from urllib.parse import urlparse
        parsed_url = urlparse(origin)
        domain = parsed_url.netloc
        """
        print('origin', origin, \
          'url', parsed_url.geturl(), \
          'domain', domain, \
          'scheme', parsed_url.scheme, \
          'port', parsed_url.port, \
          'path', parsed_url.path, \
          'hostname', parsed_url.hostname, \
          'params', parsed_url.params, \
          'query', parsed_url.query, \
          )
        """

        # index.htmlの内容を取得
        if domain == viewer_website_domain:
            lines += fetch_index_html_contents(bucket_name_viewer_website)
            #last_modified_timestamp = get_last_modified_timestamp(bucket_name_viewer_website, 'index.html')
        elif domain == viewer_website_domain_dev:
            lines += fetch_index_html_contents(bucket_name_viewer_website_dev)
            #last_modified_timestamp = get_last_modified_timestamp(bucket_name_viewer_website_dev, 'index.html')
        else:
            lines += fetch_index_html_contents(parsed_url)

    import hashlib
    result['hash'] = hashlib.md5(''.join(lines).encode()).hexdigest()
    #result['hash'] = hashlib.md5(str(last_modified_timestamp).encode()).hexdigest()

    response = make_response(jsonify(result))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response

@app.route('/check_data_updated/<userid>/<yyyymm>', methods=['GET'])
def check_data_updated(event=None, context=None, userid=None, yyyymm=None):
    result = {}
    try:
        yyyy = yyyymm[0:4]
        mm = yyyymm[5:7]
        result['hash'] = myapiutil.gen_datahash(user_id=userid, yyyy=yyyy, mm=mm)

    except Exception as e:
        print('\033[31m', e, '\033[0m')
        raise
    finally:
        pass

    response = make_response(jsonify(result))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response

@app.route('/fetch_username/<userid>', methods=['GET'])
def fetch_username(event=None, context=None, userid=None):
    result = {}
    try:
        result['username'] = myapiutil.fetch_username(userid)
    except Exception as e:
        print('\033[31m', e, '\033[0m')
        raise
    finally:
        pass
    response = make_response(jsonify(result))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response

@app.route('/fetch_data/<userid>/<yyyymm>', methods=['GET'])
def fetch_data(event=None, context=None, userid=None, yyyymm=None):
    result = {}
    data = []
    regular_holiday_data = []
    limit_hours_data = []
    day_of_week_limit_hours_data = []
    workable_hours_left_data = {}
    meisai = {}
    is_locked = False
    try:
        yyyy = yyyymm[0:4]
        mm = yyyymm[5:7]
        data = myapiutil.fetch_shift_data(user_id=userid, yyyy=yyyy, mm=mm)
        is_locked = myapiutil.is_locked(user_id=userid, yyyy=yyyy, mm=mm)
        meisai = myapiutil.fetch_meisai(user_id=userid, yyyy=yyyy, mm=mm)
        result['memo'] = myapiutil.fetch_memo(user_id=userid, yyyy=yyyy, mm=mm)
        result['hash'] = myapiutil.gen_datahash(user_id=userid, yyyy=yyyy, mm=mm)
        regular_holiday_data = myapiutil.fetch_regular_holiday_data(yyyy=yyyy, mm=mm)
        limit_hours_data = myapiutil.fetch_limit_hours_data(yyyy=yyyy, mm=mm)
        day_of_week_limit_hours_data = myapiutil.fetch_day_of_week_limit_hours_data(day=None)
        workable_hours_left_data = fetch_workable_hours_left_data(yyyy=yyyy, mm=mm, limit_hours_data=limit_hours_data, day_of_week_limit_hours_data=day_of_week_limit_hours_data)
    except Exception as e:
        print('\033[31m', e, '\033[0m')
        raise
    finally:
        pass

    result['data'] = data
    result['meisai'] = meisai
    result['regular_holiday_data'] = regular_holiday_data
    result['limit_hours_data'] = limit_hours_data
    result['day_of_week_limit_hours_data'] = day_of_week_limit_hours_data
    result['workable_hours_left_data'] = workable_hours_left_data
    result['isLocked'] = is_locked
    response = make_response(jsonify(result))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response

def fetch_workable_hours_left_data(yyyy: str, mm: str, limit_hours_data: list, day_of_week_limit_hours_data: list, own_user_id: str=None, own_shift_data: list=None):
    workable_hours_left_data = {}
    all_users = myapiutil.fetch_all_users_in_group(user_pool_id=user_pool_id, group_name=env)
    for user in all_users:
      Enabled = user.get('Enabled', False)
      if not Enabled:
        continue
      UserStatus = user.get('UserStatus')
      if not UserStatus == 'CONFIRMED':
        continue
      UserId = user.get('Username')

      shift_data = None
      if UserId == own_user_id:
        shift_data = own_shift_data
      if shift_data is None:
        shift_data = myapiutil.fetch_shift_data(user_id=UserId, yyyy=yyyy, mm=mm)

      if len(shift_data) > 0:
        for s_data in shift_data:
          yyyymmdd = s_data['key'].lstrip().rstrip()
          start = myutil.str_2_datetime(s_data['start'], '%Y-%m-%d %H:%M')
          end   = myutil.str_2_datetime(s_data['end'], '%Y-%m-%d %H:%M')
          diff = end - start
          diff_in_sec = diff.total_seconds()
          diff_in_min = diff_in_sec / 60
          diff_in_hours = myutil.my_floor(diff_in_min / 60, 1)

          def find_limit_hours(yyyymmdd: str) -> int:
            for l in limit_hours_data:
              if yyyymmdd.replace('-', '') == l['yyyymmdd'].replace('-', ''):
                return float(l['hours'])
            return 0
          limit_hours = find_limit_hours(yyyymmdd)

          if limit_hours == 0:
            weekday = myutil.str_2_datetime(yyyymmdd, '%Y-%m-%d').strftime('%A')[0:3].lower()

            def find_fixed_weekday_limit_hours(weekday: str) -> float:
              for d in day_of_week_limit_hours_data:
                if list(d.keys())[0] == weekday:
                  return d[list(d.keys())[0]]
              return 0
            limit_hours = find_fixed_weekday_limit_hours(weekday)

          if limit_hours > 0:
            workable_hours_left = workable_hours_left_data.get(yyyymmdd, limit_hours)
            workable_hours_left -= diff_in_hours
            workable_hours_left_data[yyyymmdd] = workable_hours_left

      for l in limit_hours_data:
        if l['hours'] > 0:
          if not l['key'] in workable_hours_left_data:
            workable_hours_left_data[l['key']] = l['hours']

    return workable_hours_left_data

@app.route('/get_user', methods=['GET'])
def get_user(event=None, context=None):
    result = {}
    try:
        data = request.get_json()

        response = cognito.admin_get_user(
            UserPoolId=user_pool_id,
            Username=data['userId'],
        )

    except Exception as e:
        print('\033[31m', e, '\033[0m')
        raise
    finally:
        pass
    response = make_response(jsonify(result))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response

@app.route('/list_shift', methods=['GET'])
def list_shift(event=None, context=None):
    result = {}
    users = []
    preview = {}
    try:
        data = request.get_json()

        s3objects = get_s3objects_list(bucket_name_data_user, f'history/{env}')
        for obj in s3objects:
            key = obj['Key']
            userId = key.split('/')[-1]
            _env = key.split('/')[-2]
            usernameJa = ''

            key = f'username/{userId}/username.json'
            dest = f'/tmp/{key}'
            download_succeeded = download_s3_file(bucket_name_data_user, key, dest)
            if (download_succeeded):
                with open(dest, 'r') as f:
                    json_data = json.load(f)
                    usernameJa = json_data['username']

            users.append({
                'Username': userId,
                'UsernameJa': usernameJa,
                'Env': _env,
            })

            # fetch preview
            jst = timezone(timedelta(hours=+9), 'JST')
            now = datetime.now(jst)
            next_day = now + timedelta(days=1)
            str_day = myutil.datetime_2_str(dt=next_day, datetime_format='%Y-%m-%d')
            yyyy = str_day.split('-')[0]
            mm = str_day.split('-')[1]
            dd = str_day.split('-')[2]
            preview[userId] = myapiutil.fetch_shift_data_with_date(user_id=userId, yyyy=yyyy, mm=mm, dd=dd)

    except Exception as e:
        print('\033[31m', e, '\033[0m')
        raise
    finally:
        pass

    result['data'] = users
    result['preview'] = preview
    response = make_response(jsonify(result))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response

@app.route('/list_user', methods=['GET'])
def list_user(event=None, context=None):
    result = {}
    try:
        Users = fetch_all_users_in_group_with_username_ja(group_name=env)
        result['data'] = Users
    except Exception as e:
        print('\033[31m', e, '\033[0m')
        raise
    finally:
        pass
    response = make_response(jsonify(result))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response

@app.route('/register_user', methods=['POST'])
def register_user(event=None, context=None):
    result = {}
    try:
        data = request.get_json()

        try:
            cognito.add_custom_attributes(
                UserPoolId=user_pool_id,
                CustomAttributes=[
                    {
                        'Name': 'ENV',
                        'AttributeDataType': 'String',
                        'DeveloperOnlyAttribute': False,
                        'Mutable': False,
                    }
                ]
                )
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'InvalidParameterException':
                if 'Existing attribute already has name' in e.response['Error']['Message']:
                    pass
                else:
                    raise e
            else:
                raise e

        try:
            cognito.create_group(UserPoolId=user_pool_id, GroupName=env)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'GroupExistsException':
                pass
            else:
                raise e

        try:
            response = cognito.admin_create_user(
                UserPoolId=user_pool_id,
                Username=data['userId'],
                MessageAction='SUPPRESS',
                TemporaryPassword=tmp_password,
                UserAttributes=[
                    {
                        'Name': 'custom:ENV',
                        'Value': env,
                    },
                ],
            )
        except botocore.exceptions.ClientError as e:
            raise e

        cognito.admin_add_user_to_group(UserPoolId=user_pool_id, Username=data['userId'], GroupName=env)

        response = cognito.admin_initiate_auth(
            UserPoolId=user_pool_id,
            ClientId=user_pool_client_id,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': data['userId'],
                'PASSWORD': tmp_password,
            },
        )
        session = response['Session']

        response = cognito.admin_respond_to_auth_challenge(
            UserPoolId=user_pool_id,
            ClientId=user_pool_client_id,
            ChallengeName='NEW_PASSWORD_REQUIRED',
            ChallengeResponses={ 'USERNAME': data['userId'], 'NEW_PASSWORD': data['password'] },
            Session=session
        )
        #print(response)

        key = f'username/{data["userId"]}/username.json'
        response = s3_bucket_data_user.put_object(
            Key=key,
            Body=json.dumps({ 'username': data['username'] }, ensure_ascii=False).encode("utf-8")
            )

    except Exception as e:
        print('\033[31m', e, '\033[0m')
        raise
    finally:
        pass
    response = make_response(jsonify(result))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response

@app.route('/update_meisai_value', methods=['POST'])
def update_meisai_value(event=None, context=None):
    result = {}
    meisai = {}
    try:
        data = request.get_json()
        #pprint(data)

        userid = data['userid']
        yyyymm = data['yyyymm']
        yyyy = yyyymm[0:4]
        mm = yyyymm[5:7]
        key = data['key']
        attribute = data['attribute']
        value = int(data['value'])

        meisai = myapiutil.fetch_meisai(user_id=userid, yyyy=yyyy, mm=mm)

        if len(meisai) == 0:
            json_data = myapiutil.fetch_shift_data(user_id=userid, yyyy=yyyy, mm=mm)
            meisai = myapiutil.calc_meisai(userid=userid, yyyy=yyyy, mm=mm, json_data=json_data)

        meisai = myapiutil.recalc_meisai_value(key=key, attribute=attribute, value=value, meisai=meisai)

        myapiutil.update_meisai(user_id=userid, yyyy=yyyy, mm=mm, meisai=meisai)

    except Exception as e:
        print('\033[31m', e, '\033[0m')
        raise
    finally:
        pass

    result['meisai'] = meisai
    response = make_response(jsonify(result))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response

@app.route('/update_meisai_memo', methods=['POST'])
def update_meisai_memo(event=None, context=None):
    result = {}
    meisai = {}
    try:
        data = request.get_json()
        #pprint(data)

        userid = data['userid']
        yyyymm = data['yyyymm']
        yyyy = yyyymm[0:4]
        mm = yyyymm[5:7]
        memo = data.get('memo', '')

        meisai = myapiutil.update_meisai_memo(user_id=userid, yyyy=yyyy, mm=mm, memo=memo)

    except Exception as e:
        print('\033[31m', e, '\033[0m')
        raise
    finally:
        pass

    result['meisai'] = meisai
    response = make_response(jsonify(result))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response

@app.route('/update_user', methods=['POST'])
def update_user(event=None, context=None):
    result = {}
    try:
        data = request.get_json()
        #pprint(data)

        if data.get('editpassword', '0') == '1' and data.get('oldpassword') is not None and data.get('newpassword') is not None:

            response = cognito.admin_initiate_auth(
                UserPoolId=user_pool_id,
                ClientId=user_pool_client_id,
                AuthFlow='ADMIN_NO_SRP_AUTH',
                AuthParameters={
                    'USERNAME': data['userId'],
                    'PASSWORD': data['oldpassword'],
                },
            )
            token = response['AuthenticationResult']['AccessToken']

            response = cognito.change_password(
                PreviousPassword=data['oldpassword'],
                ProposedPassword=data['newpassword'],
                AccessToken=token
            )
            #print(response)

            response = cognito.admin_user_global_sign_out(
                UserPoolId=user_pool_id,
                Username=data['userId'],
            )
            #print(response)

        key = f'username/{data["userId"]}/username.json'
        response = s3_bucket_data_user.put_object(
            Key=key,
            Body=json.dumps({ 'username': data['username'] }, ensure_ascii=False).encode("utf-8")
            )

    except Exception as e:
        print('\033[31m', e, '\033[0m')
        raise
    finally:
        pass
    response = make_response(jsonify(result))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response

@app.route('/enable_user', methods=['POST'])
def enable_user(event=None, context=None):
    result = {}
    try:
        data = request.get_json()

        response = cognito.admin_enable_user(
            UserPoolId=user_pool_id,
            Username=data['userId'],
        )
        #print(response)

    except Exception as e:
        print('\033[31m', e, '\033[0m')
        raise
    finally:
        pass
    response = make_response(jsonify(result))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response

@app.route('/disable_user', methods=['POST'])
def disable_user(event=None, context=None):
    result = {}
    try:
        data = request.get_json()

        response = cognito.admin_disable_user(
            UserPoolId=user_pool_id,
            Username=data['userId'],
        )
        #print(response)

    except Exception as e:
        print('\033[31m', e, '\033[0m')
        raise
    finally:
        pass
    response = make_response(jsonify(result))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response

@app.route('/delete_user', methods=['DELETE'])
def delete_user(event=None, context=None):
    result = {}
    try:
        data = request.get_json()

        response = cognito.admin_delete_user(
            UserPoolId=user_pool_id,
            Username=data['userId'],
        )
        #print(response)

    except Exception as e:
        print('\033[31m', e, '\033[0m')
        raise
    finally:
        pass
    response = make_response(jsonify(result))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response

@app.route('/lock_shift', methods=['POST'])
def lock_shift(event=None, context=None):
    result = {}
    try:
        data = request.get_json()
        #pprint(data)

        userid = data['userId']
        yyyy = data['yyyymm'][0:4]
        mm = data['yyyymm'][5:7]

        s3_bucket_data_user.put_object(
            Key=myapiutil.gen_s3_lockfile_key(user_id=userid, yyyy=yyyy, mm=mm),
            Body='',
            )

    except Exception as e:
        print('\033[31m', e, '\033[0m')
        raise
    finally:
        pass
    response = make_response(jsonify(result))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response

@app.route('/unlock_shift', methods=['POST'])
def unlock_shift(event=None, context=None):
    result = {}
    try:
        data = request.get_json()
        #pprint(data)

        userid = data['userId']
        yyyy = data['yyyymm'][0:4]
        mm = data['yyyymm'][5:7]

        s3_client.delete_object(
            Bucket=bucket_name_data_user,
            Key=myapiutil.gen_s3_lockfile_key(user_id=userid, yyyy=yyyy, mm=mm),
        )

    except Exception as e:
        print('\033[31m', e, '\033[0m')
        raise
    finally:
        pass
    response = make_response(jsonify(result))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response

@app.route('/fetch_regular_holiday_data/<yyyymm>', methods=['GET'])
def fetch_regular_holiday_data(event=None, context=None, yyyymm=None):
    result = {}
    data = []
    try:
        yyyy = yyyymm[0:4]
        mm = yyyymm[5:7]
        data = myapiutil.fetch_regular_holiday_data(yyyy=yyyy, mm=mm)
    except Exception as e:
        print('\033[31m', e, '\033[0m')
        raise
    finally:
        pass

    result['data'] = data
    response = make_response(jsonify(result))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response

@app.route('/register_regular_holiday', methods=['POST'])
def register_regular_holiday(event=None, context=None):
    result = {}
    try:
        data = request.get_json()
        #pprint(data)

        yyyymmdd = data.get('yyyymmdd')
        yyyy, mm, dd = myapiutil.explode_yyyymmdd(yyyymmdd)

        json_data = myapiutil.fetch_regular_holiday_data(yyyy=yyyy, mm=mm)

        myapiutil.register_regular_holiday(json_data=json_data, yyyymmdd=yyyymmdd)

    except Exception as e:
        print('\033[31m', e, '\033[0m')
        raise
    finally:
        pass
    response = make_response(jsonify(result))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response

@app.route('/unregister_regular_holiday', methods=['POST'])
def unregister_regular_holiday(event=None, context=None):
    result = {}
    try:
        data = request.get_json()
        #pprint(data)

        yyyymmdd = data.get('yyyymmdd')
        yyyy, mm, dd = myapiutil.explode_yyyymmdd(yyyymmdd)

        json_data = myapiutil.fetch_regular_holiday_data(yyyy=yyyy, mm=mm)

        myapiutil.unregister_regular_holiday(json_data=json_data, yyyymmdd=yyyymmdd)

    except Exception as e:
        print('\033[31m', e, '\033[0m')
        raise
    finally:
        pass
    response = make_response(jsonify(result))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response

@app.route('/fetch_limit_hours_data/<yyyymm>', methods=['GET'])
def fetch_limit_hours_data(event=None, context=None, yyyymm=None):
    result = {}
    data = []
    regular_holiday_data = []
    day_of_week_limit_hours_data = []
    try:
        yyyy = yyyymm[0:4]
        mm = yyyymm[5:7]
        data = myapiutil.fetch_limit_hours_data(yyyy=yyyy, mm=mm)
        regular_holiday_data = myapiutil.fetch_regular_holiday_data(yyyy=yyyy, mm=mm)
        day_of_week_limit_hours_data = myapiutil.fetch_day_of_week_limit_hours_data(day=None)
    except Exception as e:
        print('\033[31m', e, '\033[0m')
        raise
    finally:
        pass
    result['data'] = data
    result['regular_holiday_data'] = regular_holiday_data
    result['day_of_week_limit_hours_data'] = day_of_week_limit_hours_data
    response = make_response(jsonify(result))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response

@app.route('/fetch_day_of_week_limit_hours_data', methods=['GET'])
@app.route('/fetch_day_of_week_limit_hours_data/<day>', methods=['GET'])
def fetch_day_of_week_limit_hours_data(event=None, context=None, day=None):
    result = {}
    data = []
    try:
        data = myapiutil.fetch_day_of_week_limit_hours_data(day=day)
    except Exception as e:
        print('\033[31m', e, '\033[0m')
        raise
    finally:
        pass

    result['data'] = data
    response = make_response(jsonify(result))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response


@app.route('/register_day_of_week_limit_hours', methods=['POST'])
def register_day_of_week_limit_hours(event=None, context=None):
    result = {}
    try:
        data = request.get_json()
        day = data.get('day')
        hours = float(data.get('hours'))
        #pprint(data)

        myapiutil.register_day_of_week_limit_hours(day=day, hours=hours)

    except Exception as e:
        print('\033[31m', e, '\033[0m')
        raise
    finally:
        pass
    response = make_response(jsonify(result))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response

@app.route('/register_limit_hours', methods=['POST'])
def register_limit_hours(event=None, context=None):
    result = {}
    try:
        data = request.get_json()
        yyyymmdd = data.get('yyyymmdd')
        hours = float(data.get('hours'))
        #pprint(data)

        yyyy, mm, dd = myapiutil.explode_yyyymmdd(yyyymmdd)

        myapiutil.register_limit_hours(yyyy=yyyy, mm=mm, dd=dd, hours=hours)

    except Exception as e:
        print('\033[31m', e, '\033[0m')
        raise
    finally:
        pass
    response = make_response(jsonify(result))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response

@app.route('/register_date', methods=['POST'])
def register_date(event=None, context=None):
    result = {}
    try:
        data = request.get_json()
        #pprint(data)

        userid = data['userId']
        yyyy, mm, dd = myapiutil.pluck_yyyy_mm_dd(data)
        data_hash = data.get('hash')

        result['prev_hash'] = myapiutil.gen_datahash(user_id=userid, yyyy=yyyy, mm=mm)

        #regular_holiday_data = myapiutil.fetch_regular_holiday_data(yyyy=yyyy, mm=mm)
        limit_hours_data = myapiutil.fetch_limit_hours_data(yyyy=yyyy, mm=mm)
        day_of_week_limit_hours_data = myapiutil.fetch_day_of_week_limit_hours_data(day=None)
        result['limit_hours'] = limit_hours_data
        result['day_of_week_limit_hours_data'] = day_of_week_limit_hours_data

        # まずは、dry run
        json_data = myapiutil.fetch_shift_data(user_id=userid, yyyy=yyyy, mm=mm)
        workable_hours_left_data = fetch_workable_hours_left_data(
          yyyy=yyyy,
          mm=mm,
          limit_hours_data=limit_hours_data,
          day_of_week_limit_hours_data=day_of_week_limit_hours_data,
          own_user_id=userid,
          own_shift_data=json_data)
        #pprint(workable_hours_left_data)

        myapiutil.register_date(user_id=userid, json_data=json_data, input_data=data, dryrun=True)
        workable_hours_left_data = fetch_workable_hours_left_data(
          yyyy=yyyy,
          mm=mm,
          limit_hours_data=limit_hours_data,
          day_of_week_limit_hours_data=day_of_week_limit_hours_data,
          own_user_id=userid,
          own_shift_data=json_data)
        #pprint(workable_hours_left_data)

        workable_hours_left = workable_hours_left_data.get(f'{yyyy}-{mm}-{dd}', 9999)

        error = False
        if is_admin or workable_hours_left >= 0:
          myapiutil.register_date(user_id=userid, json_data=json_data, input_data=data)

          # adminリスト用ファイルput
          myapiutil.put_history(user_id=userid)

          meisai = myapiutil.calc_meisai(userid=userid, yyyy=yyyy, mm=mm, json_data=json_data)
          myapiutil.update_meisai(user_id=userid, yyyy=yyyy, mm=mm, meisai=meisai)
          result['meisai'] = meisai

          result['hash'] = myapiutil.gen_datahash(user_id=userid, yyyy=yyyy, mm=mm)

          workable_hours_left_data = fetch_workable_hours_left_data(
            yyyy=yyyy,
            mm=mm,
            limit_hours_data=limit_hours_data,
            day_of_week_limit_hours_data=day_of_week_limit_hours_data)
          #pprint(workable_hours_left_data)
          result['workable_hours_left_data'] = workable_hours_left_data

        else:
          # 残時間がマイナス値になる場合エラー
          error = True

          workable_hours_left_data = fetch_workable_hours_left_data(
            yyyy=yyyy,
            mm=mm,
            limit_hours_data=limit_hours_data,
            day_of_week_limit_hours_data=day_of_week_limit_hours_data)
          #pprint(workable_hours_left_data)
          result['workable_hours_left_data'] = workable_hours_left_data

        result["error"] = error

    except Exception as e:
        print('\033[31m', e, '\033[0m')
        raise
    finally:
        pass
    response = make_response(jsonify(result))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response

@app.route('/unregister_date', methods=['POST'])
def unregister_date(event=None, context=None):
    result = {}
    try:
        data = request.get_json()
        #pprint(data)

        userid = data['userId']
        yyyy, mm, dd = myapiutil.pluck_yyyy_mm_dd(data)
        data_hash = data.get('hash')

        result['prev_hash'] = myapiutil.gen_datahash(user_id=userid, yyyy=yyyy, mm=mm)

        json_data = myapiutil.fetch_shift_data(user_id=userid, yyyy=yyyy, mm=mm)

        myapiutil.unregister_date(user_id=userid, json_data=json_data, input_data=data)

        meisai = myapiutil.calc_meisai(userid=userid, yyyy=yyyy, mm=mm, json_data=json_data)
        myapiutil.update_meisai(user_id=userid, yyyy=yyyy, mm=mm, meisai=meisai)
        result['meisai'] = meisai

        result['hash'] = myapiutil.gen_datahash(user_id=userid, yyyy=yyyy, mm=mm)

        limit_hours_data = myapiutil.fetch_limit_hours_data(yyyy=yyyy, mm=mm)
        day_of_week_limit_hours_data = myapiutil.fetch_day_of_week_limit_hours_data(day=None)
        result['workable_hours_left_data'] = fetch_workable_hours_left_data(yyyy=yyyy, mm=mm, limit_hours_data=limit_hours_data, day_of_week_limit_hours_data=day_of_week_limit_hours_data)

    except Exception as e:
        print('\033[31m', e, '\033[0m')
        raise
    finally:
        pass
    response = make_response(jsonify(result))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response

@app.route('/fetch_pay_per_hour', methods=['GET'])
@app.route('/fetch_pay_per_hour/<userid>', methods=['GET'])
def fetch_pay_per_hour(event=None, context=None, userid=None):
    result = {}
    data = []
    try:
      commonJiKyuu = myapiutil.fetch_common_pay_per_hour()
      result['common_jikyuu'] = commonJiKyuu
      Users = fetch_all_users_in_group_with_username_ja(group_name=env)
      for u in Users:
          Username = u['Username']
          u['jikyuu'] = myapiutil.fetch_pay_per_hour(userid=Username)
      result['jikyuu'] = Users
    except Exception as e:
        print('\033[31m', e, '\033[0m')
        raise
    finally:
        pass

    result['data'] = data
    response = make_response(jsonify(result))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response

@app.route('/update_pay_per_hour', methods=['POST'])
def update_pay_per_hour(event=None, context=None):
    result = {}
    try:
        data = request.get_json()
        #pprint(data)

        userid = data['userid']
        value = int(data['value'])

        myapiutil.update_pay_per_hour(prefix=userid, value=value)

        commonJiKyuu = myapiutil.fetch_common_pay_per_hour()
        result['common_jikyuu'] = commonJiKyuu
        Users = fetch_all_users_in_group_with_username_ja(group_name=env)
        for u in Users:
            Username = u['Username']
            u['jikyuu'] = myapiutil.fetch_pay_per_hour(userid=Username)
        result['jikyuu'] = Users

    except Exception as e:
        print('\033[31m', e, '\033[0m')
        raise
    finally:
        pass

    response = make_response(jsonify(result))
    response.headers['Content-type'] = 'application/json; charset=utf-8'
    return response

def fetch_all_users_in_group_with_username_ja(group_name: str):
    Users = myapiutil.fetch_all_users_in_group(user_pool_id=user_pool_id, group_name=group_name)
    for u in Users:
        Username = u['Username']
        key = f'username/{Username}/username.json'
        dest = f'/tmp/{key}'
        download_succeeded = download_s3_file(bucket_name_data_user, key, dest)
        if (download_succeeded):
            with open(dest, 'r') as f:
                json_data = json.load(f)
                u['UsernameJa'] = json_data['username']
    return Users

def get_s3objects_list(bucket: str, prefix=''):
    contents = []
    response = s3_client.list_objects_v2(
        Bucket=bucket,
        Prefix=prefix,
    )
    if 'Contents' in response:
        contents.extend(response['Contents'])

    #次ページが有る場合、NextContinuationTokenがresponseに含まれているため、次のリクエスト時に'ContinuationToken'に指定している。
    while 'NextContinuationToken' in response:
        token = response['NextContinuationToken']
        response = s3_client.list_objects_v2(
            Bucket=bucket,
            ContinuationToken=token,
        )
        if 'Contents' in response:
            contents.extend(response["Contents"])

    # responseに最後の更新時刻('LastModified')が含まれているのでそれでソート
    return sorted(contents, key=lambda c: c['LastModified'])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 80)), debug=debug)
