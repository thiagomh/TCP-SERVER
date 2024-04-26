import socket

IP = ""
PORT = 4455
ADDR = (IP, PORT)
BUFFER = 1024

def tcp_segment():
      # source_port(2 bytes) - dest_port(2 bytes) - seq_num(4 bytes)
      # ack_num(4 bytes) - rcv_window(2 bytes) - checksum(2 bytes)
      # header_len(4 bits) - rsv(6 bits) - red_flag (6 bits)  
      MSS = 1000
      HEADER_FORMAT = ''

def main():
      # Criando socket TCP 
      # Dominio - AF_INET (IPv4) 
      # SOCK_STREAM - Tipo de comunição; fluxo de bytes sem delimitação; full duplex
      serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      # Associando socket a um endereço(IP+PORTA)
      serverSocket.bind(ADDR)
      # Abre a porta na qual no servidor vai aguardar conexões TCP
      serverSocket.listen()

if __name__ == "__main__":
      main()