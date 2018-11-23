# import cv2
# import numpy as np
# from utils.tools import getSingleMaxBoundingBoxOfImage
#
# path = 'D:\python_projects\CalligraphyGenerateWithCharacters\images\qigong_4E3E.png'
#
# img = cv2.imread(path, 0)
#
# cv2.imshow('ju_', img)
#
#
# x0, y0, w, h = getSingleMaxBoundingBoxOfImage(img)
#
# print(x0, y0, w, h)
#
# img_rect = img[y0:y0+h, x0:x0+w]
#
# cv2.imshow('imgrect', img_rect)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()

chars = "曖駱壘駭駢驪螻騁驗蠑駿睪騏騎騍墾騅坰驂堊騙墊騭埡騷騖塏瞞蟎驁堖騮騫騸驃騾矚驄驏驟驥驤塒塤堝墊垵髏髖髕劄矯術樸機磯塹墮殺礬雜礦權碭桿碼釁銜鬢磚硨補硯碸條襯來袞魘楊榪魎傑魚墻魷襖魯裊魴鮁鮃礪鮎極礱鱸構鮒"
print(len(chars))

for i in range(len(chars)):
    for j in range(i+1, len(chars)):
        if chars[i] == chars[j]:
            print(chars[i])