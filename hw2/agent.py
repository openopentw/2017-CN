import random

from udp_tcp import tcp

agent = tcp(('127.0.0.1', 8782))

while True:
    pck, src, (dst, pck_idx), (ack_type, ack_idx) = agent.recv_pck_with_ack()

    if ack_type == agent.NOACK:
        print('get\tdata\t#{}'.format(pck_idx))

        if random.random() > 0.2:
            agent.send_pck_with_ack(pck, dst, (src, pck_idx), ack_type, ack_idx)
            print('fwd\tdata\t#{}'.format(pck_idx))
        else:
            print('drop\tdata\t#{}'.format(pck_idx))

    elif ack_type == agent.ACK:
        print('get\tack\t#{}'.format(ack_idx))

        print('fwd\tack\t#{}'.format(ack_idx))
        agent.send_pck_with_ack(pck, dst, (src, pck_idx), ack_type, ack_idx)

    elif ack_type == agent.FIN:
        print('get\tfin')

        if random.random() > 0.2:
            print('fwd\tfin')
            agent.send_pck_with_ack(pck, dst, (src, pck_idx), ack_type, ack_idx)
        else:
            print('drop\tfin')

    elif ack_type == agent.FINACK:
        print('get\tfinack')

        print('fwd\tfinack')
        agent.send_pck_with_ack(pck, dst, (src, pck_idx), ack_type, ack_idx)
