# Import할 라이브러리들
import cv2
from pathlib import Path

# MPII에서 각 파트 번호, 선으로 연결될 POSE_PAIRS
BODY_PARTS = { "Head": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "Chest": 14,
                "Background": 15 }

POSE_PAIRS = [ ["Head", "Neck"], ["Neck", "RShoulder"], ["RShoulder", "RElbow"],
                ["RElbow", "RWrist"], ["Neck", "LShoulder"], ["LShoulder", "LElbow"],
                ["LElbow", "LWrist"], ["Neck", "Chest"], ["Chest", "RHip"], ["RHip", "RKnee"],
                ["RKnee", "RAnkle"], ["Chest", "LHip"], ["LHip", "LKnee"], ["LKnee", "LAnkle"] ]

# 각 파일 path
BASE_DIR=Path(__file__).resolve().parent
protoFile = str(BASE_DIR)+"/model/pose_deploy_linevec_faster_4_stages.prototxt"
weightsFile = str(BASE_DIR)+"/model/pose_iter_160000.caffemodel"

# 카메라, 모델, 입력 크기 설정
net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

capture = cv2.VideoCapture(0)

inputWidth=320
inputHeight=240
inputScale=1.0/255


#반복문을 통한 카메라 프레임을 계속 불러옴
while cv2.waitKey(1) <0:
    hasFrame, frame = capture.read()
    # 프레임의 크기를 줄여서 연산의 개수를 줄이는 부분 (선택)
    frame=cv2.resize(frame,dsize=(320,240),interpolation=cv2.INTER_AREA)
    
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]
