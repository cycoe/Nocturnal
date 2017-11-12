import os
from PIL import Image


# def img2Vector(imgPath):
#
#     fullVector = []
#     vectorList = []
#     img = Image.open(imgPath)
#     img = img.convert('RGBA')
#     pixdata = img.load()
#     for x in range(img.size[0]):
#         for y in range(img.size[1]):
#             if pixdata[x, y] == (0, 0, 153, 255):
#                 fullVector.append(1)
#             else:
#                 fullVector.append(0)
#     for i in range(4):
#         vectorList.append(fullVector[135+324*i:135+324*(i+1)])
#     return vectorList


def get_max_key(numbers_):
    max_number = numbers_[0]
    for index in range(len(numbers_)):
        if numbers_[index] > max_number:
            max_number = numbers_[index]
    return numbers_.index(max_number)


def img2Vector(img_path):
    color_tolerant = 3 * 180
    size_tolerant = 5
    most_color_ = []
    vector_ = []
    vectors_ = []
    img = Image.open(img_path)
    img = img.convert('RGB')
    img_width = img.size[0] - 2
    img_height = img.size[1] - 4
    pixdata = img.load()

    # get the most colors from picture
    for index in range(4):
        color_stack_ = []
        counter_ = []
        for x in range(2 + int(img_width / 4) * index, 2 + int(img_width / 4) * (index + 1)):
            for y in range(1, img_height):
                if pixdata[x, y][0] + pixdata[x, y][1] + pixdata[x, y][2] < color_tolerant:
                    if pixdata[x, y] in color_stack_:
                        counter_[color_stack_.index(pixdata[x, y])] += 1
                    else:
                        color_stack_.append(pixdata[x, y])
                        counter_.append(1)
        most_color_.append(color_stack_[get_max_key(counter_)])

