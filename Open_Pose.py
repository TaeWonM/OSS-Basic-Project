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

#프레임을 처음에 읽고 만약 카메라를 읽을 수 없다면 프로그램 종료하는 부분
hasFrame, frame = capture.read()
if not hasFrame:
    cv2.waitKey()
    exit



#반복문을 통한 카메라 프레임을 계속 불러옴
while cv2.waitKey(1) <0:
    hasFrame, frame = capture.read()
    # 프레임의 크기를 줄여서 연산의 개수를 줄이는 부분 (선택)
    frame=cv2.resize(frame,dsize=(320,240),interpolation=cv2.INTER_AREA)

    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]

    #변수에 프레임을 blob로 형 변환하는 부분
    inpBlob = cv2.dnn.blobFromImage(frame, inputScale, (inputWidth, inputHeight), (0, 0, 0), swapRB=False, crop=False)

    # network에 넣어주기
    net.setInput(inpBlob)

    # 결과 받아오기
    output = net.forward()

    # 신뢰도를 측정하여서 그 관절 포인트가 맞는지 확인하는 부분.
    points = []
    for i in range(0,15):
        # 해당 신체부위 신뢰도 얻음.
        probMap = output[0, i, :, :]
    
        # global 최대값 찾기
        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

        # 원래 이미지에 맞게 점 위치 변경
        x = (frameWidth * point[0]) / output.shape[3]
        y = (frameHeight * point[1]) / output.shape[2]
        # 키포인트 검출한 결과가 0.1보다 크면(검출한곳이 위 BODY_PARTS랑 맞는 부위면) points에 추가, 검출했는데 부위가 없으면 None으로    
        if prob > 0.1 :    
            cv2.circle(frame, (int(x), int(y)), 3, (0, 255, 255), thickness=-1, lineType=cv2.FILLED) # circle(그릴곳, 원의 중심, 반지름, 색)
            cv2.putText(frame, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, lineType=cv2.LINE_AA)
            points.append((int(x), int(y)))
        else :
            points.append(None)
    
    
    # 각 POSE_PAIRS별로 선 그어줌 (머리 - 목, 목 - 왼쪽어깨, ...)
    for pair in POSE_PAIRS:
        partA = pair[0]             # Head
        partA = BODY_PARTS[partA]   # 0
        partB = pair[1]             # Neck
        partB = BODY_PARTS[partB]   # 1
        
        #partA와 partB 사이에 선을 그어줌 (cv2.line)
        if points[partA] and points[partB]:
            cv2.line(frame, points[partA], points[partB], (0, 255, 0), 2)

    cv2.imshow("Output-Keypoints",frame)
 
capture.release()  #카메라 장치에서 받아온 메모리 해제
cv2.destroyAllWindows() #모든 윈도우 창 닫음