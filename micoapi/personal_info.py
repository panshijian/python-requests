import os


import yaml
import json

import time
import datetime
import json

from Base.Base import BaseApi
from Base.upload_data import UplaodData


def with_open():
    with open("../data/test_data.json", encoding="utf-8") as f:
        data = yaml.load(f)
        return data




class PersonalInfo(BaseApi):


    def __init__(self):
        self.files = UplaodData().uploadimage()

    def with_open(self):
        with open("../data/mico_data.yml", encoding="utf-8") as f:
            data = yaml.load(f)
            return data




    def get_uid(self,userId):
        self.params["userId"] = userId

        r = self.send(self.with_open()["getuid"])

        print(json.dumps(r,indent=2))

        return r

    def get_pfofile(self,targetUid):
        self.params["targetUid"] = targetUid
        r = self.send(self.with_open()["profile"])
        print(self.params)
        print(json.dumps(r, indent=2))
        return r

    def updata_profile_info(self,uid, displayName, age):
        self.params["uid"] = uid
        self.params["displayName"] = displayName
        self.params["age"] = age


        r = self.send(self.with_open()["updatainfo"])

        print(json.dumps(r, indent=2))
        return r



    def get_img_rb(self,uid):
        num = len(self.files)

        for img  in range(1):
          image = self.files[img]
          self.file["upload"] = image
          self.params["uid"] = uid

          r = self.send(self.with_open()["uploadimg"])
          print(json.dumps(r, indent=2))
          now_time = time.time()
          self.writefile("../result/"+ str(int(now_time)) +"_"+"fid.json", json.dumps(r, indent=2))
          return r

    def change_avatar(self,uid,avatar):
        self.params["avatar"] = avatar
        self.params["uid"] = uid
        r = self.send(self.with_open()["changeavatar"])
        print(json.dumps(r, indent=2))
        return r



