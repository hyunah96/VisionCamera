import config
import plc
import camera
import cv2
import time
import threading



def main():
    #plc = plc.connect()
    # 현재 어떤 웹캠이 우선순위로 잡히는지 모르므로 임의로 숫자 부여함
    #camera.findCamera()

    plcClient = plc.PLCClient()

    plcClient.connect()

    upperEvent = threading.Event()
    lowerEvent = threading.Event()

    t = threading.Thread(
    target=plcClient.read_loop,
    args=(upperEvent, lowerEvent),

)
    t.start()

    upperCamera = camera.openCamera(0)
    lowerCamera = camera.openCamera(1)

    

    while plcClient.connected:
        upperRet, upperFrame = upperCamera.read()
        lowerRet, lowerFrame = lowerCamera.read()

        if not upperRet:
            print("상부 카메라 프레임을 읽는데 오류가 발생")
            break

        if not lowerRet:
            print("하부 카메라 프레임을 읽는데 오류가 발생")
            break

        # if not upperRet or lowerRet:
        #     print("상부 또는 하부 카메라 프레임을 읽는데 오류가 발생")
        #     break

        try:
            if lowerRet:
                upperResults = config.UPPER_MODEL(upperFrame, verbose=False)[0]
                lowerResults = config.LOWER_MODEL(lowerFrame, verbose=False)[0]

                
                for upperBox in upperResults.boxes:
                    upperCls = int(upperBox.cls.item())
                    upper_class_name = config.UPPER_MODEL.names[upperCls]
                    #print("upper_class_name? " ,upper_class_name)
                    # 바운딩 박스 그리기
                    x1, y1, x2, y2 = map(int, upperBox.xyxy[0])
                    color = (0, 255, 0)
                    cv2.rectangle(upperFrame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(
                        upperFrame,
                        upper_class_name,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        color,
                        2,
                    )
                    
                for lowerBox in lowerResults.boxes:
                    lowerCls = int(lowerBox.cls.item())
                    lower_class_name = config.LOWER_MODEL.names[lowerCls]
                    #print("lower class_name? " , lower_class_name)

                    # 바운딩 박스 그리기
                    x1, y1, x2, y2 = map(int, lowerBox.xyxy[0])
                    color = (0, 255, 0)
                    cv2.rectangle(lowerFrame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(
                        lowerFrame,
                        lower_class_name,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        color,
                        2,
                    )
                        
            cv2.imshow("상부 화면", upperFrame)
            cv2.imshow("하부 화면", lowerFrame)

            if upperEvent.is_set():
                upperEvent.clear()
                snap = upperFrame.copy()
                result = config.UPPER_MODEL(snap, verbose=False)[0]

                if len(result.boxes) == 0:
                    print("객체 감지 없는 상태")
                else:
                    last_box = result.boxes[-1]
                    cls_id = int(last_box.cls.item())
                    name = config.UPPER_MODEL.names[cls_id]   # upper_ng, upper_ok
                    nameLower = name.lower() # 소문자 변환
                    print("상부 결과값 ", nameLower)

                    if "ng" in nameLower:
                        plcClient.writeBit(config.UPPER_DONE_ADDRESS_NG, 1)  # M1551
                        print("상부 NG 처리")
                        camera.takePicture(snap,name)
                    elif "ok" in nameLower:
                        plcClient.writeBit(config.UPPER_DONE_ADDRESS_OK, 1)  # M1550
                        print("상부 OK 처리")
                        camera.takePicture(snap,name)



            if lowerEvent.is_set():
                lowerEvent.clear()
                snap = lowerFrame.copy()
                result = config.LOWER_MODEL(snap, verbose=False)[0]

                if len(result.boxes) == 0:
                    print("객체 감지 없는 상태")
                    
                else:
                    last_box = result.boxes[-1]
                    cls_id = int(last_box.cls.item())
                    name = config.LOWER_MODEL.names[cls_id]     #lower_ng, lower_ok
                    nameLower = name.lower() # 소문자 변환
                    print("하부 결과값 ", nameLower)

                    if "ng" in nameLower:
                        plcClient.writeBit(config.LOWER_DONE_ADDRESS_NG, 1)  # M1581
                        print("하부 NG 처리")
                        camera.takePicture(snap,name)
                    elif "ok" in nameLower:
                        plcClient.writeBit(config.LOWER_DONE_ADDRESS_OK, 1)  # M1580
                        print("하부 OK 처리")
                        camera.takePicture(snap,name)
                

            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except Exception as ex:
            print("에러 " ,ex)
            return
    lowerCamera.release()
    upperCamera.release()

    cv2.destroyAllWindows()

                


if __name__ == "__main__":
    main()