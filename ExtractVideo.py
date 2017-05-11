# -*- coding: utf-8 -*-

import os
import cv2
from datetime import *

filePath = ''
imagePath = ''

def createImgDir():
    tempPath = filePath
    lastIndex = tempPath.rfind(".")
    tempPath = tempPath[:lastIndex]
    tempPath = tempPath +'images_'+datetime.now().strftime("%Y%m%d%H%M%S%f")
    os.mkdir(tempPath)
    return tempPath

def getImgFileName(num):
    while len(num) < 6:
       num = "0"+num
    now = datetime.now()
    imgFileName = imagePath + "\\" + now.strftime("%Y%m%d%H%M%S%f")+'.jpg'
    return imgFileName


def extract():
    # if not os.path.exists(filePath):
    #     print  "not file named \"{0}\"".format(filePath)
    #     exit(0)
    # if not os.path.exists(imagePath):
    #     os.mkdir(imagePath)


    vidcap = cv2.VideoCapture(filePath.encode('utf-8'))
    success,image = vidcap.read()
    if not success:
        print('读取视频内容失败')
        return False
    #cv2.imwrite("frame.jpg", image)

    count = 0
    framerate = vidcap.get(5)
    print("framerate:", framerate)
    framecount = vidcap.get(7)
    print("framecount:", framecount)
    vidcap.set(5,1)
    newframerate = vidcap.get(5)
    print("newframerate:", newframerate)

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


if __name__ == '__main__':
    filePath = unicode(raw_input("请输入视频文件路径："),'utf-8')
    while(True):
        if not os.path.isfile(filePath):
            filePath = raw_input("“{0}”不是有效的文件路径，请重新输入：".format(filePath))
        else:
            break
    imagePath = raw_input("请输入图片保存路径，不输入将会自动生成：")
    while(True):
        if len(imagePath) == 0 :
            imagePath = createImgDir()
            break
        elif not os.path.isdir(imagePath):
            imagePath = raw_input("“{0}”不是有效的路径，请重新输入：".format(imagePath))
        else:
            break

    print("视频文件“{0}”将被分解为图片，源文件不会更改...\r".format(filePath.encode('utf-8')))
    print("图片保存路径：{0}".format(imagePath.encode('utf-8')))
    success = extract()
    if success:
        isOpen = raw_input("分解完成，是否打开图片文件夹？(是：Y/y，否：N/n)")
        if isOpen == 'Y' or isOpen == 'y':
            os.startfile(imagePath)