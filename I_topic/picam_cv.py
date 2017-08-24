#encoding: utf-8
from picamera.array import PiRGBArray as pica
from picamera import PiCamera as picam
import numpy as np
import scipy as sp
import cv2
import time
import RPi.GPIO as gpio

resX = 800
resY = 608
#############
#
#    GPIO
#
#############
sumX = 0
sumY = 0
loop_i = 2
loop_num = loop_i
def main():
  # gpio.remove_event_detect(collect_key)
  with picam() as camera:
    camera.resolution = (resX, resY)
    camera.framerate = 24
    camera._set_iso(20)
    time.sleep(0)
    image = np.empty((resY * resX * 3,), dtype=np.uint8)
    camera.capture(image, 'bgr')
    img = image.reshape((resY, resX, 3))
    
    imgGray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  #灰度化
    ret, thresh = cv2.threshold(imgGray, 238 , 255, cv2.THRESH_BINARY) #二值化
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #get轮廓
    # print contours
    contours = [a for a in contours if len(a)>20]
    # cv2.drawContours(img, contours, -1, (0, 255, 0), 1) #绘制轮廓
    if len(contours) != 0:
      try:
        ledPoints = [[sum(x for x in [i[0][0] for i in j])/len([i[0][0] for i in j]), sum(x for x in [i[0][1] for i in j])/len([i[0][1] for i in j])] for j in contours]
        # print ledPoints
        # centerPoint = [sum(x[0])/len(x)), sum(x[1]/len(x)) for x in ledPoints]
        allLedx = [x[0] for x in ledPoints]  # LED points X[led0X, led1X, led2X]
        allLedy = [x[1] for x in ledPoints]  # LED points Y[led0Y, led1Y, led2Y]
        # print "get all x,y"
        centerPoint = [sum(allLedx)/len(allLedx), sum(allLedy)/len(allLedy)]  #中心点 [CenterPointX, CenterPointY]
        # print "found cp"
        # cv2.circle(img, (centerPoint[0], centerPoint[1]), 0, (0, 0, 255), 8)  #画出中心点

      # for a in ledPoints:
          # cv2.circle(img, (a[0], a[1]), 0, (255, 0, 0), 8)

      # print ledPoints
      # print (str(centerPoint[0])+" "+str(centerPoint[1]))
        return centerPoint
        # cv2.imshow("img", img)
        # cv2.imshow("thresh", thresh)
        # k = cv2.waitKey(0) & 0xFF
      except Exception:
        print Exception
    else:
      print "no led found"
      #cv2.imshow("img", img)
      # cv2.imshow("thresh", thresh)
      #k = cv2.waitKey(0) & 0xFF
    # print "error: 2"
    # gpio.add_event_detect(collect_key, gpio.FALLING, callback=key_callback, bouncetime=200)
# gpio.add_event_detect(collect_key, gpio.FALLING, callback=key_callback, bouncetime=200)
if __name__ == '__main__':
  try:
    while(1):
      try:
        while (loop_i>0):
          # print loop_i
          abc = main()
          sumX += abc[0]
          sumY += abc[1]
          loop_i -= 1
          cpx = sumX/loop_num
          cpy = sumY/loop_num
          cx = -49.34 + 0.1257*cpx + 0.0004289*cpy
          cy = -41.95 + 8.008*0.0000001*cpx + 0.1387*cpy
          if cx<20 and cx>-20 and cy<20 and cy>-20:
            block = "A block"
          elif cx<-20 and cy>cx and cy<-cx:
            block = "E block"
          elif cx>20 and cy>-cx and cy<cx:
            block = "C block"
          elif cy>20 and cx>-cy and cx<cy:
            block = "B block"
          elif cy<-20 and cx>cy and cx<-cy:
            block = "D block"
          else:
            block = "line"
        print ("Current position is (%0.2f, %0.2f)! is in %s" %(cx, cy, block))
        #time.sleep(1)
        loop_i = 2
        sumX = 0
        sumY = 0
      except Exception:
        pass
  except Exception:
    print Exception
    print "error: 3"
    pass

    # cv2.imshow("img", img)
    # cv2.imshow("thresh", thresh)
    # k = cv2.waitKey(0) & 0xFF

# print img.shape
# print img.size
# print img.dtype

# plt.imshow(img, cmap='gray', interpolation='bicubic')
# cv2.putText() #图片上加文字
# cv2.imshow() #显示图片
