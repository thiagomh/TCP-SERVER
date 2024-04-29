import socket
#import struct
from _thread import *
import threading

IP = '127.0.0.1'
PORT = 4455
ADDR = (IP, PORT)
BUFFER = 1024

class tcp_segment:
      # source_port(2 bytes) - dest_port(2 bytes) - seq_num(4 bytes)
      # ack_num(4 bytes) - rcv_window(2 bytes) - checksum(2 bytes)
      # header_len; ack; rst; syn; fin (1 byte)   

      MSS = 1000
      HEADER_FORMAT = 'H H I I H H b'

      def __init__(self, source_port, dest_port, seq_num, ack_num, rcv_window, data, FIN) -> None:
            self.source_port = source_port
            self.dest_port = dest_port
            self.seq_num = seq_num
            self.ack_num = ack_num
            self.rcv_window = rcv_window

            self.ack = 1
            self.fin = FIN
            self.syn = 0

            self.data = data


def client_request(clientSocket: socket):
      while True:
            data = clientSocket.recv(1000)

            if not data:
                  print('Bye')
                  break

            data = data[::-1]

            clientSocket.send(data)
      clientSocket.close()

def main():
      # Criando socket TCP 
      serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      # Associando socket a um endereço(IP+PORTA)
      serverSocket.bind(ADDR)
      # Abre a porta na qual no servidor vai aguardar conexões TCP
      serverSocket.listen()
      print(f"Server running {ADDR}")

      while True:
            clientSocket, client_addr = serverSocket.accept()

            print("Connected to:", client_addr[0], ":", client_addr[1])

            start_new_thread(client_request(clientSocket), (clientSocket))
      

if __name__ == "__main__":
      main()