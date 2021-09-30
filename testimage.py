# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 22:52:51 2021

@author: ASUS
"""

import numpy as np
import cv2
import os
from tqdm import tqdm
from einops import rearrange, reduce, repeat
import matplotlib.pyplot as plt

imgpath = "C:/Users/ASUS/Documents/project/Digit-Recognizer-master/datasetAksara/0/ha_20.jpg"
img = cv2.imread(imgpath, cv2.IMREAD_COLOR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = cv2.resize(gray, (32,32), interpolation = cv2.INTER_AREA)

#print(img)

#cv2.imshow("img", img)

#cv2.waitKey(0)
 
#cv2.destroyAllWindows()

thresh, bw = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)

temp = bw == 0

swap = 255 * (bw==0).astype(int)
swap = swap.reshape((32,32,1))

imgplot = plt.imshow(swap)
print(swap.shape)

#cv2.imshow("img", swap)

#cv2.waitKey(0)
 
#cv2.destroyAllWindows()

aksarapath = "C:/Pictures/download.png"
aksara = cv2.imread(imgpath, cv2.IMREAD_COLOR)
aksara = cv2.resize(aksara, (64,64), interpolation = cv2.INTER_AREA)
