#!/usr/bin/python3

import gen_ip

import socket

from random import randint
from time import sleep

import sys
write = sys.stdout.buffer.write

# host & names
host = 'irc.freenode.net'
port = 6667 # non-SSL
channel = '#b04902053'
botnick = 'PRIVMSG'

with open('./config') as f:
    channel = f.readline().split("'")[1]
print(channel)

# connect
ircsocket = socket.SocketType(socket.AF_INET, socket.SOCK_STREAM)
ircsocket.connect((host, port))

ircsocket.send(bytes('NICK ' + botnick + '\n', 'UTF-8'))
ircsocket.send(bytes('USER ' + botnick + ' ' + botnick + ' ' + botnick + ' ' + botnick + '\n', 'UTF-8'))
# ircsocket.send(bytes('PRIVMSG nickserv :INOOPE\r\n'), 'UTF-8')

def joinchan(chan):
    """Join channel(s)."""
    ircsocket.send(bytes('JOIN ' + chan + '\n', 'UTF-8'))
    ircmsg = ''
    while ircmsg.find('End of /NAMES list.') == -1:
        ircmsg = ircsocket.recv(2048).decode('UTF-8')
        ircmsg = ircmsg.strip('\n\r')
        # print(ircmsg)

def sendmsg(msg, target=channel):
    """Send message to specified channel."""
    msg = bytes('PRIVMSG ' + target + ' :' + msg + '\n', 'UTF-8')
    sleep(randint(5, 10) / 10) # to avoid throttling due to flooding
    write(msg)
    ircsocket.send(msg)

def ping(msg):
    """Respond to server Pings."""
    msg = msg[0:1] + 'O' + msg[2:]
    ircsocket.send(bytes(msg, 'utf-8'))
    sendmsg('This message should be eaten by irc. QQ.')

def main():
    print('Joining channel ...')
    joinchan(channel)
    print('Start!')
    sendmsg('Hello! I am robot.')

    while True:
        ircmsg = ircsocket.recv(2048).decode('UTF-8')
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)

        if ircmsg.startswith('PING'):
            print('=== PING PONG ===')
            ping(ircmsg)

        elif 'throttled due to flooding' in ircmsg:
            print('=== THROTTLE DUE TO FLOODING ===')
            # TODO
            sleep(1)

        elif ' PRIVMSG ' in ircmsg:
            name = ircmsg.split('!', 1)[0][1:]
            message = ircmsg.split(' PRIVMSG ', 1)[1].split(':', 1)[1]

            print('{}: "{}"'.format(name, message))

            if len(name) < 17:
                if message[0] == '@':
                    # repeat
                    if message.startswith('@repeat '):
                        print('=== repeat ===')
                        sendmsg(message[8:])

                    # convert
                    elif message.startswith('@convert '):
                        print('=== convert ===')
                        num_str = message[9:]
                        if num_str.startswith('0x'):
                            num = int(num_str, 16)
                            sendmsg(str(num))
                        else:
                            num = int(num_str)
                            sendmsg('0x{}'.format(format(num, '0x')))

                    # ip
                    elif message.startswith('@ip '):
                        print('=== ip ===')
                        ip_str = message[4:]
                        ips = gen_ip.gen_ips(ip_str)
                        sendmsg(str(len(ips)))
                        for ip in ips:
                            print(ip)
                            sendmsg(ip)

                    # help
                    elif message == '@help':
                        print('=== help ===')
                        sendmsg('@repeat <Message>')
                        sendmsg('@convert <Number>')
                        sendmsg('@ip <String>')

                else:
                    print('=== parse name & message error ===')
                    print('got name: {}'.format(name))
                    print('got message: {}'.format(message))

if __name__ == "__main__":
    main()
