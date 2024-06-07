# pip install tensorflow
# pip install tensorflow_hub

import copy
import math
import cv2 as cv
import numpy as np
import tensorflow as tf
import tensorflow_hub as tfhub
import pyautogui
import threading
import time


class Movenet:
    def __init__(self):
        self.status = [0]
        self.movecount = [0]
        self.index1 = [
            [0, 1],
            [0, 2],
            [1, 3],
            [2, 4],
            [0, 5],
            [0, 6],
            [5, 6],
            [5, 7],
            [7, 9],
            [6, 8],
            [8, 10],
            [11, 12],
            [5, 11],
            [11, 13],
            [13, 15],
            [6, 12],
            [12, 14],
            [14, 16],
        ]
        self.danger_massage = [False, False, False]
        self.danger_massage_flag = [False, False, False]
        self.kill_thread = False
        self.attack_flag = False

    def radian(self, one, center, two):
        o1 = math.atan2((two[1] - center[1]), (two[0] - center[0]))
        o2 = math.atan2((one[1] - center[1]), (one[0] - center[0]))
        if abs((o1 - o2) * 180 / math.pi) >= 180:
            return 360 - abs((o1 - o2) * 180 / math.pi)
        else:
            return abs((o1 - o2) * 180 / math.pi)

    def right_push_up(self, result_list, movecount, stat, score, keypoint_score_th):
        if (
            score[13] >= keypoint_score_th
            and score[15] >= keypoint_score_th
            and score[5] >= keypoint_score_th
            and score[7] >= keypoint_score_th
            and score[9] >= keypoint_score_th
            and score[11] >= keypoint_score_th
        ):
            d = []
            d.append(result_list[13][0])  # x
            d.append(result_list[15][1])  # y
            if self.radian(d, result_list[15], result_list[13]) < 60:
                if stat[0] == 0:
                    stat[0] = 1
            else:
                stat[0] = 0
            if stat[0] >= 1:
                ra = self.radian(result_list[5], result_list[7], result_list[9])
                if ra <= 200 and ra >= 155:
                    stat[0] = 2
                    if self.danger_massage[2] == False:
                        self.danger_massage_flag[2] = False
                        thread1 = threading.Thread(
                            target=self.message_box,
                            args=[
                                "Arms are not totaly set",
                                2,
                            ],
                            daemon=True,
                        )
                        thread1.start()
                        self.danger_massage[2] = True
                elif stat[0] == 2 and ra <= 150:
                    if (
                        self.radian(result_list[5], result_list[11], result_list[13])
                        > 145
                    ):
                        self.danger_massage_flag[2] = True
                        stat[0] = 1
                        movecount[0] += 1
                        self.attack_flag = True
                    elif self.danger_massage[2] == False:
                        self.danger_massage_flag[2] = False
                        thread1 = threading.Thread(
                            target=self.message_box,
                            args=[
                                "legs are not totaly set",
                                2,
                            ],
                            daemon=True,
                        )
                        thread1.start()
                        self.danger_massage[2] = True
            return False
        else:
            return True

    def left_push_up(self, result_list, movecount, stat, score, keypoint_score_th):
        if (
            score[14] >= keypoint_score_th
            and score[16] >= keypoint_score_th
            and score[6] >= keypoint_score_th
            and score[8] >= keypoint_score_th
            and score[10] >= keypoint_score_th
            and score[12] >= keypoint_score_th
        ):
            d = []
            d.append(result_list[14][0])  # x
            d.append(result_list[16][1])  # y
            if self.radian(d, result_list[16], result_list[14]) < 60:
                if stat[0] == 0:
                    stat[0] = 1
            else:
                stat[0] = 0
            if stat[0] >= 1:
                ra = self.radian(result_list[6], result_list[8], result_list[10])
                if ra <= 200 and ra >= 155:
                    stat[0] = 2
                    if self.danger_massage[2] == False:
                        self.danger_massage_flag[2] = False
                        thread1 = threading.Thread(
                            target=self.message_box,
                            args=[
                                "Arms are not totaly set",
                                2,
                            ],
                            daemon=True,
                        )
                        thread1.start()
                        self.danger_massage[2] = True
                elif stat[0] == 2 and ra <= 150:
                    self.danger_massage_flag[2] = True
                    if (
                        self.radian(result_list[6], result_list[12], result_list[14])
                        > 145
                    ):
                        self.danger_massage_flag[2] = True
                        stat[0] = 1
                        movecount[0] += 1
                        self.attack_flag = True
                    elif self.danger_massage[2] == False:
                        self.danger_massage_flag[2] = False
                        thread1 = threading.Thread(
                            target=self.message_box,
                            args=[
                                "legs are not totaly set",
                                2,
                            ],
                            daemon=True,
                        )
                        thread1.start()
                        self.danger_massage[2] = True
            return False
        else:
            return True

    def right_sqaut(self, result_list, movecount, stat, score, keypoint_score_th):
        if (
            score[14] >= keypoint_score_th
            and score[16] >= keypoint_score_th
            and score[12] >= keypoint_score_th
        ):
            d = []
            d.append(result_list[14][0])
            d.append(result_list[16][1])
            if self.radian(d, result_list[16], result_list[14]) > 45:
                if stat[0] == 0:
                    stat[0] = 1
            else:
                stat[0] = 0
            if stat[0] >= 1:
                ra = self.radian(result_list[12], result_list[14], result_list[16])
                if ra >= 145:
                    stat[0] = 2
                elif stat[0] == 2 and ra <= 120:
                    self.danger_massage_flag[2] = True
                    stat[0] = 1
                    movecount[0] += 1
                    self.attack_flag = True
                elif stat[0] == 2 and self.danger_massage[2] == False:
                    self.danger_massage_flag[2] = False
                    thread1 = threading.Thread(
                        target=self.message_box,
                        args=[
                            "legs are not totaly set",
                            2,
                        ],
                        daemon=True,
                    )
                    thread1.start()
                    self.danger_massage[2] = True
            return False
        else:
            return True

    def left_sqaut(self, result_list, movecount, stat, score, keypoint_score_th):
        if (
            score[13] >= keypoint_score_th
            and score[15] >= keypoint_score_th
            and score[11] >= keypoint_score_th
        ):
            d = []
            d.append(result_list[13][0])
            d.append(result_list[15][1])
            if self.radian(d, result_list[15], result_list[13]) > 45:
                if stat[0] == 0:
                    stat[0] = 1
                else:
                    stat[0] = 0
            if stat[0] >= 1:
                ra = self.radian(result_list[11], result_list[13], result_list[15])
                if ra >= 145:
                    stat[0] = 2
                elif stat[0] == 2 and ra <= 120:
                    self.danger_massage_flag[2] = True
                    stat[0] = 1
                    movecount[0] += 1
                    self.attack_flag = True
                elif stat[0] == 2 and self.danger_massage[2] == False:
                    self.danger_massage_flag[2] = False
                    thread1 = threading.Thread(
                        target=self.message_box,
                        args=[
                            "legs are not totaly set",
                            2,
                        ],
                        daemon=True,
                    )
                    thread1.start()
                    self.danger_massage[2] = True
            return False
        else:
            return True

    # Method to run models
    def run_inference(self, model, input_size, image):
        image_width, image_height = image.shape[1], image.shape[0]

        input_image = cv.resize(
            image, dsize=(input_size, input_size)
        )  # Revert size in WebCam
        input_image = cv.cvtColor(input_image, cv.COLOR_BGR2RGB)  # Set image_color
        input_image = input_image.reshape(
            -1, input_size, input_size, 3
        )  # reshape size in input_image
        input_image = tf.cast(input_image, dtype=tf.int32)

        outputs = model(input_image)  # run models

        keypoints_with_scores = outputs["output_0"].numpy()
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

    # main Method
    def run(self, pose_num):

        mirror = True
        keypoint_score_th = 0.3

        # Video Capture
        cap = cv.VideoCapture(0)

        # Set model
        model_url = "https://tfhub.dev/google/movenet/singlepose/lightning/4"
        input_size = 192

        module = tfhub.load(model_url)
        model = module.signatures["serving_default"]

        while True:

            ret, frame = cap.read()
            if not ret:
                break
            if mirror:
                frame = cv.flip(frame, 1)
            debug_image = copy.deepcopy(frame)

            keypoints, scores = self.run_inference(
                model,
                input_size,
                frame,
            )

            debug_image = self.draw_debug(
                debug_image,
                keypoint_score_th,
                keypoints,
                scores,
            )
            if pose_num == 0:
                if self.right_push_up(
                    keypoints, self.movecount, self.status, scores, keypoint_score_th
                ) and self.left_push_up(
                    keypoints, self.movecount, self.status, scores, keypoint_score_th
                ):
                    if self.danger_massage[1] == False:
                        self.danger_massage_flag[1] = False
                        thread1 = threading.Thread(
                            target=self.message_box,
                            args=[
                                "Necessary poses to detect push_up are not detected",
                                1,
                            ],
                            daemon=True,
                        )
                        thread1.start()
                        self.danger_massage[1] = True
                else:
                    self.danger_massage_flag[1] = True
            if pose_num == 1:
                if self.right_sqaut(
                    keypoints, self.movecount, self.status, scores, keypoint_score_th
                ) and self.left_sqaut(
                    keypoints, self.movecount, self.status, scores, keypoint_score_th
                ):
                    if self.danger_massage[1] == False:
                        self.danger_massage_flag[1] = False
                        thread1 = threading.Thread(
                            target=self.message_box,
                            args=[
                                "Necessary poses to detect sqaut are not detected",
                                1,
                            ],
                            daemon=True,
                        )
                        thread1.start()
                        self.danger_massage[1] = True
                else:
                    self.danger_massage_flag[1] = True

            if cv.waitKey(1) == 27 or self.kill_thread:  # ESC
                cv.destroyAllWindows()
                break

            cv.imshow("MoveNet", debug_image)

        cap.release()
        cv.destroyAllWindows()

    # Method to make line
    def draw_debug(
        self,
        image,
        keypoint_score_th,
        keypoints,
        scores,
    ):
        debug_image = copy.deepcopy(image)
        for index in self.index1:
            if (
                scores[index[0]] > keypoint_score_th
                and scores[index[1]] > keypoint_score_th
            ):
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

    def message_box(self, text, massages_flag):
        thread2 = threading.Thread(
            target=self.alert_message, args=[text, massages_flag], daemon=True
        )
        thread2.start()
        while self.danger_massage_flag[massages_flag] == False:
            time.sleep(1)
        if thread2.is_alive():
            pyautogui.press("enter")
        self.danger_massage[massages_flag] = False

    def alert_message(self, text, massages_flag):
        pyautogui.alert(text)
        self.danger_massage_flag[massages_flag] = True
