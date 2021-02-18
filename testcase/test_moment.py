import json
import random
from time import sleep

import jsonpath
import xdist

from Base.Base import BaseApi
from micoapi.moment import MomentApi
import pytest
import allure

def load_data(key):
    data = BaseApi.yanl_load("../data/moment.yml")

    return data[key]



@allure.feature("动态相关接口")
class TestMoment:

    @classmethod
    def setup_class(cls):
        cls.moment = MomentApi()
        cls.base = BaseApi()
    @allure.step(title="内置读取json文件调用方法")
    def _test_load_json(self):
        allure.attach("json文件路径")
        data = BaseApi.json_load("../result/post_moments.json")
        r = json.dumps(data, indent=2)
        # print(json.loads(r)[0]["circle"]["cid"])
        r = json.loads(r)
        return r
    @allure.step(title="获取热门动态")
    @pytest.mark.parametrize("dict1",load_data("get_hot_moment"))
    def test_get_hot_moment(self,dict1):
        allure.attach("yml文件数据，{}".format(dict1))
        uid = dict1["uid"]
        allure.attach("用户uid，{}".format(uid))
        self.moment.get_hot_moments(uid=str(uid))

    @allure.step(title="获取已关注动态")
    @pytest.mark.parametrize("dict1",load_data("get_follow_moment"))
    def test_get_follow_moment(self,dict1):
        allure.attach("yml文件数据，{}".format(dict1))
        uid = dict1["uid"]
        allure.attach("用户uid，{}".format(uid))
        result = self.moment.get_follow_moments(uid=str(uid))
        print(len(result["circles"]))
        assert len(result["circles"]) > 0

    @allure.step(title="获取附近动态")
    @pytest.mark.parametrize("dict1", load_data("get_nearby_moment"))
    def test_get_nearby_moment(self,dict1):
        allure.attach("yml文件数据，{}".format(dict1))
        uid = dict1["uid"]
        allure.attach("用户uid，{}".format(uid))
        result = self.moment.get_nearby_moments(uid=str(uid))
        print(len(result["circles"]))
        assert len(result["circles"]) > 0
    @allure.step(title="内置发布动态调用方法")
    def _test_post_moment(self,dict1):
        uid, text = dict1["uid"], dict1["text"]
        result = self.moment.post_moments(uid=str(uid),text=str(text))
        return  result

    @allure.step(title="发布动态")
    # @pytest.mark.parametrize(("uid,text"), test_load_data("post_moment"))
    @pytest.mark.parametrize("dict1", load_data("post_moment"))
    def test_post_moment(self,dict1):
        # print('-------',dict1)
        allure.attach("yml文件数据，{}".format(dict1))
        result = self._test_post_moment(dict1)
        assert result["circle"]["cid"] is not None


    @allure.step(title="对已发布的动态点赞")
    # @pytest.mark.parametrize(("from_uid,from_text,to_uid"),test_load_data("like_moment"))
    @pytest.mark.parametrize("dict1", load_data("like_moment"))
    def test_like_moment(self,dict1):
        allure.attach("yml文件数据，{}".format(dict1))
        to_uid = dict1["to_uid"]
        allure.attach("来自点赞用户uid，{}".format(to_uid))
        post_moment = self._test_post_moment(load_data("post_moment")[1])
        allure.attach("用户动态，{}".format(post_moment))
        result = self.moment.like_moments(uid=to_uid,cid=str(post_moment["circle"]["cid"]),ownerId=str(post_moment["circle"]["uid"]))
        assert result["result"] == True
    @allure.step(title="对已发布的动态多条点赞")
    @pytest.mark.parametrize("dict1", load_data("like_moment"))
    def test_like_json(self,dict1):
        allure.attach("yml文件数据，{}".format(dict1))
        to_uid = dict1["to_uid"]
        allure.attach("来自点赞用户uid，{}".format(to_uid))
        cid = self._test_load_json()[1]["circle"]["cid"]
        allure.attach("提取发动态用户的动态ID，{}".format(cid))
        uid = self._test_load_json()[1]["user"]["uid"]
        allure.attach("提取发动态用户uid，{}".format(uid))
        result = self.moment.like_moments(uid=to_uid,cid=str(cid),ownerId=str(uid))
        assert result["result"] == True
        sleep(0.5)
    @allure.step(title="对已发布的动态评论")
    # @pytest.mark.parametrize(("from_uid,from_text,to_uid,content,ownerId,targetUid"),test_load_data("comment_moment"))
    @pytest.mark.parametrize("dict1",load_data("comment_moment_1"))
    def test_comment_moment(self,dict1):
        allure.attach("yml文件数据，{}".format(dict1))
        to_uid=dict1["to_uid"]
        content=dict1["content"]
        ownerId=dict1["ownerId"]
        targetUid=dict1["targetUid"]
        post_moment = self._test_post_moment(load_data("post_moment")[1])
        allure.attach("选择的用户，{}".format(post_moment))
        result = self.moment.comment_moments(uid=to_uid,cid=str(post_moment["circle"]["cid"]),content=str(content),ownerId=ownerId,targetUid=targetUid)
        assert post_moment["circle"]["cid"] == result["cid"]
    @allure.step("多条动态评论")
    @pytest.mark.parametrize("dict1",load_data("comments_moment"))
    def test_comments_moment(self,dict1):
        allure.attach("yml文件数据，{}".format(dict1))
        to_uid=dict1["to_uid"]
        content=dict1["content"]
        # 提取已发布动态的cid
        cid = self._test_load_json()[0]["circle"]["cid"]
        allure.attach("提取发动态用户的动态ID，{}".format(cid))
        # 提取发布者uid
        uid = self._test_load_json()[0]["user"]["uid"]
        allure.attach("提取发动态用户uid，{}".format(uid))
        result = self.moment.comment_moments(uid=to_uid,cid=str(cid),content=str(content),ownerId=str(uid),targetUid=str(uid))
        assert content == result["content"]
        sleep(0.3)





