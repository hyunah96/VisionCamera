import datetime
import config
import cv2
from ultralytics import YOLO

def main():
    
    upperModel = YOLO("/Users/giyoma/Desktop/visionCamera/upper/best.pt") #상부
    lowerModel = YOLO("/Users/giyoma/Desktop/visionCamera/lower/best.pt") #하부
    

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("웹캠 열기 실패")
        return

    
# 파일 이름 정의
def fileName():
    print("fileName")
    now = datetime.datetime.now()
    name_str = now.strftime("%Y-%m-%d-%H-%M-%S")
    imageName = config.SAVE_PATH + name_str
    return imageName

# 사진 촬영 
def takePhoto():
    imageName = fileName()
    cv2.imwrite(imageName + ".jpg", frame)