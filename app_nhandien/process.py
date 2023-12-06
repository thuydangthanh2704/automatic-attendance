#Thư viện cần thiết
import os
import imutils
import math
import numpy as np
import cv2 as cv
import tensorflow as tf
from tensorflow.python.platform import gfile
import cv2
import numpy as np
import time
import glob
import os
import matplotlib.pyplot as plt
import pytesseract

def Ketqua(path_img):
    #Đường dẫn của ảnh
    image = cv.imread(path_img)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()
    image = cv.imread(path_img)
    filename = path_img.split("/")[2].split(".")[0]
    if(str(os.path.isdir("static/process/" +  filename)) == "False"):
        os.mkdir("static/process/" +  filename)
    cv.imwrite(path_save_process+"/"+filename+"/"+"1.jpg", img)
    image = cv2.resize(image, None, fx=6, fy=6, interpolation=cv2.INTER_CUBIC)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image = cv2.threshold(image, 120, 255, cv2.THRESH_BINARY)[1]
    image = cv2.medianBlur(image, 7)
    plt.imshow(image, cmap = 'gray', vmin = 0, vmax = 255)
    plt.show()
    return result  
































