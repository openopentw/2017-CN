import socket
import struct

class udp():
    def __init__(self, bind):
        self.sock = socket.socket(socket.AF_INET, # Internet
                                  socket.SOCK_DGRAM) # UDP
        self.sock.bind(bind)

    def send_pck(self, msg, dst, pck_info):
        host, pck_idx = pck_info
        msg = self.pack_header(host, pck_idx) + msg
        self.sock.sendto(msg, dst)

    def recv_pck(self):
        data, src = self.sock.recvfrom(1024) # buffer size is 1024 bytes
        return data[8:], src, self.unpack_header(data[:8])

    def pack_header(self, host, pck_idx):
        ip = struct.unpack("!I", socket.inet_aton(host[0]))[0] # change ip to int
        pack_ip = ip.to_bytes(4, 'big')
        pack_port = host[1].to_bytes(2, 'big')
        pack_pck_idx = pck_idx.to_bytes(2, 'big')
        return pack_ip + pack_port + pack_pck_idx

    def unpack_header(self, header):
        int_ip = int.from_bytes(header[:4], byteorder='big')
        ip = socket.inet_ntoa(struct.pack("!I", int_ip)) # change int to ip
        port = int.from_bytes(header[4:6], byteorder='big')
        pck_idx = int.from_bytes(header[6:8], byteorder='big')
        return (ip, port), pck_idx

class tcp(udp):
    def __init__(self, bind):
        udp.__init__(self, bind)

        self.NOACK = 0
        self.ACK = 1
        self.FIN = 2
        self.FINACK = 3

    def send_pck_with_ack(self, data, dst, pck_info, ack_type, ack_num=0):
        data = self.pack_acks(ack_type, ack_num) + data
        self.send_pck(data, dst, pck_info)

    def recv_pck_with_ack(self):
        data, src, pck_info = self.recv_pck()
        return data[8:], src, pck_info, self.unpack_acks(data[:8])

    def pack_acks(self, ack_type, ack_num=0):
        pack_ack = ack_type.to_bytes(2, 'big')
        pack_ack += b'\x00'*2
        if ack_type == self.ACK:
            pack_ack += ack_num.to_bytes(4, 'big')
        else:
            pack_ack += b'\x00'*4
        return pack_ack

    def unpack_acks(self, acks_header):
        ack_type = int.from_bytes(acks_header[:2], byteorder='big')
        if ack_type == self.ACK:
            ack_num = int.from_bytes(acks_header[4:], byteorder='big')
            return ack_type, ack_num
        else:
            return ack_type, 0
