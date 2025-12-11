import datetime
import config
import cv2

# 카메라 실행
def openCamera(index=0):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("웹캠을 여는데 실패하였습니다")
        return None
    return cap
    
      
    
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