import config
import plc
import camera



def main():
    plc = plc.connect()
    # 현재 어떤 웹캠이 우선순위로 잡히는지 모르므로 임의로 숫자 부여함
    upperCamera = camera.openCamera(0)
    lowerCamera = camera.openCamera(1)



    while plc is not None:
        upperRet, upperFrame = upperCamera.read()
        lowerRet, lowerFrame = lowerCamera.read()

        if not upperRet:
            print("상부 카메라 프레임을 읽는데 실패하였습니다")
            break
        if not lowerRet:
            print("하부 카메라 프레임을 읽는데 실패하였습니다")
            break

        upperResults = config.UPPER_MODEL
        lowerResults =  config.LOWER_MODEL


if __name__ == "__main__":
    main()