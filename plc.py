import config
import pymcprotocol as protocol
import camera


def __init__(self):
    self.plc = protocol.Type3E()
    self.ip = config.PLC_IP
    self.port = config.PLC_PORT

def connect(self):
    try:
        self.plc.connect(self.ip, self.port)
        print("PLC 연결")
        return self.plc
    except Exception as ex:
        print("PLC 연결에서 오류가 발생하였습니다", ex)
        return None 

def disconnect(self):
    try:
        self.plc.close()
        print("PLC 연결 해제")
    except Exception as ex:
        print("PLC 연결 해제에서 오류가 발생하였습니다 ", ex)

# PLC 읽기 (개선 전)
def read_loop(self):
    print("read_loop")
    while self.plc.connect:
        M550 = self.plc.batchread_bitunits("M550",1)[0]
        if M550 == 1:
            camera.takePhoto()
            M550 = 0
            self.plc.batchread_bitunits(config.DONE_ADDRESS_OK,[1])
        
