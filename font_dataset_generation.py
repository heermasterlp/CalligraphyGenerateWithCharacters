# coding: utf-8
import xml.etree.ElementTree as ET
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont

radical_xml_path = '../../Data/Characters/radicals.xml'

# font_path = '../../Data/Fonts/simkai.ttf'
font_path = '../../Data/Fonts/simsun.ttc'
# font_path = '../../Data/Fonts/qigongscfont.ttf'

base_path = '../../Data/Calligraphy_database'

jianti_chars_path = '../../Data/Characters/jianti_chars.txt'
fanti_chars_path = '../../Data/Characters/fanti_chars.txt'

font_str = 'song'


def generate_char_image(character, font_path, width, height, image_mode='L', x_offset=0, y_offset=0):
    if character == '' or font_path == '' or width <= 0 or height <=0:
        return

    font = ImageFont.truetype(font_path, size=width)
    default_color = 255
    if image_mode == 'RGB':
        default_color = (255, 255, 255)
    img = Image.new(image_mode, (width, height), default_color)
    img_ = img.copy()
    draw = ImageDraw.Draw(img)
    draw.text((x_offset, y_offset), character, 0, font=font)

    if img_ == img:
        return None
    else:
        return img


# read jian ti and fan ti chars
jianti_chars = None
fanti_chars = None
with open(jianti_chars_path, 'r') as f:
    chars = f.readlines()
    jianti_chars = chars[0]

with open(fanti_chars_path, 'r') as f:
    chars = f.readlines()
    fanti_chars = chars[0]

if len(jianti_chars) != len(fanti_chars):
    print("jianti len is not equal with fanti len!")

# make font images directory
root_path = os.path.join(base_path, font_str)
if not os.path.exists(root_path):
    os.makedirs(root_path)


# image size
image_size = 220


tree = ET.parse(radical_xml_path)
root = tree.getroot()
print('root len:', len(root))

for i in range(len(root)):
    element = root[i]
    character = element.attrib['TAG']
    code = element.attrib['ID']

    if len(character) > 1:
        continue
    print('Processing: ', character)
    # find fanti with this jianti character
    fanti_index = jianti_chars.find(character)
    fanti_char = fanti_chars[fanti_index]
    file_name = character + '_' + code + '_' + fanti_char + '_' + str(1) + '.png'

    file_path = os.path.join(root_path, file_name)

    img = generate_char_image(character, font_path, width=image_size, height=image_size)
    if img:
        img.save(file_path)



