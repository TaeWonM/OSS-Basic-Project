# pip install mediapipe
# define imports and settings
import cv2
import math
import mediapipe as mp
import pyautogui
import threading
import time


class MediaPipe:

    def __init__(self):
        self.status = [0]
        self.movecount = [0]
        self.danger_massage = [False, False, False]
        self.danger_massage_flag = [False, False, False]
        self.attack_flag = False

    def setdict(self, result, image, danger_massage):
        l = []
        image_height, image_width, _ = image
        try:
            for k in range(0, 33):
                d = {}
                if result.pose_landmarks.landmark[k].visibility >= 0.5:
                    x = result.pose_landmarks.landmark[k].x * image_width
                    y = result.pose_landmarks.landmark[k].y * image_height
                    d["num"] = k
                    d["x"] = x
                    d["y"] = y
                l.append(d)
            self.danger_massage_flag[0] = True
        except:
            if danger_massage[0] == False:
                self.danger_massage_flag[0] = False
                thread1 = threading.Thread(
                    target=self.message_box,
                    args=["None of poses are not detected", 0],
                    daemon=True,
                )
                thread1.start()
                self.danger_massage[0] = True
        return l

    def radian(self, one, center, two):
        o1 = math.atan2((two["y"] - center["y"]), (two["x"] - center["x"]))
        o2 = math.atan2((one["y"] - center["y"]), (one["x"] - center["x"]))
        if abs((o1 - o2) * 180 / math.pi) >= 180:
            return 360 - abs((o1 - o2) * 180 / math.pi)
        else:
            return abs((o1 - o2) * 180 / math.pi)

    def right_push_up(self, result_list, movecount, stat):
        try:
            d = {}
            d["x"] = result_list[27]["x"]
            d["y"] = result_list[25]["y"]
            if self.radian(d, result_list[25], result_list[27]) < 60:
                if stat[0] == 0:
                    stat[0] = 1
            else:
                stat[0] = 0
            if stat[0] >= 1:
                ra = self.radian(result_list[11], result_list[13], result_list[15])
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
                elif stat[0] == 2 and ra <= 130:
                    self.danger_massage_flag[2] = True
                    if (
                        self.radian(result_list[11], result_list[23], result_list[25])
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
        except:
            return True

    def left_push_up(self, result_list, movecount, stat):
        try:
            d = {}
            d["x"] = result_list[28]["x"]
            d["y"] = result_list[26]["y"]
            if self.radian(d, result_list[26], result_list[28]) < 60:
                if stat[0] == 0:
                    stat[0] = 1
            else:
                stat[0] = 0
            if stat[0] >= 1:
                ra = self.radian(result_list[12], result_list[14], result_list[16])
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
                elif stat[0] == 2 and ra <= 130:
                    self.danger_massage_flag[2] = True
                    if (
                        self.radian(result_list[12], result_list[24], result_list[26])
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
        except:
            return True

    def right_sqaut(self, result_list, movecount, stat):
        try:
            d = {}
            d["x"] = result_list[26]["x"]
            d["y"] = result_list[28]["y"]
            if self.radian(d, result_list[28], result_list[26]) > 45:
                if stat[0] == 0:
                    stat[0] = 1
            else:
                stat[0] = 0
            if stat[0] >= 1:
                ra = self.radian(result_list[24], result_list[26], result_list[28])
                if ra >= 145:
                    stat[0] = 2
                elif stat[0] == 2 and ra <= 110:
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
        except:
            return True

    def left_sqaut(self, result_list, movecount, stat):
        try:
            d = {}
            d["x"] = result_list[25]["x"]
            d["y"] = result_list[27]["y"]
            if self.radian(d, result_list[27], result_list[25]) > 45:
                if stat[0] == 0:
                    stat[0] = 1
            else:
                stat[0] = 0
            if stat[0] >= 1:
                ra = self.radian(result_list[23], result_list[25], result_list[27])
                if ra >= 145:
                    stat[0] = 2
                elif stat[0] == 2 and ra <= 110:
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
        except:
            return True

    def run(self, pose_num):
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_pose = mp.solutions.pose
        cap = cv2.VideoCapture(0)
        with mp_pose.Pose(
            min_detection_confidence=0.5, min_tracking_confidence=0.5
        ) as pose:
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    continue
                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = pose.process(image)
                # Draw the pose annotation on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style(),
                )
                result_list = self.setdict(results, image.shape, self.danger_massage)
                if pose_num == 0:
                    if self.right_push_up(
                        result_list, self.movecount, self.status
                    ) and self.left_push_up(result_list, self.movecount, self.status):
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
                        result_list, self.movecount, self.status
                    ) and self.left_sqaut(result_list, self.movecount, self.status):
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
                # Flip the image horizontally for a selfie-view display.
                cv2.imshow("MediaPipe Pose", cv2.flip(image, 1))
                if cv2.waitKey(1) & 0xFF == 27:
                    for i in range(0, 3):
                        self.danger_massage_flag[i] = True
                    cv2.destroyAllWindows()
                    break
        cap.release()

    def message_box(self, text, massages_flag):
        thread2 = threading.Thread(
            target=self.alert_message, args=[text, massages_flag], daemon=True
        )
        thread2.start()
        while self.danger_massage_flag[massages_flag] == False:
            time.sleep(1)
        while thread2.is_alive():
            pyautogui.press("enter")
        self.danger_massage[massages_flag] = False

    def alert_message(self, text, massages_flag):
        pyautogui.alert(text)
        self.danger_massage_flag[massages_flag] = True
