from tcp import tcp

agent = tcp(('127.0.0.1', 8782))

while True:
    msg, src, (dst, pck_idx) = agent.recv_pck()
    agent.send_pck(msg, dst, (src, pck_idx))
