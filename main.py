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
    folder_for_testing = './testing_images'
    folder_for_validating = './validating_images'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(folder_for_testing):
        os.makedirs(folder_for_testing)

    names_background = []
    background_len = 0
    for filename in os.listdir(input_background):
        names_background.append(filename)
        background_len += 1
    back_images = pd.DataFrame(np.array(names_background), columns=['name_file'])
    # iterate through the folder with objects
    num_img = 0
    # iterate through different classes of objects

    for id_obj in range(len(input_objects)):
        for filename in os.listdir(input_objects[id_obj]):
            break
            print(filename)
            object_img = cv2.imread(input_objects[id_obj] + '/' + filename)
            object_height, object_width, _ = object_img.shape
            id_back = random.randint(1, background_len-1)
            background_img = cv2.imread(input_background + '/' + back_images.loc[id_back, 'name_file'])
#            print(back_images.loc[id_back, 'name_file'])
            back_height, back_width, _ = background_img.shape
#            print('back_width ', back_width)
            # increase the size of background to be bigger than object size
            scale_width = object_width / back_width
            scale_height = object_height / back_height
            imgScale = max(scale_width, scale_height) * random.randint(3, 8)
            newX, newY = background_img.shape[1] * imgScale, background_img.shape[0] * imgScale
            background_img = cv2.resize(background_img, (int(newX), int(newY)))
            # post the image randomly into this background image
            back_height, back_width, _ = background_img.shape
#            print('back_width ', back_width)
            min_x = object_width // 2 + 1
#            print('min_x, ', min_x)
            max_x = back_width - (object_width // 2 + 1)
#            print('max_x, ', max_x)
            min_y = object_height // 2 + 1
            max_y = back_height - (object_height // 2 + 1)
            x_center = random.randint(min_x, max_x)
            y_center = random.randint(min_y, max_y)
            x_start = x_center - object_width // 2
            y_start = y_center - object_height // 2
            background_img[y_start:y_start + object_height, x_start:x_start + object_width] = object_img
            cv2.imwrite(output_folder + '/' + str(num_img) + '.jpg', background_img)
            # save text files to the same folder with the same name
            x_yolo = x_center / back_width
            y_yolo = y_center / back_height
            width_yolo = object_width / back_width
            height_yolo = object_height / back_height
            output_line = str(id_obj) + ' ' + str(x_yolo) + ' ' + str(y_yolo) + ' ' + str(width_yolo) + ' ' + str(
                height_yolo)
            f = open(output_folder + '/' + str(num_img) + '.txt', "w+")
            f.write(output_line)
            f.close()
            num_img += 1
    num_img = 240
    id_obj = 1
    print('generate testing images')
    testing_num = 0
    for id_obj in range(len(input_objects)):
        for filename in os.listdir(input_objects[id_obj]):
            print(filename)
            print(0.2 * (num_img // (id_obj + 1)))
            if testing_num >= 0.2 * (num_img // (id_obj + 1)):
                print(testing_num)
                break
            object_img = cv2.imread(input_objects[id_obj] + '/' + filename)
            object_height, object_width, _ = object_img.shape
            id_back = random.randint(1, background_len - 1)
            background_img = cv2.imread(input_background + '/' + back_images.loc[id_back, 'name_file'])
            #            print(back_images.loc[id_back, 'name_file'])
            back_height, back_width, _ = background_img.shape
            #            print('back_width ', back_width)
            # increase the size of background to be bigger than object size
            scale_width = object_width / back_width
            scale_height = object_height / back_height
            imgScale = max(scale_width, scale_height) * random.randint(3, 8)
            newX, newY = background_img.shape[1] * imgScale, background_img.shape[0] * imgScale
            background_img = cv2.resize(background_img, (int(newX), int(newY)))
            # post the image randomly into this background image
            back_height, back_width, _ = background_img.shape
            #            print('back_width ', back_width)
            min_x = object_width // 2 + 1
            #            print('min_x, ', min_x)
            max_x = back_width - (object_width // 2 + 1)
            #            print('max_x, ', max_x)
            min_y = object_height // 2 + 1
            max_y = back_height - (object_height // 2 + 1)
            x_center = random.randint(min_x, max_x)
            y_center = random.randint(min_y, max_y)
            x_start = x_center - object_width // 2
            y_start = y_center - object_height // 2
            background_img[y_start:y_start + object_height, x_start:x_start + object_width] = object_img
            cv2.imwrite(folder_for_testing + '/' + str(testing_num) + '.jpg', background_img)
            # save text files to the same folder with the same name
            x_yolo = x_center / back_width
            y_yolo = y_center / back_height
            width_yolo = object_width / back_width
            height_yolo = object_height / back_height
            output_line = str(id_obj) + ' ' + str(x_yolo) + ' ' + str(y_yolo) + ' ' + str(width_yolo) + ' ' + str(
                height_yolo)
            f = open(folder_for_testing + '/' + str(testing_num) + '.txt', "w+")
            f.write(output_line)
            f.close()

            testing_num += 1
    print('done')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_objects', nargs='+', type=str, default='./objects_1 ./objects_2', help='')
    parser.add_argument('--input_background', type=str, default='./input_background', help='')
    parser.add_argument('--output_folder', type=str, default='./output_folder', help='')

    args = parser.parse_args()
    main(args)
