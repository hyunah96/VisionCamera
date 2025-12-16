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
