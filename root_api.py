from urllib.parse import quote_plus

import requests
import json

from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
import time

APP_KEY = "21646297"
TT_ID = '227200%40taobao_android_9.12.0'
APP_VER = "9.12.0"
LAT = ""
LNG = ""
UTD_ID = 'X03fKfpe1UYDAPhdFrObFmvR'
DEVICE_ID = 'AoPbqzQ7rFhQeS0-m3_BCGvdwz6-7zWFTdENB99iwyEc'
SIGN_SERVER = 'http://192.168.2.225:6780/xsign'

UC_SERVER = "http://192.168.79.60:2778/queryUser"


def get_cur_time(length: int = 0):
    return int(time.time() * pow(10, length))


def get_sign_dic(sign_server, payload: dict):
    headers = {
        "content-type": "application/json;charset=utf-8"
    }
    res = requests.post(sign_server, data=json.dumps(payload), headers=headers)
    return res.json()


def get_curr_user(uc_server):
    headers = {
        "content-type": "application/json;charset=utf-8"
    }
    res = requests.post(uc_server, data=json.dumps('{}'), headers=headers)
    res_content = res.content
    user_dic = {}
    if res.status_code == requests.codes.ok:
        user_dic = json.loads(res_content.decode())
    return user_dic


def get_sign(api, version, data: str, t, sign_server, page_id='', page_name='', uid='', sid='',
             features='27'):
    disable_warnings(InsecureRequestWarning)
    pre_sign_data = {
        "uid": uid,
        "ttid": TT_ID,
        "data": quote_plus(data),
        "lng": LNG,
        "utdid": UTD_ID,
        "api": api,
        "lat": LAT,
        "deviceId": DEVICE_ID,
        "sid": sid,
        "x-features": features,
        "v": version,
        "t": str(t),
        "pageName": page_name,
        "pageId": page_id
    }
    sign_dic = get_sign_dic(sign_server, pre_sign_data)
    return sign_dic


def gw_api(api, version, data: str, host, page_id='', page_name='', uid='', sid='', features='27',
           use_cookie=False, cookie='', method='GET'):
    t = get_cur_time()
    sign_dict = get_sign(api, version, data, t, SIGN_SERVER, page_id, page_name, uid, sid, features)
    body = "data=" + quote_plus(data)
    req_url = "https://{}/gw/{}/{}/".format(host, api, version)
    headers = {
        "x-m-biz-live-bizcode": "TAOBAO",
        "x-features": features,
        "x-sgext": sign_dict['result']['x-sgext'],
        "c-launch-info": "0,0,1588652065055,1588651952000,3",
        "x-page-name": page_name,
        "User-Agent": "MTOPSDK%2F3.1.1.7+%28Android%3B6.0.1%3BSamsung%3BGalaxy+S8%29",
        "x-ttid": quote_plus(TT_ID),
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
        "a-orange-q": "appKey=21646297&appVersion=9.6.1&clientAppIndexVersion=1120200504231704166&clientVersionIndexVersion=0",
        "x-region-channel": "CN",
        "x-appkey": APP_KEY,
        "x-nq": "WIFI",
        "x-mini-wua": quote_plus(sign_dict['result']['x-mini-wua']),
        "x-c-traceid": "XpF17gMK9P0DAM5H9D8NAKDU15886444930540109121941",
        "x-SLIDER-Q": "appKey%3D21646297%26ver%3D1588443286014",
        "x-app-conf-v": str(19),
        "x-bx-version": "6.4.16",
        "x-pv": "6.3",
        "x-t": str(t),
        "x-app-ver": APP_VER,
        "f-refer": "mtop",
        "x-nettype": "WIFI",
        "x-utdid": UTD_ID,
        "x-umt": quote_plus(sign_dict['result']['x-umt']),
        "x-devid": DEVICE_ID,
        "x-sign": quote_plus(sign_dict['result']['x-sign']),
        "x-page-url": quote_plus(page_id),
        "x-location": quote_plus("{0},{1}".format(LNG, LAT)),
        "Host": host
    }
    if uid != "":
        headers["x-uid"] = uid

    if sid != "":
        headers["x-sid"] = sid
    if use_cookie:
        headers["Cookie"] = cookie
    if method.upper() == 'GET':
        req_url = (req_url + "?{0}").format(body)
        r = requests.get(req_url, headers=headers, verify=False)
        content = r.text
    else:
        content = requests.post(req_url, data=body, headers=headers, verify=True).text

    return content


if __name__ == '__main__':
    # user = get_curr_user(UC_SERVER)
    # uid = user['result']['uid']
    # sid = user['result']['sid']
    data = r'{"accountType":"3","dataTypeIdMap":"{\"imCmd\":1,\"imMsg\":38,\"imGroupEvent\":56,\"tao_friend\":3,\"imba\":1318,\"imbaCmd\":0,\"imba_relation\":15}","fetchSize":"30","firstReq":"false","namespace":"0","readModeSyncMap":"{}","sdkVersion":"1"}'
    version = "1.0"
    api = "mtop.com.taobao.wireless.amp.newsync"
    host = "guide-acs.m.taobao.com"
    sid = "12e61dab2cb53f14a332e98f82b4315d"
    uid = "2990638377"
    d = gw_api(api=api, version=version, data=data,
               host=host, sid=sid, uid=uid, method="POST")
    print(d)
