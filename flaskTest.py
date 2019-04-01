from flask import Flask,request
from json import JSONDecoder
import requests
import cv2
import numpy as np
from socket import *
from PIL import Image
import os
import glob
from PIL import Image
import getHand
import matplotlib.pyplot as plt
data=''
faceIds = []
counter=1
def inImage():
    face_cascade = cv2.CascadeClassifier('xml/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    count = 0
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            count += 1
            cv2.imwrite("Face/face" + str(count) + '.jpg', gray[y:y + h, x:x + w])
        cv2.imshow('img', img)
        if count > 10:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

    # 提取图片

    w_size = []
    for i in range(1, 11):
        fn = "Face/face" + str(i) + ".jpg"
        # print 'load %s as ...' % fn
        img = cv2.imread(fn)
        sp = img.shape
        # print sp
        sz1 = sp[0]  # height(rows) of image
        sz2 = sp[1]  # width(colums) of image
        sz3 = sp[2]  # the pixels value is made up of three primary colors
        # print 'width: %d \nheight: %d \nnumber: %d' % (sz1, sz2, sz3)
        w_size.append(sz2)
    a = w_size
    b = max(w_size)
    c = a.index(b)
    c += 1
    filename = "Face/face" + str(c) + '.jpg'
    global counter
    filename_w = "getImage/face" + str(counter) + '.jpg'
    img = Image.open(filename)
    img.save(filename_w)
    faceIds.append(filename_w)
    counter+=1

def camera():
    face_cascade = cv2.CascadeClassifier('xml/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    count=0
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            count +=1
            cv2.imwrite("Face/face"+str(count)+'.jpg',gray[y:y+h,x:x+w])
        cv2.imshow('img', img)
        if count>10:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def client(data):
    HOST = '192.168.43.211'
    PORT = 21567
    BUFSIZ = 1024
    ADDR = (HOST, PORT)
    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    tcpCliSock.connect(ADDR)
    tcpCliSock.send(bytes(data,'utf-8'))
    tcpCliSock.close()

def face():
    compare_url = "https://api-cn.faceplusplus.com/facepp/v3/compare"
    key = "SASuuvcBxQmaweSsUH06xeV3ouCdjrLU"
    secret = "JP6XgFiqH7zMZSh0nUh0LngyYg8Fe0UQ"
    data = {"api_key": key, "api_secret": secret}


    i = 1
    jResult=False
    result=False
    # #循环体
    for j in range(len(faceIds)):
        while True:
            print("Face/face"+str(i)+".jpg")
            files = {"image_file1": open(faceIds[j], "rb"), "image_file2": open("Face/face"+str(i)+".jpg", "rb")}
            # file_2 = {"image_file2": open(faceId2, "rb")}
            response = requests.post(compare_url, data=data, files=files)
            req_con = response.content.decode('utf-8')
            req_dict = JSONDecoder().decode(req_con)
            # print req_dict
            # print("req_dict is:", req_dict)
            try:
                confindence = req_dict['confidence']
            except:
                confindence=0
                pass

            i = i + 1
            if confindence >= 70:
                print("true:", i)
                print("face"+str(j+1)+",Success")
                jresult=True
                result=True
                break
            if i>11:
                break
        if jResult==True:
            break
    return result
app=Flask(__name__)
@app.route('/')
def index():
    return '''<h1 align="center">人脸识别测试</h1>
    <a style="text-decoration:NONE" href="http://127.0.0.1:5000/recognition">
    <div style="text-align:center;background-color:#dcdcdc;width:180;height:60px;font-size:40px">开始识别<div>
    </a>
    <br>
    <a style="text-decoration:NONE" href="http://127.0.0.1:5000/in">
    <div style="text-align:center;background-color:#dcdcdc;width:100;height:60px;font-size:40px">录入<div>
    </a>
    
    '''
@app.route('/recognition')
def Result():
    # cmd=request.args.get('result','Flask')
    camera()
    result=face()
    page=''
    if result==True:
        data = 'OK'
        page='''<center>
                <br>
                <br>
                <br>
                <h1>验证成功!</h1>
                <a style="text-decoration:NONE" href="http://127.0.0.1:5000/hands">
    <div style="text-align:center;background-color:#dcdcdc;width:180;height:60px;font-size:40px">开始手势识别<div>
    </a>
                </center>'''
    else:
        data='NO'
        page = '<h1>验证失败!</h1>'
    print(data)
    client(data)
    return page


@app.route('/hands')
def hand():
    getHand.show()
    return '<center><br><br><br><h1>手势识别结束</h1></center>'


@app.route('/in')
def input():
    inImage()
    return '<h1>成功录入</h1>'

if __name__ == '__main__':
    app.run(debug=True)