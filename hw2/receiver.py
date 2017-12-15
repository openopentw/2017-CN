from udp_tcp import tcp

class receiver_tcp(tcp):
    def __init__(self, bind):
        tcp.__init__(self, bind)
        self.default_wndw_sze = 32

    def recv_data(self):
        self.data = b''
        self.wndw = b''

        self.ack_idx = -1
        self.wndw_sze = self.default_wndw_sze
        self.wndw_beg = 0

        # filetype, ack_idx, _ = self.recv_from_src()
        # print('receive filetype:', filetype)
        # self.send_ack_to_src(ack_idx)

        while True:
            pck, ack_idx, ack_type = self.recv_from_src()
            if ack_type == self.NOACK:
                if ack_idx > self.wndw_beg + self.wndw_sze:
                    print('drop\tdata\t#{}'.format(ack_idx))
                    self.flush_wndw()
                    self.send_ack_to_src()
                else:
                    if ack_idx == self.ack_idx + 1:
                        print('recv\tdata\t#{}'.format(ack_idx))
                        self.wndw += pck
                        self.ack_idx = ack_idx
                    else:
                        print('drop\tdata\t#{}'.format(ack_idx))
                    self.send_ack_to_src()
            elif ack_type == self.FIN:
                print('recv\tfin')
                self.flush_wndw()
                self.send_finack_to_src()
                break

    def flush_wndw(self):
        # TODO: write data outside
        self.data += self.wndw
        self.wndw = b''
        self.wndw_beg = self.ack_idx

    def recv_from_src(self):
        pck, self.agt, (self.src, ack_idx), (ack_type, _) = self.recv_pck_with_ack()
        return pck, ack_idx, ack_type

    def send_ack_to_src(self):
        print('send\tack\t#{}'.format(self.ack_idx))
        self.send_pck_with_ack(b'', self.agt, (self.src, 0), self.ACK, self.ack_idx)

    def send_finack_to_src(self):
        print('send\tfinack')
        self.send_pck_with_ack(b'', self.agt, (self.src, 0), self.FINACK, 0)

receiver = receiver_tcp(('127.0.0.1', 8781))

receiver.recv_data()
print(receiver.data)
