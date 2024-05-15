#pip install tensorflow
#pip install tensorflow_hub

import sys
import copy
import time
import argparse

import cv2 as cv
import numpy as np
import tensorflow as tf
import tensorflow_hub as tfhub

#Method to set arguments
def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--file", type=str, default=None)
    parser.add_argument("--width", help='cap width', type=int, default=960)
    parser.add_argument("--height", help='cap height', type=int, default=540)

    parser.add_argument('--mirror', action='store_true')

    parser.add_argument("--model_select", type=int, default=0)
    parser.add_argument("--keypoint_score", type=float, default=0.4)

    args = parser.parse_args()

    return args

#Method to run models
def run_inference(model, input_size, image):
    image_width, image_height = image.shape[1], image.shape[0]

    input_image = cv.resize(image, dsize=(input_size, input_size))  # Revert size in WebCam
    input_image = cv.cvtColor(input_image, cv.COLOR_BGR2RGB)  # Set image_color
    input_image = input_image.reshape(-1, input_size, input_size, 3)  # reshape size in input_image
    input_image = tf.cast(input_image, dtype=tf.int32)

    outputs = model(input_image) #run models

    keypoints_with_scores = outputs['output_0'].numpy()
    keypoints_with_scores = np.squeeze(keypoints_with_scores)

    keypoints = []
    scores = []
    for index in range(17):
        keypoint_x = int(image_width * keypoints_with_scores[index][1])
        keypoint_y = int(image_height * keypoints_with_scores[index][0])
        score = keypoints_with_scores[index][2]

        keypoints.append([keypoint_x, keypoint_y])
        scores.append(score)

    return keypoints, scores