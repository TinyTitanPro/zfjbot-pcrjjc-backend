import requests
from Luna.PCRPack import *
import ast
import hashlib
import base64
import random
import json
import time
from flask import Flask,jsonify,request

class PCRClient:
    def __init__(self, viewer_id):
        self.viewer_id = viewer_id
        self.request_id = ""
        self.session_id = ""
        self.urlroot = "https://le1-prod-all-gs-gzlj.bilibiligame.net/"
        self.default_headers={
            "Accept-Encoding": "gzip",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; VTR-AL00 Build/V417IR)",
            "X-Unity-Version": "2017.4.37c2",
            "APP-VER": "2.4.9",
            "BATTLE-LOGIC-VERSION": "3",
            "BUNDLE_VER" : "",
            "CHANNEL-ID": "1",
            "DEVICE": "2",
            "DEVICE-ID": "b459355e617d72e85d4558e66046ef6f",
            "DEVICE-NAME": "Xiaomi MI 6",
            "EXCEL-VER": "1.0.0",
            "GRAPHICS-DEVICE-NAME": "MuMu GL (NVIDIA GeForce RTX 2070 Direct3D11 vs_5_0 ps_5_0)",
            "IP-ADDRESS": "10.0.2.15",
            "KEYCHAIN": "",
            "LOCALE": "CN",
            "PLATFORM": "2",
            "PLATFORM-ID": "2", 
            "PLATFORM-OS-VERSION": "Android OS 6.0.1 / API-23 (V417IR/eng.root.20200623.095831)",
            "REGION-CODE": "",
            "RES-KEY": "ab00a0a6dd915a052a2ef7fd649083e5",
            "RES-VER": "10002200",
            "SHORT-UDID": "0",
            "Connection": "Keep-Alive"}
        self.conn = requests.session()
    
    
    def Callapi(self, apiurl, request, crypted = True):
        key = CreateKey()
        if crypted:
            request['viewer_id'] = encrypt(str(self.viewer_id), key).decode()
        else:
            request['viewer_id'] = str(self.viewer_id)
        req = Pack(request, key)
        flag = self.request_id != None and self.request_id != ''
        flag2 = self.session_id != None and self.session_id != ''
        headers = self.default_headers
        if flag: headers["REQUEST-ID"] = self.request_id
        if flag2: headers["SID"] = self.session_id
        
        resp = self.conn.post(url= self.urlroot + apiurl,
                        headers = headers, data = req)
        null = None
        if crypted:
            ret = decrypt(resp.content)
        else: ret = eval(resp.content.decode())
        ret_header = ret["data_headers"]
        if "sid" in ret_header:
            if ret_header["sid"] != None and ret_header["sid"] != "":
                self.session_id = hashlib.md5((ret_header["sid"] + "c!SID!n").encode()).hexdigest()
        if "request_id" in ret_header:
            if ret_header["request_id"] != None and ret_header["request_id"] != "" and ret_header["request_id"] != self.request_id:
                self.request_id = ret_header["request_id"]
        if "viewer_id" in ret_header:
            if ret_header["viewer_id"] != None and ret_header["viewer_id"] != 0 and ret_header["viewer_id"] != self.viewer_id:
                self.viewer_id = int(ret_header["viewer_id"])
        return ret["data"]
    
    
    def login(self, uid, access_key):
        self.manifest = self.Callapi('source_ini/get_maintenance_status', {}, False)
        ver = self.manifest["required_manifest_ver"]
        print(str(self.manifest))
        self.default_headers["MANIFEST-VER"] = ver
        print(str(self.Callapi('tool/sdk_login', {"uid": uid, 
                                                "access_key" : access_key, 
                                                "platform" : self.default_headers["PLATFORM-ID"], 
                                                "channel_id" : self.default_headers["CHANNEL-ID"]
                                                }
                                )))
        print(str(self.Callapi('check/game_start', {"app_type": 0, "campaign_data" : "", "campaign_user": random.randint(1, 1000000)}) ))
        print(str(self.Callapi("check/check_agreement", {}) ))
        self.Callapi("load/index", {"carrier": "Xiaomi"})
        time.sleep(1)
        self.Home = self.Callapi("home/index", {'message_id': 1, 'tips_id_list': [], 'is_first': 1, 'gold_history': 0})


def arena_info(target_viewer_id):
    viewer_id=xxxxxxxxxxxxx
    uid="xxxxxxxxxxxxxx"
    access_key="xxxxxxxxxxxxxxxxxxxxxxx"

    Client = PCRClient(viewer_id)
    Client.login(uid, access_key)
    return Client.Callapi("profile/get_profile",{'target_viewer_id': int(target_viewer_id), 'viewer_id': viewer_id})

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
@app.route('/api/pcrjjc/get_profile')
def index():
    if request.args.get('target_viewer_id'):
        target_viewer_id = request.args['target_viewer_id']
        data=arena_info(target_viewer_id)
        if data.get('user_info'):
            res={"status": "done","data":data}
        else:
            res={"status": "error","data":data}
        return jsonify(res)
    else:
        return jsonify({"msg":"Error"})
app.run(
      host='0.0.0.0',
      port= 9025,
      debug=False
    )
