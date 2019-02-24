# severstal_hackathon
hackathon on computer vision by Severstal company in Moscow

We created scripts for users to generate data for the neural network YOLO. 

We found the data from kaggle competition (https://www.kaggle.com/gaborvecsei/flats-to-rent-at-budapest) and used it as background images. 

To generate images for training YOLO use augmentation.py script: it takes image '.jpg' file and generates copies of it which are rotated. After rotation, we used scaling: objects are scaled 4 times, from 1 up to 2 times. 

To place the objects to the background images and then to create .txt files as location information of the object in the images, use script main.py: it randomly chooses images from the 'flats-to-rent-at-budapest' dataset and places all the generated objects information for YOLO training in the output_folder along with '.txt' files for object location information. 
