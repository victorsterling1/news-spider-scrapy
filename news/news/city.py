#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os

province_list = []
province_city = {}

city_list = []
city_province = {}

select = "请选择".decode("utf-8")
other = "其他".decode("utf-8")

path = os.path.abspath(os.path.join(os.path.curdir, "city.json"))

with open(path) as f:
    js = json.load(f)
    for p in list(js):
        p_name = p["name"]
        if p_name not in [select, other]:
            province_list.append(p_name)
            province_city[p_name] = []
            for c in list(p["sub"]):
                c_name = c["name"]
                if c_name not in [select, other]:
                    province_city[p_name].append(c_name)
                    city_list.append(c_name)
                    city_province[c_name] = p_name

def get_province_city(text):
    province = None
    city = None
    for p in province_list:
        if text.find(p) != -1:
            province = p
    if province:
        for c in province_city[province]:
            if text.find(c) != -1:
                city = c
    else:
        for c in city_list:
            if text.find(c) != -1:
                city = c
                province = city_province[city]
    return (province, city)

if __name__ == "__main__":
    print get_province_city("天津实施大气污染防治网格化管理 防污治污无死角".decode("utf-8"))
