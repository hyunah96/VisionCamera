import datetime
import config
import cv2

# 카메라 실행
def openCamera(index):
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print("웹캠을 여는데 실패하였습니다")
        return None
    if cap.isOpened():
        print("웹캠 index ? " ,cap)
        return cap
    
def findCamera():
    max = 10
    for i in range(max):
        cap = cv2.VideoCapture(i)  
        if cap.isOpened():
            print(f"카메라 연결 {i}")
                
        if not cap.isOpened():
            print(f"카메라 연결 안된 곳 {i}")
# 파일 이름
def fileName():
    print("fileName")
    now = datetime.datetime.now()
    name_str = now.strftime("%Y-%m-%d-%H-%M-%S")
    imageName = config.SAVE_PATH + name_str
    return imageName

# 사진 촬영 
def takePhoto(frame):
    imageName = fileName()
    cv2.imwrite(imageName + ".jpg", frame)