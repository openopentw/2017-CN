import signal

from functools import partial
from udp_tcp import tcp

class sender_tcp(tcp):
    def __init__(self, bind):
        tcp.__init__(self, bind)
        self.sent_idx = 0
        self.default_wndw_sze = 16
        signal.signal(signal.SIGALRM, partial(self.handler, self))

    def send_data(self, data, agt, dst):
        self.data = data
        self.data_len = len(data)
        self.agt = agt
        self.dst = dst

        self.wndw_sze = self.default_wndw_sze
        self.wndw_beg = 0
        self.wndw_end = min(self.wndw_beg + self.wndw_sze, self.data_len)
        self.last_end = 0

        self.send_data_to_dst()

        ack_num = 0
        while ack_num + 1 != self.data_len:
            _, _, _, (ack_type, ack_num) = self.recv_pck_with_ack()
            if ack_type == self.ACK:
                print('ack:', ack_num)
                self.wndw_beg = ack_num
                self.wndw_end = min(self.wndw_beg + self.wndw_sze, self.data_len)
                self.send_data_to_dst()

        self.send_pck_with_ack(b'', self.agt, (self.dst, 0), self.FIN)
        _, _, (_, _), (ack_type, _) = self.recv_pck_with_ack()
        if ack_type == self.FINACK:
            print('receive FINACK')

    def send_data_to_dst(self):
        for self.sent_idx in range(self.last_end, self.wndw_end):
            print('send:', self.sent_idx)
            self.send_pck_with_ack(self.data[self.sent_idx], self.agt, (self.dst, self.sent_idx), self.NOACK)
            signal.alarm(1)
            sleep(1)
        self.last_end = self.wndw_end

    def handler(self, alrm_self, signum, frame):
        print('alarm:', alrm_self.sent_idx)

sender = sender_tcp(('127.0.0.1', 8780))

from time import sleep

agt = ('127.0.0.1', 8782)
dst = ('127.0.0.1', 8781)

datas = ['Hello~']*10
datas = [(str(i)+' '+data).encode() for i,data in enumerate(datas)]

# filename = './src/ubuntu.jpg'
# with open(filename, 'rb') as f:
#     data = f.read()
# datas = [ data[i:i+900] for i in range(0, len(data), 900) ]
# datas = [filename.split('.')[-1].encode()] + datas

sender.send_data(datas, agt, dst)
