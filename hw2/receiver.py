from tcp import tcp

class receiver_tcp(tcp):
    def __init__(self, bind):
        tcp.__init__(self, bind)

    def recv_from_src(self):
        msg, self.agt, (self.src, pck_idx) = self.recv_pck()
        return msg, pck_idx

    def send_ack_to_src(self, ack_num):
        msg = self.pack_acks(self.ACK, ack_num)
        self.send_pck(msg, self.agt, (self.src, 0))

receiver = receiver_tcp(('127.0.0.1', 8781))

while True:
    msg, pck_idx = receiver.recv_from_src()
    print('receive:', msg)
    receiver.send_ack_to_src(pck_idx)
