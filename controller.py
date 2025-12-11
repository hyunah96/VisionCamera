import pymcprotocol as protocol
PLC_IP = "192.168.3.10"
PLC_PORT = 5028

# 상부 양품 완료 트리거 신호
DONE_ADDRESS_OK = 'M1500'
# 상부 불량 완료 트리거 신호
DONE_ADDRESS_NG = 'M1501'
class PLCController:

    def __init__(self):
        self.plc = protocol.Type3E()
        self.ip = PLC_IP
        self.port = PLC_PORT

    
    def connect(self):
        try:
            self.plc.connect(self.ip, self.port)
            print("PLC 연결 성공")
            return True
        except Exception as ex:
            print("connect 예외", ex)
            return False 

    def disconnect(self):
        try:
            self.plc.close()
            print("disconnect")
        except Exception as ex:
            print("disconnect 예외", ex)

    def read_loop(self):
        print("read_loop")
        while self.plc.connect:
            #M200 = self.plc.batchread_bitunits("M200", 1)[0]
            M550 = self.plc.batchread_bitunits("M550",1)[0]
            if M550 == 1:
                run.picture()
                M550 = 0
                self.plc.batchread_bitunits(DONE_ADDRESS_OK,[1])
            
    
            
        