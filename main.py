# script to place an object into different images
# folder from where we will take the objects
# folder to where we will place this object

import argparse
import os
import cv2
import pandas as pd
import numpy as np
import random


def main(args):
    input_objects = args.input_objects
    input_background = args.input_background
    output_folder = args.output_folder
    names_background = []
    background_len = 0
    for filename in os.listdir(input_background):
        names_background.append(filename)
        background_len += 1
    back_images = pd.DataFrame(np.array(names_background), columns=['name_file'])

    # iterate through the folder with objects
    num_img = 0
    for filename in os.listdir(input_objects):
        object_img = cv2.imread(input_objects + '/' + filename)
        id_back = random.randint(1, background_len)
        background_img = cv2.imread(input_background + '/' + back_images.loc[id_back, 'name_file'])
        # post the image randomly into this background image
        back_height, back_width, _ = background_img.shape
        object_height, object_width, _ = object_img.shape
        min_x = object_width // 2 + 1
        max_x = back_width - (object_width // 2 + 1)
        min_y = object_height // 2 + 1
        max_y = back_height - (object_height // 2 + 1)
        x_center = random.randint(min_x, max_x)
        y_center = random.randint(min_y, max_y)
        x_start = x_center - object_width // 2
        y_start = y_center - object_height // 2
        background_img[y_start:y_start + object_height, x_start:x_start + object_width] = object_img
        cv2.imwrite(output_folder + '/' + str(num_img) + '.jpg', background_img)
        # save text files to the same folder with the same name
        x_yolo = x_center/back_width
        y_yolo = y_center/back_height
        width_yolo = object_width/back_width
        height_yolo = object_height/back_height
        class_id = 0
        output_line = str(class_id) + ' ' + str(x_yolo) + ' ' + str(y_yolo) + ' ' + str(width_yolo) + ' ' + str(height_yolo)
        f = open(output_folder + '/' + str(num_img) + '.txt', "w+")
        f.write(output_line)
        f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_objects', type=str, default='./input_objects', help='')
    parser.add_argument('input_background', type=str, default='./input_background', help='')
    parser.add_argument('output_folder', type=str, default='./output_folder', help='')
    args = parser.parse_args()
    main(args)
