import signal

from functools import partial
from time import sleep
from udp_tcp import tcp

class sender_tcp(tcp):
    def __init__(self, bind):
        tcp.__init__(self, bind)
        self.default_wndw_sze = 16
        signal.signal(signal.SIGALRM, partial(handler, self))

    def send_data(self, data, agt, dst):
        self.data = data
        self.data_len = len(data)
        self.agt = agt
        self.dst = dst

        self.recv_ack_idx = []
        self.sent_idx = 0
        self.wndw_sze = self.default_wndw_sze
        self.wndw_beg = 0
        self.wndw_end = min(self.wndw_beg + self.wndw_sze, self.data_len)
        self.last_end = 0

        self.send_data_to_dst()

        ack_idx = 0
        while ack_idx + 1 != self.data_len:
            ack_type, ack_idx = self.recv_ack_from_dst()
            if ack_type == self.ACK:
                # XXX: may deadlock here
                self.wndw_beg = ack_idx
                self.wndw_end = min(self.wndw_beg + self.wndw_sze, self.data_len)
                self.send_data_to_dst()

        print('send\tfin')
        self.send_pck_with_ack(b'', self.agt, (self.dst, 0), self.FIN)
        _, _, (_, _), (ack_type, _) = self.recv_pck_with_ack()
        if ack_type == self.FINACK:
            print('recv\tfinack')

    def send_data_to_dst(self):
        for i in range(self.last_end, self.wndw_end):
            if i == 33:
                print('==============')
                print('=== SEND33 ===')
                print('==============')
            self.sent_idx  = i

            print('send\tdata\t#{},\twinSize = {}'.format(self.sent_idx, self.wndw_sze))
            self.send_pck_with_ack(self.data[self.sent_idx], self.agt, (self.dst, self.sent_idx), self.NOACK)

            if len(self.recv_ack_idx) < self.sent_idx+1:
                self.recv_ack_idx += [False]
            self.recv_ack_idx[self.sent_idx] = False

            signal.alarm(1)
            sleep(0.5)
        self.last_end = self.wndw_end

    def recv_ack_from_dst(self):
        _, _, _, (ack_type, ack_idx) = self.recv_pck_with_ack()
        self.recv_ack_idx[ack_idx] = True
        if ack_type == self.ACK:
            print('recv\tack\t#{}'.format(ack_idx))
        return ack_type, ack_idx

def handler(alrm_self, signum, frame):
    if alrm_self.sent_idx == 33:
        print('===============')
        print('=== alarm33 ===')
        print('===============')
    if not sender.recv_ack_idx[alrm_self.sent_idx]:
        print('time\tout\t\tthreshold = {}'.format(sender.wndw_sze))

sender = sender_tcp(('127.0.0.1', 8780))

agt = ('127.0.0.1', 8782)
dst = ('127.0.0.1', 8781)

datas = ['Hello~']*50
datas = [(str(i)+' '+data).encode() for i,data in enumerate(datas)]

# filename = './src/ubuntu.jpg'
# with open(filename, 'rb') as f:
#     data = f.read()
# datas = [ data[i:i+900] for i in range(0, len(data), 900) ]
# datas = [filename.split('.')[-1].encode()] + datas

sender.send_data(datas, agt, dst)
