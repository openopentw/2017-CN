import signal

from functools import partial
from sys import argv
from time import sleep
from udp_tcp import tcp

class sender_tcp(tcp):
    def __init__(self, bind):
        tcp.__init__(self, bind)
        self.default_wndw_sze = 1
        self.thres = 16

        self.recved_ack = -1
        self.sent_alarm = False
        signal.signal(signal.SIGALRM, self.handler)

    def send_data(self, data, agt, dst):
        self.last_sent = -1 # for resend decide use

        self.data = data
        self.data_len = len(data)
        self.agt = agt
        self.dst = dst

        self.sent_idx = 0
        self.wndw_sze = self.default_wndw_sze
        self.wndw_beg = 0
        self.last_end = 0

        self.send_data_to_dst()

        ack_idx = 0
        while ack_idx + 1 < self.data_len:
            ack_type, ack_idx = self.recv_ack_from_dst()
            # if ack_type == self.ACK:
            self.wndw_beg = ack_idx
            self.send_data_to_dst()

        signal.alarm(0)
        signal.alarm(1)
        print('send\tfin')
        self.sent_alarm = True
        self.send_pck_with_ack(b'', self.agt, (self.dst, 0), self.FIN)
        _, _, (_, _), (ack_type, _) = self.recv_pck_with_ack()
        if ack_type == self.FINACK:
            print('recv\tfinack')
        sleep(1)

    def send_data_to_dst(self):
        wndw_end = min(self.last_end + self.wndw_sze, self.data_len)
        # wndw_end = min(self.wndw_beg + self.wndw_sze, self.data_len)+1
        # print(self.wndw_beg, self.last_end, self.wndw_sze)
        for i in range(self.last_end, wndw_end):
            self.sent_idx  = i
            if i <= self.last_sent:
                print('resnd\tdata\t#{},\twinSize = {}'.format(self.sent_idx, self.wndw_sze))
            else:
                self.last_sent = i
                print('send\tdata\t#{},\twinSize = {}'.format(self.sent_idx, self.wndw_sze))
            self.send_pck_with_ack(self.data[self.sent_idx], self.agt, (self.dst, self.sent_idx), self.NOACK)
            signal.alarm(1)

        self.last_end = wndw_end

    def recv_ack_from_dst(self):
        _, _, _, (ack_type, ack_idx) = self.recv_pck_with_ack()
        if ack_type == self.ACK and self.recved_ack + 1 == ack_idx:
            print('recv\tack\t#{}'.format(ack_idx))
            self.recved_ack = ack_idx
            # _, _, (_, _), (ack_type, _) = self.recv_pck_with_ack()

            if self.wndw_sze < self.thres:
                self.wndw_sze *= 2
            else:
                self.wndw_sze += 1

        return ack_type, ack_idx

    def handler(self, signum, frame):
        self.thres = max(self.wndw_sze // 2, 1)
        self.wndw_sze = 1

        resnd_pck = self.recved_ack + 1
        # if resnd_pck >= self.data_len:
        #     pass
        if self.sent_alarm:
            # resend fin
            print('resnd\tfin')
            self.send_pck_with_ack(b'', self.agt, (self.dst, 0), self.FIN)
        elif resnd_pck <= self.sent_idx:
            print('time\tout\t\tthreshold = {}'.format(self.thres))
            self.last_end = resnd_pck
            self.send_data_to_dst()

sender = sender_tcp(('127.0.0.1', 8780))

agt = ('127.0.0.1', 8782)
dst = ('127.0.0.1', 8781)

# datas = ['Hello~']*50
# datas = [(str(i)+' '+data).encode() for i,data in enumerate(datas)]
# datas = [b'START'] + datas + [b'END']

# filename = './src/ubuntu.jpg'
filename = argv[1]
with open(filename, 'rb') as f:
    data = f.read()
datas = [ data[i:i+900] for i in range(0, len(data), 900) ]
datas = [filename.split('.')[-1].encode()] + datas

sender.send_data(datas, agt, dst)
