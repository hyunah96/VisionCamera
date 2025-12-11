from ultralytics import YOLO
import cv2
import pymcprotocol as protocol
import time
import datetime
import config

# 신호끊어주는것!!!
# 신호끊어주는것!!!
# 신호끊어주는것!!!
# 신호끊어주는것!!!
# 신호끊어주는것!!!

def main():
    # YOLO 모델
    


        # ---- YOLO 추론 ----
        # yolo 이미지 추론 결과
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
