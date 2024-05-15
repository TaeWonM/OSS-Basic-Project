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

#main Method
def main():

    args = get_args()
    cap_device = args.device
    cap_width = args.width
    cap_height = args.height

    if args.file is not None:
        cap_device = args.file

    mirror = args.mirror
    model_select = args.model_select
    keypoint_score_th = args.keypoint_score

    # Video Capture
    cap = cv.VideoCapture(cap_device)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

    # Set model
    if model_select == 0:
        model_url = "https://tfhub.dev/google/movenet/singlepose/lightning/4"
        input_size = 192
    elif model_select == 1:
        model_url = "https://tfhub.dev/google/movenet/singlepose/thunder/4"
        input_size = 256
    else:
        sys.exit(
            "*** model_select {} is invalid value. Please use 0-1. ***".format(
                model_select))

    module = tfhub.load(model_url)
    model = module.signatures['serving_default']

    while True:
        start_time = time.time()

        ret, frame = cap.read()
        if not ret:
            break
        if mirror:
            frame = cv.flip(frame, 1)
        debug_image = copy.deepcopy(frame)

        keypoints, scores = run_inference(
            model,
            input_size,
            frame,
        )

        elapsed_time = time.time() - start_time

        debug_image = draw_debug(
            debug_image,
            elapsed_time,
            keypoint_score_th,
            keypoints,
            scores,
        )

        key = cv.waitKey(1)
        if key == 27:  # ESC
            break

        cv.imshow('MoveNet(singlepose) Demo', debug_image)

    cap.release()
    cv.destroyAllWindows()
