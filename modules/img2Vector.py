import os
from PIL import Image
from .listUtils import is_same_neighbor


def get_max_key(numbers_):
    max_number = numbers_[0]
    for index in range(len(numbers_)):
        if numbers_[index] > max_number:
            max_number = numbers_[index]
    return numbers_.index(max_number)


def is_near_color(tup1, tup2, color_tolerant=70):
    diff = 0
    for index in range(3):
        diff += abs(tup1[index] - tup2[index])

    if diff < color_tolerant:
        return True
    else:
        return False


def get_most_colors(pixdata, img_width, img_height, max_color):
    """
    get the most colors from picture

    :param pixdata:
    :param img_width:
    :param img_height:
    :param max_color:
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
                if pixdata[x, y][0] + pixdata[x, y][1] + pixdata[x, y][2] < max_color:
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
        flagStack = FlagStack(3)
        for x in range(left_border, right_border):
            in_flag = False
            for y in range(1, img_height):
                if is_near_color(most_color_[index], pixdata[x, y]):
                    in_flag = True
                    break
            flagStack.push(in_flag)
            if flagStack.get_total_flag() and not begin_flag:
                position_[index].append(x - flagStack.get_middle_pos())
                begin_flag = True
            elif not flagStack.get_total_flag() and begin_flag and x - left_border > 5:
                position_[index].append(x - flagStack.get_middle_pos())
                begin_flag = False
                break
        if begin_flag:
            position_[index].append(right_border - 1)

        begin_flag = False
        flagStack = FlagStack(3)
        for y in range(1, img_height):
            in_flag = False
            for x in range(position_[index][0], position_[index][1] + 1):
                if is_near_color(most_color_[index], pixdata[x, y]):
                    in_flag = True
                    break
            flagStack.push(in_flag)
            if flagStack.get_total_flag() and not begin_flag:
                position_[index].append(y - flagStack.get_middle_pos())
                begin_flag = True
            elif not flagStack.get_total_flag() and begin_flag:
                position_[index].append(y - flagStack.get_middle_pos())
                begin_flag = False
                break
        if begin_flag:
            position_[index].append(img_height - 1)

    return position_


def knot_out(img, most_color_, img_width, img_height, size_tolerant):
    img_ = []
    for index in range(4):
        left_border = max(2, 2 + int(img_width / 4) * index - size_tolerant)
        right_border = min(2 + int(img_width / 4) * (index + 1) + size_tolerant, img_width + 2)
        new_img = img.crop((left_border, 1, right_border, img_height + 1))
        # pixdata = new_img.load()
        # for y in range(new_img.size[1]):
        #     for x in range(new_img.size[0]):
        #         if is_near_color(pixdata[x, y], most_color_[index], color_tolerant=100):
        #             pixdata[x, y] = (0, 0, 0)
        #         else:
        #             pixdata[x, y] = (255, 255, 255)
        img_.append(new_img)

    return img_


def remove_padding(img_, most_color_, new_width=15, new_height=20, count_tolerant=1):
    for index in range(4):
        position_ = []
        img = img_[index]
        pixdata = img.load()

        for x in range(img.size[0]):
            point_count = 0
            for y in range(img.size[1]):
                if is_near_color(pixdata[x, y], most_color_[index], color_tolerant=10):
                    point_count += 1
            if point_count >= count_tolerant:
                position_.append(x)
                break

        for y in range(img.size[1]):
            point_count = 0
            for x in range(img.size[0]):
                if is_near_color(pixdata[x, y], most_color_[index], color_tolerant=10):
                    point_count += 1
            if point_count >= count_tolerant:
                position_.append(y)
                break

        for x in range(img.size[0] - 1, -1, -1):
            point_count = 0
            for y in range(img.size[1]):
                if is_near_color(pixdata[x, y], most_color_[index], color_tolerant=10):
                    point_count += 1
            if point_count >= count_tolerant:
                position_.append(x)
                break

        for y in range(img.size[1] - 1, -1, -1):
            point_count = 0
            for x in range(img.size[0]):
                if is_near_color(pixdata[x, y], most_color_[index], color_tolerant=10):
                    point_count += 1
            if point_count >= count_tolerant:
                position_.append(y)
                break

        new_img = img.crop(tuple(position_))
        new_img = new_img.resize((new_width, new_height), Image.ANTIALIAS)
        img_[index] = new_img

    return img_


def cut_into_piece(img, most_color_, position_, img_width, img_height, image_tag):
    if not os.path.exists('cut'):
        os.mkdir('cut')
    if not os.path.exists('cut_vector'):
        os.mkdir('cut_vector')
    vectors_ = []
    for index in range(4):
        vector_ = []
        vector = []
        new_img = img.crop((position_[index][0], position_[index][2], position_[index][1], position_[index][3]))
        new_img = new_img.resize((15, 20), Image.ANTIALIAS)
        pixdata = new_img.load()
        for y in range(new_img.size[1]):
            line = []
            for x in range(new_img.size[0]):
                if is_near_color(most_color_[index], pixdata[x, y]):
                    vector_.append(1)
                    line.append(1)
                else:
                    vector_.append(0)
                    line.append(0)
            vector.append(line)
        vectors_.append(vector_)
        if not os.path.exists('cut' + os.sep + image_tag[index]):
            os.mkdir('cut' + os.sep + image_tag[index])
        new_img.save('cut' + os.sep + image_tag[index] + os.sep + str(len(os.listdir('cut' + os.sep + image_tag[index]))) + '.png', 'png')
        if not os.path.exists('cut_vector' + os.sep + image_tag[index]):
            os.mkdir('cut_vector' + os.sep + image_tag[index])
        with open('cut_vector' + os.sep + image_tag[index] + os.sep + str(len(os.listdir('cut_vector' + os.sep + image_tag[index]))), 'w') as fr:
            for line in vector:
                for item in line:
                    fr.write(str(item))
                fr.write('\n')

    return vectors_


# def img2Vector(img_path, image_tag):
#     max_color = 3 * 180
#     size_tolerant = 5
#     img = Image.open(img_path)
#     img = img.convert('RGB')
#     img_width = img.size[0] - 4
#     img_height = img.size[1] - 2
#     pixdata = img.load()
#     most_color_ = get_most_colors(pixdata, img_width, img_height, max_color)
#     if is_same_neighbor(most_color_):
#         return False
#     img_ = remove_padding(knot_out(img, most_color_, img_width, img_height, size_tolerant), most_color_)
#
#     if not os.path.exists('cut'):
#         os.mkdir('cut')
#     if not os.path.exists('cut_vector'):
#         os.mkdir('cut_vector')
#
#     vectors_ = []
#     for index in range(4):
#         vector_ = []
#         if not os.path.exists('cut' + os.sep + image_tag[index]):
#             os.mkdir('cut' + os.sep + image_tag[index])
#         img_[index].save('cut' + os.sep + image_tag[index] + os.sep + str(len(os.listdir('cut' + os.sep + image_tag[index]))) + '.png', 'png')
#
#         pixdata = img_[index].load()
#         for y in range(img_[index].size[1]):
#             for x in range(img_[index].size[0]):
#                 if is_near_color(pixdata[x, y], most_color_[index], color_tolerant=100):
#                     vector_.append(1)
#                 else:
#                     vector_.append(0)
#         vectors_.append(vector_)
#
#         vector_ = [str(item) for item in vector_]
#         line = '\n'.join([''.join(vector_[0 + i * img_[index].size[0]: 0 + (i + 1) * img_[index].size[0]]) for i in range(img_[index].size[1] - 1)])
#         if not os.path.exists('cut_vector' + os.sep + image_tag[index]):
#             os.mkdir('cut_vector' + os.sep + image_tag[index])
#         with open('cut_vector' + os.sep + image_tag[index] + os.sep + str(len(os.listdir('cut_vector' + os.sep + image_tag[index]))), 'w') as fr:
#             fr.write(line)
#
#     # position_ = get_char_position(pixdata, most_color_, img_width, img_height, size_tolerant)
#     # vectors_ = cut_into_piece(img, most_color_, position_, img_width, img_height, image_tag)
#
#     return vectors_


def img2Vector(img_path):
    max_color = 3 * 180
    size_tolerant = 5
    img = Image.open(img_path)
    img = img.convert('RGB')
    img_width = img.size[0] - 4
    img_height = img.size[1] - 2
    pixdata = img.load()
    most_color_ = get_most_colors(pixdata, img_width, img_height, max_color)
    if is_same_neighbor(most_color_):
        return False
    img_ = remove_padding(knot_out(img, most_color_, img_width, img_height, size_tolerant), most_color_)

    vectors_ = []
    for index in range(4):
        vector_ = []
        pixdata = img_[index].load()
        for y in range(img_[index].size[1]):
            for x in range(img_[index].size[0]):
                if is_near_color(pixdata[x, y], most_color_[index], color_tolerant=100):
                    vector_.append(1)
                else:
                    vector_.append(0)
        vectors_.append(vector_)

    return vectors_


class FlagStack(object):

    def __init__(self, depth):
        self.depth = depth
        self.flag_ = [False for index in range(depth)]

    def push(self, flag):
        for index in range(self.depth - 1, 0, -1):
            self.flag_[index] = self.flag_[index - 1]
        self.flag_[0] = flag

    def get_middle_pos(self):
        return int(self.depth / 2)

    def get_total_flag(self):
        for flag in self.flag_:
            if flag:
                return True
        return False
