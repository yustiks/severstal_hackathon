# script to place an object into different images
# folder from where we will take the objects
# folder to where we will place this object

import argparse
import os
import cv2
import numpy as np
import random

from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import os

step = 50
width = 100

datagen = ImageDataGenerator(
    rotation_range=5,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.2,
    zoom_range=0.2,
    #        channel_shift_range = 25.,
    horizontal_flip=False,
    vertical_flip=False,
    fill_mode='nearest')

def find_nearest_neighbour(img1, file_folder):
    height, width = img1.shape
    img1 = normalize(img1)
    print('img1 ', img1)
    id_neighbour = 516545020000
    sum_dif = 516545020000
    sum1 = int(np.sum(img1[0:height, 0:width]))
    for filename in os.listdir(file_folder):
        img_temp = cv2.imread(file_folder + '/' + filename)
        img_temp = normalize(img_temp)
#        print('img_temp ', img_temp)
        sum2 = int(np.sum(img_temp[0:height, 0:width]))
        sum = abs(sum1 - sum2)
        if int(sum) < sum_dif:
            sum_dif = sum
            id_neighbour = filename
    print(sum_dif)
    print(id_neighbour)
    return id_neighbour, sum_dif

def resize_images(img, size_img, level):
    if level == 3:
        back_height, back_width, _ = img.shape
    else:
        back_height, back_width = img.shape
    # increase the size of background to be bigger than object size
    scale_width = size_img / back_width
    scale_height = size_img / back_height
    imgScale = min(scale_width, scale_height)
    newX, newY = img.shape[1] * imgScale, img.shape[0] * imgScale
    result_img = cv2.resize(img, (int(newX), int(newY)))
    return result_img

def normalize(img):
#    height, width = img.shape
#    normalizedImg = np.zeros((width, height))
#    normalizedImg = cv2.normalize(img, normalizedImg, 0, 255, cv2.NORM_MINMAX)
#    image = cv2.imread("lenacolor512.tiff", cv2.IMREAD_COLOR)  # uint8 image
    normalizedImg = cv2.normalize(img, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    return normalizedImg


def generate_patches(img1, img2, k):
    height, width = img1.shape
    sum_average = 0
    num_patches = 0
    for x1 in range(0, width - step - 1, step):
        for y1 in range(0, height - step - 1, step):
            y2 = y1 + step
            x2 = x1 + step
            sum1 = int(np.sum(img1[y1:y2, x1:x2]))
            sum2 = int(np.sum(img2[y1:y2, x1:x2]))
            sum_average += abs(sum1 - sum2)
            num_patches += 1
    sum_average = 2 * sum_average / num_patches
    list_of_predicted_patches = []
    for x1 in range(0, width - step - 1, step):
        for y1 in range(0, height - step - 1, step):
            y2 = y1 + step
            x2 = x1 + step
            sum1 = int(np.sum(img1[y1:y2, x1:x2]))
            sum2 = int(np.sum(img2[y1:y2, x1:x2]))
            if abs(sum1 - sum2) > k*sum_average:
                list_of_predicted_patches.append([x1, y1])
    return list_of_predicted_patches


def draw_patches(list_of_patches, img2):
    for i in range(len(list_of_patches)):
        x1 = list_of_patches[i][0]
        y1 = list_of_patches[i][1]
        x2 = x1 + step
        y2 = y1 + step
        cv2.rectangle(img2, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)
    cv2.imwrite('output.jpg', img2)


def generate_many_images(img, n):
    if not os.path.exists('img1'):
        os.makedirs('img1')
    # img = load_img('boat_aug/4.jpg')  # this is a PIL image
    x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
    x = x.reshape((1,) + x.shape)  # this is a Numpy array with shape (1, 3, 150, 150)

    # the .flow() command below generates batches of randomly transformed images
    # and saves the results to the `preview/` directory
    i = 0
    for batch in datagen.flow(x, batch_size=1,
                              save_to_dir='img1', save_prefix='img1', save_format='jpg'):
        i += 1
        if i > n:
            break  # otherwise the generator would loop indefinitely
    return 0


def main(args):
    file1 = args.file1
    file2 = args.file2
    img1_ = cv2.imread(file1, 0)
    img1_ = resize_images(img1_, 500, 2)
    img2_ = cv2.imread(file2, 0)
    img2_ = resize_images(img2_, 500, 2)
    cv2.imwrite('img2_gray.jpg', img2_)
    # generate 100 images from img1_
#    generate_many_images(img1_, 500)
#    filename_, _ = find_nearest_neighbour(img2_, './img1')
#    img1_ = cv2.imread('./img1/' + filename_, 0)
    img1 = normalize(img1_)
    img2 = normalize(img2_)
    img2_out = cv2.imread(file2)
    img2_out = resize_images(img2_out, 500, 3)
    list_of_patches = generate_patches(img1, img2, 1)
    draw_patches(list_of_patches, img2_out)
    print('drawing done')
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file1', type=str, default='./img1.jpg', help='')
    parser.add_argument('--file2', type=str, default='./img2.jpg', help='')
    parser.add_argument('--output_folder', type=str, default='./matching', help='')

    args = parser.parse_args()
    main(args)
