import config
import plc
import camera
import cv2
import time



def main():
    #plc = plc.connect()
    # 현재 어떤 웹캠이 우선순위로 잡히는지 모르므로 임의로 숫자 부여함
    upperCamera = camera.openCamera(1)
    lowerCamera = camera.openCamera(0)
    #camera.findCamera()



    #while plc is not None:
    while True:
        upperRet, upperFrame = upperCamera.read()
        lowerRet, lowerFrame = lowerCamera.read()

        if not upperRet:
            print("상부 카메라 프레임을 읽는데 실패하였습니다")
            break
        if not lowerRet:
            print("하부 카메라 프레임을 읽는데 실패하였습니다")
            break

        upperResults = config.UPPER_MODEL(upperFrame)[0]
        lowerResults =  config.LOWER_MODEL(lowerFrame)[0]
        
        for upperBox in upperResults.boxes:
            upperCls = int(upperBox.cls.item())
            class_name = config.UPPER_MODEL.names[upperCls]
            print("upper class_name? " , class_name)
            time.sleep(1)
            
            
              # 바운딩 박스 그리기
            x1, y1, x2, y2 = map(int, upperBox.xyxy[0])
            color = (0, 255, 0)
            cv2.rectangle(upperFrame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(
                upperFrame,
                class_name,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2,
            )
            
            
            #cv2.imshow("upperFrame!!!", upperFrame)
            
        for lowerBox in lowerResults.boxes:
            lowerCls = int(lowerBox.cls.item())
            class_name = config.LOWER_MODEL.names[lowerCls]
            print("lower class_name? " , class_name)
            time.sleep(1)
            
            
              # 바운딩 박스 그리기
            x1, y1, x2, y2 = map(int, lowerBox.xyxy[0])
            color = (0, 255, 0)
            cv2.rectangle(lowerFrame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(
                lowerFrame,
                class_name,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2,
            )
            
            
            cv2.imshow("lowerFrame!!!", lowerFrame)

            
            


if __name__ == "__main__":
    main()