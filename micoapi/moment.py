import json
import time
import yaml

from Base.Base import BaseApi
from Base.upload_data import UplaodData


class MomentApi(BaseApi):

    def __init__(self):
        self.files = UplaodData().uploadimage()



    def with_open(self):
        with open("../data/mico_data.yml", encoding="utf-8") as f:
            data = yaml.load(f)
            return data

    def get_hot_moments(self,uid):
        self.params["uid"] = uid
        r = self.send(self.with_open()["get_hot_moments"])
        print(json.dumps(r, indent=2))
        return r
    def get_follow_moments(self,uid):
        self.params["uid"] = uid
        r = self.send(self.with_open()["get_follow_moments"])
        print(json.dumps(r, indent=2))
        return r
    def get_nearby_moments(self,uid):
        self.params["uid"] = uid
        r = self.send(self.with_open()["get_nearby_moments"])
        print(json.dumps(r, indent=2))
        return r
    def post_moments(self,uid,text):
        # self.file["key"] = "upload0"
        for img  in range(3):
          image = self.files[img]
          print(image)
          self.file["upload" + str(img)] = image
        self.params["uid"] = uid
        self.params["text"] = text

        r = self.send(self.with_open()["post_moments"])

        print(json.dumps(r, indent=2))
        now_time = time.time()
        self.writefile("../result/"+str(int(now_time))+"_"+"post_moments1.json",json.dumps(r,indent=2))
        return r
    def like_moments(self,uid,cid,ownerId):
        self.params["uid"] = uid
        self.params["cid"] = cid
        self.params["ownerId"] = ownerId
        r = self.send(self.with_open()["like_moments"])
        print(json.dumps(r, indent=2))
        return r
    def comment_moments(self,uid,cid,content,ownerId,targetUid):
        self.params["uid"] = uid
        self.params["cid"] = cid
        self.params["content"] = content
        self.params["ownerId"] = ownerId
        self.params["targetUid"] = targetUid
        r = self.send(self.with_open()["comment_moments"])
        print(json.dumps(r, indent=2))
        return r

