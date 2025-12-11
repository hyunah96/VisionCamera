import config
import pymcprotocol as protocol

class PLCController:

    def __init__(self):
        self.plc = protocol.Type3E()
        self.ip = config.PLC_IP
        self.port = config.PLC_PORT
    
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
            M550 = self.plc.batchread_bitunits("M550",1)[0]
            if M550 == 1:
                run.picture()
                M550 = 0
                self.plc.batchread_bitunits(DONE_ADDRESS_OK,[1])
            
    
            
        