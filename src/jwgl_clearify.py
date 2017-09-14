#!/usr/bin/python

from PIL import Image


def clearify(image):
    pixdata = image.load()
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            if pixdata[x, y] == (0, 0, 153, 255):
                pixdata[x, y] = (0, 0, 0, 255)
            else:
                pixdata[x, y] = (255, 255, 255, 255)
    return pixdata
