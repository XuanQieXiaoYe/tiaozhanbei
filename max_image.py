import numpy as np
import cv2
from PIL import Image
import os
import glob
from PIL import Image
import matplotlib.pyplot as plt
#摄像头调用

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

#提取图片

w_size=[]
for i in range(1,11):
    fn="Face/face"+str(i)+".jpg"
    #print 'load %s as ...' % fn
    img = cv2.imread(fn)
    sp = img.shape
    #print sp
    sz1 = sp[0]  # height(rows) of image
    sz2 = sp[1]  # width(colums) of image
    sz3 = sp[2]  # the pixels value is made up of three primary colors
    #print 'width: %d \nheight: %d \nnumber: %d' % (sz1, sz2, sz3)
    w_size.append(sz2)
a=w_size
b=max(w_size)
c=a.index(b)
c +=1

filename="Face/face"+str(c)+'.jpg'

filename_w="getImage/face"+str(c)+'.jpg'
img=Image.open(filename)
img.save(filename_w)