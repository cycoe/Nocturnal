import os
from PIL import Image


def img2Vector(imgPath):

    fullVector = []
    vectorList = []
    img = Image.open(imgPath)
    img = img.convert('RGBA')
    pixdata = img.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            if pixdata[x, y] == (0, 0, 153, 255):
                fullVector.append(1)
            else:
                fullVector.append(0)
    for i in range(4):
        vectorList.append(fullVector[135+324*i:135+324*(i+1)])
    return vectorList
