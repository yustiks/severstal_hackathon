from PIL import Image
import os
#import cv2

input_objects = ['./input_background']
output_objects = ['./input_background2']
for id_obj in range(len(input_objects)):
    for filename in os.listdir(input_objects[id_obj]):
#        object_img = cv2.imread(input_objects[id_obj] + '/' + filename)
        print(filename)
        print(filename[-4:])
        if filename[-4:] == '.jpg':
#            im = Image.open(input_objects[id_obj] + '/' + filename)
#            im.save(output_objects[id_obj] + '/' + filename[:-4] + '.png')
            im = Image.open(input_objects[id_obj] + '/' + filename)
            im.save(output_objects[id_obj] + '/' + filename)