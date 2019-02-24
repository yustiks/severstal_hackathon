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
    for x1 in range(0, width-step-1, step):
        for y1 in range(0, height-step-1, step):
            y2 = y1 + step
            x2 = x1 + step
            sum1 = int(np.sum(img1[y1:y2, x1:x2]))
            sum2 = int(np.sum(img2[y1:y2, x1:x2]))
            print(sum1 - sum2)

def main(args):
    file1 = args.file1
    file2 = args.file2
    img1 = cv2.imread(file1, 0)
    img2 = cv2.imread(file2, 0)
    img1 = normalize(img1)
    img2 = normalize(img2)

    generate_patches(img1, img2)
    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file1', type=str, default='./lemming/00001.jpg', help='')
    parser.add_argument('--file2', type=str, default='./lemming/00123.jpg', help='')
    parser.add_argument('--output_folder', type=str, default='./matching', help='')

    args = parser.parse_args()
    main(args)