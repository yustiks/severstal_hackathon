from PIL import Image, ImageFont, ImageDraw
import argparse
import os
import numpy as np
import cv2

def main(args):
    input_objects = args.input_objects
    output_objects = args.output_objects
    for i in range(len(input_objects)):
        for filename in os.listdir(input_objects[i]):
            img = Image.open(input_objects[i] + '/' + filename)
            # converted to have an alpha layer
            im2 = img.convert('RGBA')
            # rotated image
            for angle in np.arange(0, 360, 15):
                rot = im2.rotate(angle, expand=1)
                # a white image same size as rotated image
                fff = Image.new('RGBA', rot.size, (255,)*4)
                # create a composite image using the alpha layer of rot as a mask
                out = Image.composite(rot, fff, rot)
                # save your work (converting back to mode='1' or whatever..)
                out.convert(img.mode).save(output_objects[i] + '/' + str(angle) + filename)
                img_temp = cv2.imread(output_objects[i] + '/' + str(angle) + filename)
                for scale in range(1, 5):
                    scale = 1 + scale/4
                    newX, newY = img_temp.shape[1] * scale, img_temp.shape[0] * scale
                    big_image = cv2.resize(img_temp, (int(newX), int(newY)))
                    cv2.imwrite(output_objects[i] + '/' + str(angle) + filename[:-4] + '_' + str(scale*100) + '.jpg', big_image)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_objects', nargs='+', type=str, default='./input_objects_1 ./input_objects_2', help='')
    parser.add_argument('--output_objects', nargs='+', type=str, default='./objects_1 ./objects_2', help='')
    args = parser.parse_args()
    main(args)
