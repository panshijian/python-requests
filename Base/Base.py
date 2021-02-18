import json
import os
from string import Template
import allure
import requests
import yaml

@allure.feature("")
class BaseApi:
    params = {}
    headers = {}
    data = {}
    file = {}
    env = yaml.safe_load(open("../data/mico_host.yml"))


    # todo:json读取
    @classmethod
    def json_load(cls,path) -> list:
        with open(path, 'r') as f:
            data = json.loads(f.read())
            print(data)
            return data

    @classmethod
    def yanl_load(cls,path) -> list:
        with open(path) as f:
            data = yaml.safe_load(f)
            return data
    # 发送请求封装
    def send(self, data:dict):
        # 不同環境地址切換
        data["url"] = str(data["url"]).replace("host",self.env["mico_host"][self.env["default"]])
        raw_data = json.dumps(data)
        # yml数据替换
        for key, value in self.params.items():
            raw_data = raw_data.replace("${" + key + "}", value)

        for key,value in self.headers.items():
            raw_data = raw_data.replace("${" + key + "}", value)

        data = json.loads(raw_data)
        print(data)
        # 上传本地图片
        files = {}
        for key, value in self.file.items():
            files[key] = (os.path.basename(value), open(value, "rb"), 'image/jpeg')
            data['files'] = files
        result=requests.request(**data)
        print(result.request.body)
        return result.json()
    # 写入数据封装
    def writefile(self, filepath, line):
        f = open(filepath, 'a+')
        line = '%s\n' % (line,)
        f.write(line)
        f.close()
        return f








