from tcp import tcp

class sender_tcp(tcp):
    def __init__(self, bind, agt, dst):
        tcp.__init__(self, bind)
        self.agt = agt
        self.dst = dst
        self.ack_num = 0

    def send_to_dst(self, msg):
        self.send_pck(msg, self.agt, (self.dst, self.ack_num))
        self.ack_num += 1

    def recv_ack_from_dst(self):
        msg, _, _ = sender.recv_pck()
        ack_type, ack_num = sender.unpack_acks(msg)
        return ack_type, ack_num

agt = ('127.0.0.1', 8782)
dst = ('127.0.0.1', 8781)
sender = sender_tcp(('127.0.0.1', 8780), agt, dst)

for i in range(10):
    sender.send_to_dst(b'Hello, World!')
    ack_type, ack_num = sender.recv_ack_from_dst()
    if ack_type == sender.ACK:
        print('ack:', ack_num)
