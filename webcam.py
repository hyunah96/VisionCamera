# opencv import
import cv2

# openCV VideoCapture 객체 생성
# 인수 0번째는 첫번째 웹캠 (PC에 여러 개의 웹캠이 연결되어 있을 수 있기 때문)
webcam = cv2.VideoCapture(0)

# 웹캠이 제대로 연결되어 있는지 확인 제대로 연결되어 있다면 webcam.isOpened() 값이 True
# 웹캠이 연결되어 있지 않다면 코드 수행하지 않고 exit() 
if not webcam.isOpened():
    exit()

# 웹캠이 제대로 연결되어 있는 동안 반복 
# 웹캠으로 촬영되는 영상을 webcam.read()를 통해 읽음
# cv2.imshow()를 통해 test라는 창에 캡쳐된 프레임을 보여줌
while webcam.isOpened():
    status, frame = webcam.read()

    if status:
        cv2.imshow("test", frame)

    # q 를 입력하면 반복문 탈출 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# webcam 연결 종료
webcam.release()
# 창 닫음
cv2.destroyAllWindows()