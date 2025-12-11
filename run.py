from ultralytics import YOLO
import cv2
import pymcprotocol as protocol
import time

PLC_IP = "192.168.3.10"
PLC_PORT = 5028

# 상부 양품 완료 트리거 신호
DONE_ADDRESS_OK = 'M1550'
# 상부 불량 완료 트리거 신호
DONE_ADDRESS_NG = 'M1551'

# 판정 기준
OK_CLASSES = ["good"]          # 양품 클래스명
NG_CLASSES = ["bad", "defect"] # 불량 클래스명

SAVE_PATH = "/Users/giyoma/Desktop/visionCamera/capture.jpg"


def connect_plc():
    """PLC 연결 후 객체 리턴"""
    try:
        plc = protocol.Type3E()
        plc.connect(PLC_IP, PLC_PORT)
        print(f"PLC 연결 성공: {PLC_IP}:{PLC_PORT}")
        return plc
    except Exception as ex:
        print("PLC connect 예외:", ex)
        return None


def disconnect_plc(plc):
    """PLC 연결 종료"""
    if plc is None:
        return
    try:
        plc.close()
        print("PLC disconnect")
    except Exception as ex:
        print("PLC disconnect 예외:", ex)


def main():
    # 1) YOLO 모델 불러오기
    model = YOLO("/Users/giyoma/Desktop/visionCamera/runs/detect/train7/weights/best.pt")

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

    print("PLC 신호 대기 시작 (M550 == 1 이면 사진 촬영 후 종료)")

    judgment = ""

    while True:
        # ---- 카메라 프레임 읽기 ----
        ret, frame = cap.read()
        if not ret:
            print("카메라 프레임 읽기 실패")
            break

        # ---- YOLO 추론 ----
        results = model(frame)[0]
        judgment = ""  # 초기화

        for box in results.boxes:
            cls = int(box.cls.item())
            class_name = model.names[cls]  # 클래스 이름 (good / bad / defect 등)

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
            M550 = plc.batchread_bitunits("M550", 1)[0]
        except Exception as ex:
            print("PLC M550 read 예외:", ex)
            break

        # 신호 들어오면 사진 촬영 후 루프 종료
        if M550 == 1:
            cv2.imwrite(SAVE_PATH, frame)
            print(f"사진 촬영 성공: '{SAVE_PATH}' 파일로 저장되었습니다.")

            # 판정 따라 완료 신호 쏴주고 싶으면 여기서 처리
            try:
                if judgment == "OK":
                    plc.batchwrite_bitunits(DONE_ADDRESS_OK, [1])
                    print("DONE_ADDRESS_OK ON")
                elif judgment == "NG":
                    plc.batchwrite_bitunits(DONE_ADDRESS_NG, [1])
                    print("DONE_ADDRESS_NG ON")
            except Exception as ex:
                print("완료 신호 쓰기 예외:", ex)

            # 무한루프 종료
            break

        # ESC 키로 강제 종료 (테스트용)
        if cv2.waitKey(1) & 0xFF == 27:
            print("ESC 입력으로 종료")
            break

        # PLC 폴링 너무 빠르지 않게 살짝 딜레이
        time.sleep(0.01)

    # 자원 정리
    cap.release()
    cv2.destroyAllWindows()
    disconnect_plc(plc)


if __name__ == "__main__":
    main()
