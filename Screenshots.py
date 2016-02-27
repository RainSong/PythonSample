#encoding:utf-8

from PIL import Image,ImageGrab

def shots():
    img = ImageGrab.grab()
    img.save('d:\\123.jpg')


if __name__ == '__main__':
    print('begin')
    shots()
    print('ok')