# -*- coding: utf-8 -*-

import os
import cv2
from datetime import *

filePath = r"""D:\TDDownload\20160120\dhmgddgpscbsxjypyeccmz\videos\dhmgddgpscbsxjypyeccmz_05.mp4"""
imagePath = r"""D:\TDDownload\20160120\dhmgddgpscbsxjypyeccmz\videos\dhmgddgpscbsxjypyeccmz_imgs_05\\"""
def getImgFileName(num):
    while len(num) < 6:
       num = "0"+num
    now = datetime.now()
    imgFileName = imagePath+ now.strftime("%Y%m%d%H%M%S%f")+'.jpg'
    return imgFileName



if not os.path.exists(filePath):
    print  "not file named \"{0}\"".format(filePath)
    exit(0)
if not os.path.exists(imagePath):
    os.mkdir(imagePath)


vidcap = cv2.VideoCapture(filePath)
success,image = vidcap.read()
print success
#cv2.imwrite("frame.jpg", image)

count = 0
framerate = vidcap.get(5)
print "framerate:", framerate
framecount = vidcap.get(7)
print "framecount:", framecount
vidcap.set(5,1)
newframerate = vidcap.get(5)
print "newframerate:", newframerate

while success:
  success,image = vidcap.read()
  #cv2.imwrite("frame%d.jpg" % count, image)

  getvalue = str(int(vidcap.get(0)))
  # print getvalue
  # if getvalue == 20000:
  imgFileName = getImgFileName(getvalue)
  cv2.imwrite(imgFileName,image)

  #if cv2.waitKey(10) == 27:
      #break
  count += 1

  print str(100 * count / framecount)+"%"

