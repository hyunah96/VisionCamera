from ultralytics import YOLO
import cv2
import pymcprotocol as protocol
import time
import datetime

# 신호끊어주는것!!!
# 신호끊어주는것!!!
# 신호끊어주는것!!!
# 신호끊어주는것!!!
# 신호끊어주는것!!!


# PLC_IP = "192.168.3.10"
# PLC_PORT = 5028

# # 상부 양품 완료 트리거 신호
# DONE_ADDRESS_OK = 'M1550'
# # 상부 불량 완료 트리거 신호
# DONE_ADDRESS_NG = 'M1551'

# # 판정 기준
# OK_CLASSES = ["good"]   # 양품 클래스명
# NG_CLASSES = ["bad"]    # 불량 클래스명

# SAVE_PATH = "/Users/giyoma/Desktop/visionCamera/"





    
# 사진 저장
def picture(frame):
    print("picture")
    imageName = fileName()
    cv2.imwrite(imageName + ".jpg" ,frame)
    
    

# plc 연결
def connect_plc():
    try:
        plc = protocol.Type3E()
        plc.connect(PLC_IP, PLC_PORT)
        print(f"PLC 연결 성공: {PLC_IP}:{PLC_PORT}")
        return plc
    except Exception as ex:
        print("PLC connect 예외:", ex)
        return None

# plc 연결 해제
def disconnect_plc(plc):
    if plc is None:
        return
    try:
        plc.close()
        print("PLC disconnect")
    except Exception as ex:
        print("PLC disconnect 예외:", ex)


def main():
    # 1) YOLO 모델 불러오기
    #model = YOLO("/Users/giyoma/Desktop/visionCamera/upper/best.pt") #상부
    model = YOLO("/Users/giyoma/Desktop/visionCamera/lower/best.pt") #하부
    
    # 2) 웹캠 열기
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("웹캠 열기 실패")
        return

    # 3) PLC 연결
    plc = connect_plc()
    if plc is None:
        cap.release()
        return

    judgment = ""

    #while True:
    #plc 연결되어 있으면  
    while plc is not None:    
        # 카메라 프레임 읽기 
        ret, frame = cap.read()
        if not ret:
            print("카메라 프레임 읽기 실패")
            break

        # ---- YOLO 추론 ----
        results = model(frame)[0]
        judgment = ""  # 초기화

        for box in results.boxes:
            cls = int(box.cls.item())
            class_name = model.names[cls]  # 클래스 이름 (good / bad)
            print("class_name? " ,class_name)

            if class_name in NG_CLASSES:
                judgment = "NG"
            elif class_name in OK_CLASSES:
                judgment = "OK"

            # 바운딩 박스 그리기
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            color = (0, 255, 0) if judgment == "OK" else (0, 0, 255)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(
                frame,
                class_name,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2,
            )

        # 화면 상단에 판정 표시
        color = (0, 255, 0) if judgment == "OK" else (0, 0, 255)
        cv2.putText(
            frame,
            f"JUDGMENT: {judgment}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            color,
            3,
        )

        # ---- 화면 표시 ----
        cv2.imshow("YOLOv8 Realtime Inspection", frame)

        # ---- PLC 신호 읽기 (M550) ----
        try:
            print("plc 신호 읽기")
            # 상부 양불 감지 센서 
            M550 = plc.batchread_bitunits("M550", 1)[0]
            M580 = plc.batchread_bitunits("M580", 1)[0]
            print("M550  읽기", M550)
        except Exception as ex:
            print("PLC M550 read 예외:", ex)
            break

        # 신호 들어오면 사진 촬영 후 루프 종료
        if M550 == 1:
            #cv2.imwrite(SAVE_PATH, frame)
            #print(f"사진 촬영 성공: '{SAVE_PATH}' 파일로 저장되었습니다.")
            print("M550 " , M550)
            picture(frame)
            print(class_name)
            M550 = 0
        
        if M580 == 1:
            print("M580 " , M580)
            picture(frame)
            print(class_name)
            M580 = 0
                

            # 판정 따라 완료 신호
            try:
                if judgment == "OK":
                    plc.batchwrite_bitunits(DONE_ADDRESS_OK, [1])
                    print("DONE_ADDRESS_OK")
                elif judgment == "NG":
                    plc.batchwrite_bitunits(DONE_ADDRESS_NG, [1])
                    print("DONE_ADDRESS_NG")
            except Exception as ex:
                print("완료 신호 쓰기 예외:", ex)
                break

        # ESC 키로 강제 종료 (테스트용)
        if cv2.waitKey(1) & 0xFF == 27:
            print("ESC 입력으로 종료")
            break

        time.sleep(0.05)

    cap.release()
    cv2.destroyAllWindows()
    disconnect_plc(plc)


if __name__ == "__main__":
    main()
