import os
from PIL import Image
from listUtils import is_same_neighbor


def get_max_key(numbers_):
    max_number = numbers_[0]
    for index in range(len(numbers_)):
        if numbers_[index] > max_number:
            max_number = numbers_[index]
    return numbers_.index(max_number)


def is_near_color(tup1, tup2, near_tolerant):
    for index in range(3):
        if max(tup1[index], tup2[index]) - min(tup1[index], tup2[index]) > near_tolerant:
            return False
    return True


def get_most_colors(pixdata, img_width, img_height, color_tolerant):
    """
    get the most colors from picture

    :param pixdata:
    :param img_width:
    :param img_height:
    :param color_tolerant:
    :return:
    """
    most_color_ = []
    for index in range(4):
        color_stack_ = []
        counter_ = []
        left_border = 2 + int(img_width / 4) * index
        right_border = 2 + int(img_width / 4) * (index + 1)
        for x in range(left_border, right_border):
            for y in range(1, img_height):
                if pixdata[x, y][0] + pixdata[x, y][1] + pixdata[x, y][2] < color_tolerant:
                    if pixdata[x, y] in color_stack_:
                        counter_[color_stack_.index(pixdata[x, y])] += 1
                    else:
                        color_stack_.append(pixdata[x, y])
                        counter_.append(1)
        most_color_.append(color_stack_[get_max_key(counter_)])
    return most_color_


def get_char_position(pixdata, most_color_, img_width, img_height, size_tolerant):
    position_ = [[] for i in range(4)]
    for index in range(4):
        left_border = max(2, 2 + int(img_width / 4) * index - size_tolerant)
        right_border = min(2 + int(img_width / 4) * (index + 1) + size_tolerant, img_width)
        begin_flag = False
        for x in range(left_border, right_border):
            if most_color_[index] in [pixdata[x, y] for y in range(1, img_height)] and not begin_flag:
                position_[index].append(x)
                begin_flag = True
            elif most_color_[index] not in [pixdata[x, y] for y in range(1, img_height)] and begin_flag:
                position_[index].append(x)
                begin_flag = False
        if begin_flag:
            position_[index].append(right_border - 1)

    return position_


def cut_into_piece(img, most_color_, position_, img_width, img_height):
    vectors_ = []
    for index in range(4):
        vector_ = []
        new_img = img.crop((position_[index][0], 0, position_[index][1], img_height))
        new_img = new_img.resize((15, img_height), Image.ANTIALIAS)
        pixdata = new_img.load()
        for y in range(new_img.size[1]):
            for x in range(new_img.size[0]):
                if is_near_color(most_color_[index], pixdata[x, y], near_tolerant=50):
                    vector_.append(1)
                else:
                    vector_.append(0)
        vectors_.append(vector_)

    return vectors_


def img2Vector(img_path):
    color_tolerant = 3 * 180
    size_tolerant = 5
    img = Image.open(img_path)
    img = img.convert('RGB')
    img_width = img.size[0] - 4
    img_height = img.size[1] - 2
    pixdata = img.load()
    most_color_ = get_most_colors(pixdata, img_width, img_height, color_tolerant)
    if is_same_neighbor(most_color_):
        return False
    position_ = get_char_position(pixdata, most_color_, img_width, img_height, size_tolerant)
    vectors_ = cut_into_piece(img, most_color_, position_, img_width, img_height)
    return vectors_






