import cv2
import numpy as np
from utils.tools import getSingleMaxBoundingBoxOfImage

path = 'D:\python_projects\CalligraphyGenerateWithCharacters\images\qigong_4E3E.png'

img = cv2.imread(path, 0)

cv2.imshow('ju_', img)


x0, y0, w, h = getSingleMaxBoundingBoxOfImage(img)

print(x0, y0, w, h)

img_rect = img[y0:y0+h, x0:x0+w]

cv2.imshow('imgrect', img_rect)

cv2.waitKey(0)
cv2.destroyAllWindows()