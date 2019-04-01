'''
# -*- coding:utf-8 -*-
@author: TulLing
'''
import requests
from json import JSONDecoder

gesture_englist = [ 'ok', 'hand_open',
                   'thumb_up', 'thumb_down', 'fist']
gesture_chinese = [
                   "好的呢，OK",
                   "手张开",
                   "点赞",
                   "差评",
                   "握拳",
                  ]


# 将字典排序
def sort_dict(adict):
    return sorted(adict.items(), key=lambda item: item[1])


class Gesture(object):
    def __init__(self):
        self.http_url = 'https://api-cn.faceplusplus.com/humanbodypp/v1/gesture'
        self.key = 'SASuuvcBxQmaweSsUH06xeV3ouCdjrLU'
        self.secret = 'JP6XgFiqH7zMZSh0nUh0LngyYg8Fe0UQ'
        self.data = {"api_key": self.key, "api_secret": self.secret}

    # 获取手势信息
    def get_info(self, files):
        response = requests.post(self.http_url, data=self.data, files=files)
        req_con = response.content.decode('utf-8')
        req_dict = JSONDecoder().decode(req_con)
        #print(req_dict)
        if ('error_message' not in req_dict.keys()) and (len(req_dict['hands'])):
            # 获取
            hands_dict = req_dict['hands']
            # print(type(hands_dict))
            # 获取到手的矩形的字典
            gesture_rectangle_dict = hands_dict[0]['hand_rectangle']
            # 获取到手势的字典
            gesture_dict = hands_dict[0]['gesture']

            return gesture_dict, gesture_rectangle_dict
        else:
            return [], [];

    # 获取到手势文本信息
    def get_text(self, index):
        return gesture_chinese[index]

    # 获取到手势对应的概率
    def get_pro(self, gesture_dict, index):
        # print(gesture_dict)
        if (gesture_dict is None or gesture_dict == []):
            return 0
        return gesture_dict[gesture_englist[index]]

    # 获取到手势的位置
    def get_rectangle(self, gesture_rectangle_dict):
        if (gesture_rectangle_dict is None or gesture_rectangle_dict == []):
            return (0, 0, 0, 0)
        x = gesture_rectangle_dict['top']
        y = gesture_rectangle_dict['left']
        width = gesture_rectangle_dict['width']
        height = gesture_rectangle_dict['height']
        return (x, y, width, height)
