import os
import cv2
from shutil import copyfile


input_objects = './output_folder'
output_objects = './output_folder1'
for filename in os.listdir(input_objects):
    if filename[-4:] == '.jpg':
        background_img = cv2.imread(input_objects + '/' + filename)
        back_height, back_width, _ = background_img.shape
        # increase the size of background to be bigger than object size
        scale_width = 300 / back_width
        scale_height = 300 / back_height
        imgScale = min(scale_width, scale_height)
        newX, newY = background_img.shape[1] * imgScale, background_img.shape[0] * imgScale
        background_img = cv2.resize(background_img, (int(newX), int(newY)))
        cv2.imwrite(output_objects + '/' + filename, background_img)
    else:
        copyfile(input_objects + '/' + filename, output_objects + '/' + filename)