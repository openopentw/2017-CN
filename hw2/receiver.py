from udp_tcp import tcp

class receiver_tcp(tcp):
    def __init__(self, bind):
        tcp.__init__(self, bind)

    def recv_from_src(self):
        pck, self.agt, (self.src, pck_idx), (ack_type, _) = self.recv_pck_with_ack()
        return pck, pck_idx, ack_type

    def send_ack_to_src(self, ack_num):
        self.send_pck_with_ack(b'', self.agt, (self.src, 0), self.ACK, ack_num)

    def send_finack_to_src(self):
        self.send_pck_with_ack(b'', self.agt, (self.src, 0), self.FINACK, 0)

receiver = receiver_tcp(('127.0.0.1', 8781))

filetype, pck_idx, _ = receiver.recv_from_src()
print('receive filetype:', filetype)
receiver.send_ack_to_src(pck_idx)

# with open('result.' + filetype.decode(), 'wb') as f:
#     while True:
#         pck, pck_idx, ack_type = receiver.recv_from_src()
#         if ack_type == receiver.NOACK:
#             print('receive pck_idx:', pck_idx)
#             f.write(pck)
#             receiver.send_ack_to_src(pck_idx)
#         elif ack_type == receiver.FIN:
#             print('receive FIN')
#             receiver.send_finack_to_src()
#             break

while True:
    pck, pck_idx, ack_type = receiver.recv_from_src()
    if ack_type == receiver.NOACK:
        print('receive:', pck)
        print('receive pck_idx:', pck_idx)
        receiver.send_ack_to_src(pck_idx)
    elif ack_type == receiver.FIN:
        print('receive FIN')
        receiver.send_finack_to_src()
        break
