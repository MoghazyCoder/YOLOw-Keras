# import the needed modules
import os
from matplotlib.pyplot import imshow
import scipy.io
import scipy.misc
import numpy as np
from PIL import Image
#import image
import cv2
from keras import backend as K
from keras.models import load_model

# The below provided fucntions will be used from yolo_utils.py
from yolo_utils import read_classes, read_anchors, generate_colors, preprocess_image, draw_boxes

# The below functions from the yad2k library will be used
from yad2k.models.keras_yolo import yolo_head, yolo_eval


#Provide the name of the image that you saved in the images folder to be fed through the network
cap = cv2.VideoCapture(-1)
yolo_model = load_model("yolo.h5")

size = 608, 608
while True:
	ret, frame = cap.read()
	input_image = Image.fromarray(frame)
	width, height = input_image.size
	width = np.array(width, dtype=float)
	height = np.array(height, dtype=float)

	#Assign the shape of the input image to image_shapr variable
	image_shape = (height, width)


	#Loading the classes and the anchor boxes that are provided in the madel_data folder
	class_names = read_classes("coco_classes.txt")
	anchors = read_anchors("yolo_anchors.txt")

	#Load the pretrained model. Please refer the README file to get info on how to obtain the yolo.h5 file
	
	#Print the summery of the model
	#yolo_model.summary()

	#Convert final layer features to bounding box parameters
	yolo_outputs = yolo_head(yolo_model.output, anchors, len(class_names))

	#Now yolo_eval function selects the best boxes using filtering and non-max suppression techniques.
	# If you want to dive in more to see how this works, refer keras_yolo.py file in yad2k/models
	boxes, scores, classes = yolo_eval(yolo_outputs, image_shape)


	# Initiate a session
	sess = K.get_session()


	#Preprocess the input image before feeding into the convolutional network
	image, image_data = preprocess_image(input_image, model_image_size = (608, 608))

	#Run the session
	out_scores, out_boxes, out_classes = sess.run([scores, boxes, classes],feed_dict={yolo_model.input:image_data,K.learning_phase(): 0})


	#Print the results
	print('Found {} boxes for {}'.format(len(out_boxes), "jkaka"))
	#Produce the colors for the bounding boxs
	colors = generate_colors(class_names)
	#Draw the bounding boxes
	draw_boxes(image, out_scores, out_boxes, out_classes, class_names, colors)
	pix = np.array(image)
	cv2.imshow('frame' ,pix)
	k = cv2.waitKey(1)
	if k == 27:
		break
