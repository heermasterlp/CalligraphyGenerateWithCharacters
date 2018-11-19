# coding: utf-8
import cv2
import numpy as np
import argparse
import xml.etree.ElementTree as ET
import os
import math

from utils.tools import getSingleMaxBoundingBoxOfImage


def generate_calligraphy(sentence, font, width, height, char_num, word_space_mode, column_space_mode, x_offset=100, y_offset=100):
    if sentence == '':
        return

    # find character code with xml database
    tree = ET.parse('data\\radicals.xml')
    root = tree.getroot()
    code_list = []
    for ch in sentence:
        code = ''
        for i in range(len(root)):
            element = root[i]
            if element.attrib['TAG'] == ch:
                code = element.attrib['ID']
                break
        code_list.append(code)

    images_path = 'images\\'
    images_names = []
    for f in os.listdir(images_path):
        if '.png' in f or '.jpg' in f or '.jpeg' in f:
            images_names.append(f)
    print(images_names)

    # based file name to get images

    images_list = []
    for code in code_list:
        file_name = ''
        print('code:', code)
        print('font:', font)
        for name in images_names:
            if (font + '_' + code) in name:
                file_name = name
                break
        if file_name == '':
            file_name = 'kai_' + code + '.png'
        print('file name:', file_name)
        file_path = os.path.join(images_path, file_name)
        print(file_path)
        img = cv2.imread(file_path, 0)

        images_list.append(img.copy())

    # change image from rectangle to square based on the minibox
    images_squares = []
    for i in range(len(images_list)):
        img = images_list[i]

        x0, y0, w, h = getSingleMaxBoundingBoxOfImage(img)
        if i == 10:
            print('x0:', x0, 'y0:', y0, 'w:', w, 'h:', h)
        rect = img[y0: y0+h, x0: x0+w]
        new_w = max(w, h)

        new_rect = np.ones((new_w, new_w)) * 255
        print('rect shape:', rect.shape, 'new_rect:', new_rect.shape)
        if w > h:
            new_rect[int((w-h)/2): int((w-h)/2) + h, 0: w] = rect
        else:
            new_rect[0: h, int((h-w)/2): int((h-w)/2) + w] = rect

        images_squares.append(new_rect)

    # resize all images squares with same size
    images_squares_resized = []
    new_size = 0
    for i in range(len(images_squares)):
        new_size += images_squares[i].shape[0]

    # new size of square is the mean value of all squares
    new_size = int(new_size / len(images_squares) * 0.5)
    print(new_size)

    for i in range(len(images_squares)):
        img = images_squares[i]
        img = cv2.resize(img, (new_size, new_size))
        images_squares_resized.append(img)

    # calculate the calligraphy image size based on the number of characters and
    column_num = math.ceil(len(images_squares_resized) / char_num)
    row_num = char_num
    word_space_dist = 0
    column_space_dist = 0
    if word_space_mode == 'thick':
        print('word space is thick')
    elif word_space_mode == 'normal':
        print('word space is normal')
        word_space_dist = int(new_size * 0.1)
    elif word_space_mode == 'sparse':
        print('word space is sparse')
        word_space_dist = int(new_size * 0.2)

    if column_space_mode == 'thick':
        print('column space is thick')
    elif column_space_mode == 'normal':
        print('column space is normal')
        column_space_dist = int(new_size * 0.4)
    elif column_space_mode == 'sparse':
        print('column space is sparse')
        column_space_dist = int(new_size * 0.6)

    bk_w = int(new_size * column_num + column_space_dist * (column_num - 1) + x_offset)
    bk_h = int(new_size * row_num + word_space_dist * (row_num - 1) + y_offset)

    bk = np.ones((bk_h, bk_w)) * 255
    print('bk shape:', bk.shape)

    # layout of all characters
    for i in range(1, len(images_squares_resized)+1):
        print('process', i)
        column_id = math.ceil(i / char_num)
        row_id = i % char_num
        if row_id == 0:
            row_id = 5
        print('colu %d row %d' % (column_id, row_id))

        insert_pos_y = int(y_offset/2) + (row_id-1) * new_size + (row_id-1)*word_space_dist
        insert_pos_x = bk.shape[1] - int(x_offset/2) - column_id * new_size - (column_id-1)* column_space_dist


        print('insert pos:', (insert_pos_y, insert_pos_x))
        print('bk rect:', bk[insert_pos_y: insert_pos_y+new_size, insert_pos_x: insert_pos_x+new_size].shape)
        bk[insert_pos_y: insert_pos_y+new_size, insert_pos_x: insert_pos_x+new_size] = images_squares_resized[i-1]









    # show iamges
    # for i in range(len(images_squares)):
    #     img = images_squares[i]
    #     cv2.imshow('%d_img' % i, img)
    #
    # for i in range(len(images_squares_resized)):
    #     img = images_squares_resized[i]
    #     cv2.imshow('resied_%d_img' % i, img)
    #
    cv2.imshow('bk', bk)
    cv2.waitKey(0)
    cv2.destroyAllWindows()












parser = argparse.ArgumentParser(description='Generate calligraophy with type into a Chinese characters string')
parser.add_argument('--sentence', dest='sentence', type=str, required=True, help='Sentence of calligraphy')
parser.add_argument('--font', dest='font', required=True, help='Font of character')
parser.add_argument('--width', dest='width', type=int, default=400, help='The width of calligraphy image')
parser.add_argument('--height', dest='height', type=int, default=100, help='The height of calligraphy image')
parser.add_argument('--char_num', dest='char_num', type=int, default=5, help='The number of characters in one column')
parser.add_argument('--word_space_mode', dest='word_space_mode', type=str, default='normal', help='The type of word '
                    'space, includes: thick, normal and sparse')
parser.add_argument('--column_space_mode', dest='column_space_mode', type=str, default='normal', help='The type of '
                    'column space, including: thick, normal and sparse')

args = parser.parse_args()

if __name__ == '__main__':
    generate_calligraphy(args.sentence, args.font, args.width, args.height, args.char_num, args.word_space_mode,
                         args.column_space_mode)