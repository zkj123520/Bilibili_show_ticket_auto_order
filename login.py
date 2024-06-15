import requests
import qrcode
import os
import sys
import time
import json

qr_baseurl = 'https://passport.bilibili.com/x/passport-login/web/qrcode/generate'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.1.4.514 Safari/537.36 360se/19.19.81.0",
    "Referer": "https://passport.bilibili.com/",
    "Origin": "https://passport.bilibili.com/",
    "Pregma": "no-cache",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Accept-Encoding": "",
    "Connection": "keep-alive"
}

qr = qrcode.QRCode()
qr_data = requests.get(qr_baseurl,headers=headers).json()

qr_url = qr_data["data"]["url"]
qrcode_key = qr_data["data"]["qrcode_key"]

qr.add_data(qr_url)
qr.make()
qr.print_ascii()
print("请在180秒内扫描登录")

poll_url = "https://passport.bilibili.com/x/passport-login/web/qrcode/poll"
poll_params = {
    "qrcode_key": qrcode_key
}

if not os.path.exists('user_data.json'):
    open('user_data.json','w').write("{}").close()
cookies = {}
with open('user_data.json','r') as f:
    cookies = json.load(f)

for i in range(1,180):
    qr_check = requests.get(poll_url,headers=headers,params=poll_params)
    qr_ckjson = qr_check.json()
    if(qr_ckjson["data"]["code"]!=0):
        if(qr_ckjson["data"]["code"]==86038):
            print("二维码已失效。")
            os.system("pause")
            sys.exit(0)
    else:
        uid = qr_check.cookies["DedeUserID"]
        cookies[uid]={}
        for key in qr_check.cookies.iterkeys():
            cookies[uid][key] = qr_check.cookies[key]
        break
    time.sleep(1)

with open('user_data.json','w') as f:
    json.dump(cookies,f)

print("获取完毕.")
os.system("pause")