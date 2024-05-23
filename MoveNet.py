#pip install tensorflow
#pip install tensorflow_hub

import sys
import copy
import math
import cv2 as cv
import numpy as np
import tensorflow as tf
import tensorflow_hub as tfhub

def radian (one, center, two):
  o1 = math.atan2((two[1]-center[1]),(two[0] - center[0])) 
  o2 = math.atan2((one[1]-center[1]),(one[0] - center[0]))
  if (abs((o1-o2) * 180/math.pi) >= 180):
    return 360 - abs((o1-o2) * 180/math.pi)
  else:
    return abs((o1-o2) * 180/math.pi)
  
def right_push_up(result_list , movecount, stat, score, keypoint_score_th):
    if (score[13] >=  keypoint_score_th and 
        score[15] >=  keypoint_score_th and
        score[5] >=  keypoint_score_th and
        score[7] >=  keypoint_score_th and
        score[9] >=  keypoint_score_th and
        score[11] >=  keypoint_score_th):
        d = []
        d.append(result_list[13][0]) #x
        d.append(result_list[15][1]) #y
        if (radian(d,result_list[15],result_list[13])<60):
            if (stat[0] == 0) : 
                stat[0] = 1
        else : 
            stat[0] = 0
        if (stat[0] >= 1):
            ra = radian(result_list[5],result_list[7],result_list[9])
            if (ra <= 200 and ra >= 155):
                stat[0] = 2
            elif (stat[0] == 2 and ra <= 150 and radian(result_list[5],result_list[11],result_list[13]) > 145):
                stat[0] = 1
                movecount[0]+=1
                print(movecount[0])
        return False
    else :
        return True

index1 = [[0,1],
          [0,2],
          [1,3],
          [2,4],
          [0,5],
          [0,6],
          [5,6],
          [5,7],
          [7,9],
          [6,8],
          [8,10],
          [11,12],
          [5,11],
          [11,13],
          [13,15],
          [6,12],
          [12,14],
          [14,16]]

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

    mirror = True
    keypoint_score_th = 0.3

    # Video Capture
    cap = cv.VideoCapture(0)

    # Set model
    model_url = "https://tfhub.dev/google/movenet/singlepose/lightning/4"
    input_size = 192

    module = tfhub.load(model_url)
    model = module.signatures['serving_default']

    while True:

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

        debug_image = draw_debug(
            debug_image,
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

#Method to make line
def draw_debug(
    image,
    keypoint_score_th,
    keypoints,
    scores,
):
    debug_image = copy.deepcopy(image)
    for index in index1:
        if scores[index[0]] > keypoint_score_th and scores[
            index[1]] > keypoint_score_th:
            point01 = keypoints[index[0]]
            point02 = keypoints[index[1]]
            cv.line(debug_image, point01, point02, (255, 255, 255), 4)
            cv.line(debug_image, point01, point02, (0, 0, 0), 2)   
    
    # Set Circle
    for keypoint, score in zip(keypoints, scores):
        if score > keypoint_score_th:
            cv.circle(debug_image, keypoint, 6, (255, 255, 255), -1)
            cv.circle(debug_image, keypoint, 3, (0, 0, 0), -1)

    return debug_image

#Run main
if __name__ == '__main__':
    main()