#encoding: utf-8
from picamera.array import PiRGBArray
from picamera import PiCamera as picam
import numpy as np
import scipy as sp
# import cv2 #未安装
from  matplotlib import pyplot as plt
import multiprocessing as mp
import time

# resX = 
# resY = 


with picam() as camera:
  # camera = picam()
  # camera.reslution = (resX, rexY) #定义分辨率
  # try:
    # for i in range(500, 1000, 20):
      # for j in range(i - 400, i, 20):
        # camera.resolution = (i, j)
        # camera.start_preview()
        # time.sleep(1)

        # camera.capture('foo'+str(camera.resolution[0])+'x'+str(camera.resolution[1])+'.jpg')
  # except Exception:
    # pass
  camera.resolution = (1920, 1220)
  # camera.start_preview()
  time.sleep(1)
  camera.capture('foo'+str(camera.resolution[0])+'x'+str(camera.resolution[1])+'.jpg')
