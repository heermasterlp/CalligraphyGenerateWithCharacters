# coding: utf-8
import xml.etree.ElementTree as ET

import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont


jianti_chars_path = '../../Data/Characters/jianti_chars.txt'
fanti_chars_path = '../../Data/Characters/fanti_chars.txt'

radical_xml_path = '../../Data/Characters/radicals.xml'

bihua_path = '../../Data/Characters/uninsided_bihua.txt'


def prettyXml(element, indent, newline, level = 0): # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
    if element:  # 判断element是否有子元素
        if element.text == None or element.text.isspace(): # 如果element的text没有内容
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
    #else:  # 此处两行如果把注释去掉，Element的text也会另起一行
        #element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element) # 将elemnt转成list
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1): # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        prettyXml(subelement, indent, newline, level = level + 1) # 对子元素进行递归操作


jianti_chars = None
fanti_chars = None

with open(jianti_chars_path, 'r') as f:
    chars = f.readlines()
    jianti_chars = chars[0]

with open(fanti_chars_path, 'r') as f:
    chars = f.readlines()
    fanti_chars = chars[0]

if len(jianti_chars) != len(fanti_chars):
    print('The number of jianti and fanti not same!')

jianti_diff_list = []
fanti_diff_list = []

for i in range(len(jianti_chars)):
    if jianti_chars[i] != fanti_chars[i]:
        jianti_diff_list.append(jianti_chars[i])
        fanti_diff_list.append(fanti_chars[i])

print(jianti_diff_list)
print(fanti_diff_list)

print(len(jianti_diff_list))

# find fanti chars not in radical.xml
tree = ET.parse(radical_xml_path)
root = tree.getroot()
print('root len:', len(root))

radical_chars = []
for i in range(len(root)):
    element = root[i]
    character = element.attrib['TAG']
    radical_chars.append(character)
print("racial len:", len(radical_chars))

uninside_chars = []
inside_chars = []
for ch in fanti_diff_list:
    if ch not in radical_chars:
        uninside_chars.append(ch)
    else:
        inside_chars.append(ch)
print('%d chars not in radical!' % len(uninside_chars))
print('unside len:', len(uninside_chars))
print(inside_chars)
print(uninside_chars)

uninside_chars_bihua = []
with open(bihua_path, 'r') as f:
    uninside_chars_bihua = f.readlines()

print("bihua", len(uninside_chars_bihua))

# add not inside fanti to radical.xml file
for i in range(len(uninside_chars)):
    ch = uninside_chars[i]
    code = ch.encode('unicode_escape').decode('utf-8').replace('\\u', '').upper()
    elem = ET.Element("RADICAL")
    elem.set("ID", code)
    elem.set("TAG", ch)

    # type
    type_elem = ET.Element("TYPE")
    type_elem.text = "character"
    elem.append(type_elem)

    # structure
    struct_elem = ET.Element("STRUCTURE")
    struct_elem.text = "Single Character"
    elem.append(struct_elem)

    # key radical
    keyrad_elem = ET.Element("KEY_RADICAL")
    keyrad_elem.text = ""
    elem.append(keyrad_elem)

    # bihua
    bihua_elem = ET.Element("STROKE_COUNT")
    bihua_elem.text = uninside_chars_bihua[i].replace('\n', '')
    elem.append(bihua_elem)



    elem.tail = '\n'

    root.insert(len(root), elem)

prettyXml(root, '\t', '\n')


tree.write('new_radical.xml', encoding='utf-8')








