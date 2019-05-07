#https://www.twobitarcade.net/article/etch-a-snap--processing/
#
#
from PIL import ImageOps, Image
import math
import cv2 ##import cv
import numpy as np

im = Image.open('khan.jpg')


t_width, t_height = (240.0, 144.0) #added the .0 to make the calulation work on mac
c_width, c_height = im.size

wr, hr = t_width / c_width, t_height / c_height

# Scale the dimension closest to the target.
ratio = wr if wr > hr else hr
target = int(c_width * ratio), int(c_height * ratio)

image_r = im.resize(target, Image.ANTIALIAS)

c_width, c_height = image_r.size

# Crop a rectangular region from this image.
# The box is a 4-tuple defining the left, upper, right, and lower pixel coordinate.
hw, hh = c_width // 2, c_height // 2
x, y = t_width // 2, t_height // 2

image_r = image_r.crop((hw - x, hh -y, hw + x, hh + y))

gray = image_r.convert('L')

gray.show()
#image_r.show()

# Finding edges
ocv = np.array(gray)

#if something is above the threshold1 then it is an edge, if it is below the treshold2 then it is not an edge. Try 200 and 50 for more detail.
threshold1 = 200
threshold2 = 100

edgec = cv2.Canny(ocv, threshold1, threshold2)
edgec = Image.fromarray(edgec)
edgec = ImageOps.invert(edgec)
edgec.show()

#continous line

fill_patterns = [
    np.array([[1]]),
    1-np.eye(16),
    1-np.eye(8),
    1-np.eye(4),
]
## this is not working for me
def line_fill(edgec, mask_expand=0):  #replaced img with edgec
    data = np.array(edgec)  # "data" is a height x width x 4 numpy array; replaced img with edgec
    output = data.copy()
    width, height = data.shape
    for n, pattern in enumerate(fill_patterns):
        p_width, p_height = pattern.shape
        fill_image = np.tile(pattern * 255, (width // p_width + 1, height // p_height + 1))
        fill_image = fill_image[:width, :height] #drop down to image dimensions, so we map straight
        output[mask] = fill_image[data == n]
    return Image.fromarray(output)
## this is not working for me
#img = Image.fromarray(output)
#img.show()
