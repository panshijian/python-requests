import json
import allure
from Base.Base import BaseApi
from Base.upload_data import UplaodData
from micoapi.personal_info import PersonalInfo
import pytest
import random

def load_data(key):
    data = BaseApi.yanl_load("../data/user_info.yml")

    return data[key]
@allure.feature("mico个人信息相关")
class TestUserInfo:
    params1 = {}
    data = BaseApi.json_load("../data/test_data.json")


    @classmethod
    def setup_class(cls):
        cls.userinfo = PersonalInfo()
        cls.files = UplaodData().uploadimage()

    @allure.step(title="内置读取json文件调用方法")
    def _test_load_json(self):
        allure.attach("json文件路径")
        data = BaseApi.json_load("../result/fid.json")
        r = json.dumps(data, indent=2)
        r = json.loads(r)
        return r
    @allure.step(title="获取micoUid")
    @pytest.mark.parametrize("dict1",load_data("get_uid"))
    def test_get_uid(self,dict1):
        allure.attach("yml文件数据，{}".format(dict1))
        userId = dict1["userId"]
        result = self.userinfo.get_uid(userId=userId)

        assert result["user"]["userId"] == int(userId)

    @allure.step(title="获取profile信息")
    @pytest.mark.parametrize("dict1",load_data("get_pfofile"))
    def test_get_profile(self,dict1):
        allure.attach("yml文件数据，{}".format(dict1))
        uid = dict1["uid"]
        result = self.userinfo.get_pfofile(targetUid=uid)
        assert result["user_basic"]["uid"] == int(uid)

    @allure.step(title="更改用户昵称，年龄")
    @pytest.mark.parametrize("dict1",load_data("updata_profile_info"))
    def test_updata_info(self,dict1):
        allure.attach("yml文件数据，{}".format(dict1))
        uid, displayName, age = dict1["uid"],dict1["displayName"],dict1["age"]
        result = self.userinfo.updata_profile_info(uid=uid,displayName=displayName,age=age)
        assert result["displayName"] == dict1["displayName"]

    @allure.step(title="获取fid")
    @pytest.mark.parametrize("dict1", load_data("get_img_rb"))
    def test_upload_image(self,dict1):
        allure.attach("yml文件数据，{}".format(dict1))
        uid = dict1["uid"]
        result = self.userinfo.get_img_rb(uid=uid)
        assert result["result"] == "ok"

    @allure.step(title="更换头像")
    @pytest.mark.parametrize("dict1", load_data("change_avatar"))
    def test_change_avatar(self,dict1):
        allure.attach("yml文件数据，{}".format(dict1))
        uid = dict1["uid"]
        i = random.randint(0,len(self._test_load_json())-1)
        allure.attach("获取随机fid，{}".format(i))
        fid = self._test_load_json()[i]["fid"]
        allure.attach("生成的fid，{}".format(fid))
        result = self.userinfo.change_avatar(uid=uid,avatar=str(fid))
        assert result["result"] == True












