import os
import random
import cv2
import time
import LearnGesture
import setPhoto
import sys
# #
# gesture_englist = [ 'ok', 'hand_open',
#                    'thumb_up', 'thumb_down', 'fist']
# gesture_chinese = [
#                    "好的呢，OK",
#                    "手张开",
#                    "点赞",
#                    "差评",
#                    "握拳",
#                   ]

def sel_file(file_path):
    count_i=[0,1,2,3,4]
    for i in count_i:
        # 此处应该有手势识别
        files = {"image_file": open(file_path, 'rb')}
        gesture = LearnGesture.Gesture()
        # 获取到手势文本
        ge_text = gesture.get_text(i)
        # 获取手势信息
        gesture_dict, gesture_rectangle_dict = gesture.get_info(files)
        # 获取手势的概率
        ge_pro = gesture.get_pro(gesture_dict, i)
        if ge_pro>70.0:
            print("您的手势是：", ge_text)
            print("相似度达到：", ge_pro)
            break
    print("为找到匹配信息")

#图片录入

def show():
    for i in range(0,9):
        file_path = setPhoto.make_photo()
        print(file_path)
        sel_file(file_path)
        if  0xFF == ord('q'):
            break
    
if __name__ == '__main__':
    show()







