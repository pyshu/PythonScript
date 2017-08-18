# _*_ coding : utf-8 _*_
__author__ = 'lius'

from socketserver import BaseRequestHandler, UDPServer
from socketserver import ThreadingUDPServer
import threading

connect_data = {}
g_lock = threading.Lock()
server_ip = '192.168.2.112'
server_70 = (server_ip, 70)
server_90 = (server_ip, 90)

class E_Handler(BaseRequestHandler):
    def handle(self):
        print('*' * 100)
        global connect_data, g_lock, server_70, server_90, server_ip
        print('Got connection from', self.client_address)
        msg, sock = self.request
        if b'OK' in msg:
            sock.sendto(msg, server_70)
            print('Send the message to the server : ', server_70, ' EF status OK')
        elif self.client_address[0] == server_ip:
            if msg[0] in connect_data.keys():
                sock.sendto(msg[1:], connect_data[msg[0]])
                print('Send the message to the client : ', connect_data[msg[0]], ' ef number :', msg[0])
        else:
            if msg[0] not in connect_data.keys() or connect_data[msg[0]] != self.client_address:
                with g_lock:
                    connect_data[msg[0]] = self.client_address
            sock.sendto(msg, server_90)
            print('Send the message to the server : ', server_90, ' ef number :', msg[0])
        print('*'*100)

if __name__ == '__main__':
    serv = ThreadingUDPServer(('', 70), E_Handler)
    serv.serve_forever()