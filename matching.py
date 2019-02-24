# script to place an object into different images
# folder from where we will take the objects
# folder to where we will place this object

import argparse
import os
import cv2
import numpy as np
import random

step = 10
width = 20

def normalize(img):
    height, width = img.shape
    normalizedImg = np.zeros((width, height))
    normalizedImg = cv2.normalize(img, normalizedImg, 0, 255, cv2.NORM_MINMAX)
    return normalizedImg

def generate_patches(img1, img2):
    height, width = img1.shape
    sum_average = 0
    num_patches = 0
    for x1 in range(0, width-step-1, step):
        for y1 in range(0, height-step-1, step):
            y2 = y1 + step
            x2 = x1 + step
            sum1 = int(np.sum(img1[y1:y2, x1:x2]))
            sum2 = int(np.sum(img2[y1:y2, x1:x2]))
            sum_average += abs(sum1 - sum2)
            num_patches += 1
    sum_average = sum_average/num_patches
    list_of_predicted_patches = []
    for x1 in range(0, width-step-1, step):
        for y1 in range(0, height-step-1, step):
            y2 = y1 + step
            x2 = x1 + step
            sum1 = int(np.sum(img1[y1:y2, x1:x2]))
            sum2 = int(np.sum(img2[y1:y2, x1:x2]))
            if abs(sum1-sum2) > 2 * sum_average:
                list_of_predicted_patches.append([x1, y1])
    return list_of_predicted_patches


def draw_patches(list_of_patches, img2):
    for i in range(len(list_of_patches)):
        x1 = list_of_patches[i][0]
        y1 = list_of_patches[i][1]
        x2 = x1 + step
        y2 = y1 + step
        cv2.rectangle(img2,(x1,y1),(x2,y2),(0,255,0),2)
    cv2.imwrite('output.jpg', img2)

def main(args):
    file1 = args.file1
    file2 = args.file2
    img1_ = cv2.imread(file1, 0)
    img2_ = cv2.imread(file2, 0)
    img1 = normalize(img1_)
    img2 = normalize(img2_)

    list_of_patches = generate_patches(img1, img2)
    draw_patches(list_of_patches, img2_)
    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file1', type=str, default='./lemming/00001.jpg', help='')
    parser.add_argument('--file2', type=str, default='./lemming/00123.jpg', help='')
    parser.add_argument('--output_folder', type=str, default='./matching', help='')

    args = parser.parse_args()
    main(args)