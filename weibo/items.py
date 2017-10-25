# -*- coding: utf-8 -*-
"""
    @author: Jiale Xu
    @date: 2017/10/23
    @desc: Items of weibo scraping
"""
from exception import ItemAttrError, ItemEmptyError


class WeiboUserItem:
    _fields = ["user_id", "user_name", "sex", "address", "birthday", "synopsis",
              "weibo_number", "follow_number", "fans_number"]

    def __init__(self):
        self._value = {}
        self._value["user_id"] = None
        self._value["user_name"] = None
        self._value["sex"] = None
        self._value["address"] = None
        self._value["birthday"] = None
        self._value["synopsis"] = None
        self._value["weibo_number"] = 0
        self._value["follow_number"] = 0
        self.fans_number = 0

    def __getitem__(self, key):
        if key not in self._fields:
            raise ItemAttrError(key)
        return self._value[key]

    def __setitem__(self, key, value):
        if key not in self._fields:
            raise ItemAttrError(key)
        else:
            self._value[key] = value

    def __str__(self):
        if "user_id" not in self._value.keys():
            raise ItemEmptyError()
        string = "User ID: " + str(self._value["user_id"]) + "\n"
        if "user_name" in self._value.keys():
            string += "User Name: " + str(self._value["user_name"]) + "\n"
        if "sex" in self._value.keys():
            string += "Sex: " + str(self._value["sex"]) + "\n"
        if "address" in self._value.keys():
            string += "Address: " + str(self._value["address"]) + "\n"
        if "birthday" in self._value.keys():
            string += "Birthday: " + str(self._value["birthday"]) + "\n"
        if "synopsis" in self._value.keys():
            string += "Synopsis: " + str(self._value["synopsis"]) + "\n"
        return string

    def __hash__(self):
        if "user_id" not in self._value.keys():
            raise ItemEmptyError()
        return hash(self._value["user_id"])


class WeiboItem:
    _fields = ["from", "time", "content", "images"]

    def __init__(self):
        self._value = {}
        self._value["from"] = None
        self._value["time"] = None
        self._value["content"] = None
        self._value["images"] = []

    def __getitem__(self, key):
        if key not in self._fields:
            raise ItemAttrError(key)
        return self._value[key]

    def __setitem__(self, key, value):
        if key not in self._fields:
            raise ItemAttrError(key)
        else:
            self._value[key] = value

    def __str__(self):
        if "content" not in self._value.keys():
            raise ItemEmptyError()
        string = "Content: " + str(self._value["content"]) + "\n"
        if "from" in self._value.keys():
            string += "From: " + str(self._value["from"]) + "\n"
        if "time" in self._value.keys():
            string += "Time: " + str(self._value["time"]) + "\n"
        return string

    def __hash__(self):
        if "content" not in self._value.keys():
            raise ItemEmptyError()
        return hash(self._value["content"])
