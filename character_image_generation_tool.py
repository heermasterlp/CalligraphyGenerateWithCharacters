# coding: utf-8
import xml.etree.ElementTree as ET
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont


def generate_char_image(character, font_path, width, height, image_mode='L', x_offset=0, y_offset=0):
    if character == '' or font_path == '' or width <= 0 or height <=0:
        return

    font = ImageFont.truetype(font_path, size=width)
    default_color = 255
    if image_mode == 'RGB':
        default_color = (255, 255, 255)
    img = Image.new(image_mode, (width, height), default_color)
    draw = ImageDraw.Draw(img)
    draw.text((x_offset, y_offset), character, 0, font=font)

    return img



song_font_path = 'D:\python_projects\ChineseCalligraphyGenerationModel\\fontset\simsun.ttc'
kai_font_path = 'D:\python_projects\ChineseCalligraphyGenerationModel\\fontset\simkai.ttf'
qigong_font_path = 'D:\python_projects\ChineseCalligraphyGenerationModel\\fontset\qigongscfont.TTF'


tree = ET.parse('data\\radicals.xml')
root = tree.getroot()

print(len(root))

images_root_path = 'images\\'

for i in range(len(root)):
    element = root[i]
    character = element.attrib['TAG']
    print('Processing: ', character)
    if len(character) > 1:
        continue

    file_name = 'qigong_' + element.attrib['ID'] + '.png'


    font_path = qigong_font_path
    size = 220
    # if i % 3 == 0:
    #     font_path = kai_font_path
    #     file_name = 'kai_' + file_name
    #
    # elif i % 3 == 1:
    #     # song font
    #     font_pth = song_font_path
    #     size = 200
    #     file_name = 'song_' + file_name
    # elif i % 3 == 2:
    #     # qigong font
    #     font_path = qigong_font_path
    #     size = 220
    #     file_name = 'qigong_' + file_name

    file_path = os.path.join(images_root_path, file_name)

    # generate characeter image with character, font dictionary and image size
    img = generate_char_image(character, font_path, width=size, height=size)

    img.save(file_path)




