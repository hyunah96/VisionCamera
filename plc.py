import config
import pymcprotocol as protocol
import camera
import time

#M580 하부카메라 사진 촬영 요청 양품 1580 불량 1581


class PLCClient:
    def __init__(self, ip=config.PLC_IP, port=config.PLC_PORT):
        self.plc = protocol.Type3E()
        self.ip = ip
        self.port = port
        self.connected = False

    def connect(self):
        try:
            self.plc.connect(self.ip, self.port)
            print("PLC 연결 성공")
            self.connected = True
            return True
        except Exception as ex:
            print("PLC 연결에서 오류가 발생하였습니다", ex)
            self.connected = False
            return False

    def disconnect(self):
        try:
            self.plc.close()
            print("PLC 연결 해제")
        except Exception as ex:
            print("PLC 연결 해제에서 오류가 발생하였습니다 ", ex)
            self.connected = False

    # PLC에게 비트 신호 전송
    def writeBit(self, addr:str, value:int):
        self.plc.batchwrite_bitunits(addr,[value])


    # PLC 읽기 (개선 전)
    def read_loop(self, upperEvent, lowerEvent):
        print("read_loop")
        while self.plc.connect:
            # 상부 양불 감지 센서 
            M550 = self.plc.batchread_bitunits("M550",1)[0]
            M580 = self.plc.batchread_bitunits("M580",1)[0]

            if M550 == 1:
                #camera.takePicture()
                upperEvent.set()
                M550 = 0
                time.sleep(1)

                
            if M580 == 1:
                lowerEvent.set()
                M580 = 0 
                time.sleep(1)

            
