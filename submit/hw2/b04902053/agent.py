import random

from udp_tcp import tcp

agent = tcp(('127.0.0.1', 8782))

random_num = 0.2

total = 0
drop = 0

while True:
    pck, src, (dst, pck_idx), (ack_type, ack_idx) = agent.recv_pck_with_ack()

    if ack_type == agent.NOACK:
        total += 1

        print('get\tdata\t#{}'.format(pck_idx))

        if random.random() > random_num:
            agent.send_pck_with_ack(pck, dst, (src, pck_idx), ack_type, ack_idx)
            print('fwd\tdata\t#{},\tloss rate = {}'.format(pck_idx, drop / total))
        else:
            drop += 1
            print('drop\tdata\t#{},\tloss rate = {}'.format(pck_idx, drop / total))

    elif ack_type == agent.ACK:
        print('get\tack\t#{}'.format(ack_idx))

        print('fwd\tack\t#{}'.format(ack_idx))
        agent.send_pck_with_ack(pck, dst, (src, pck_idx), ack_type, ack_idx)

    elif ack_type == agent.FIN:
        print('get\tfin')

        if random.random() > random_num:
            print('fwd\tfin')
            agent.send_pck_with_ack(pck, dst, (src, pck_idx), ack_type, ack_idx)
        else:
            print('drop\tfin')

    elif ack_type == agent.FINACK:
        print('get\tfinack')

        print('fwd\tfinack')
        agent.send_pck_with_ack(pck, dst, (src, pck_idx), ack_type, ack_idx)
