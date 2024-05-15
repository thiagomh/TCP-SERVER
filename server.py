from socket import socket, AF_INET, SOCK_STREAM
import threading

def close_connection(socket: socket, addr):
      socket.send(b"OK")
      print(f"Encerrando conexão com cliente: {addr[0]}:{addr[1]}")
      socket.close()

def handle_client(socket: socket, addr):
      while True:
            request = socket.recv(1024)
            request = request.decode().split("/")

            print(f"request: {request}")

            if request[0] == "SAIR":
                  close_connection(socket, addr)
                  break

            elif request[0] == "ARQUIVO":
                  print("Arquivo")
            
            elif request[0] == "CHAT":
                  print("Chat") 

            else: 
                  socket.send("Requisição inválida.".encode())

def start_server():
      IP = '127.0.0.1'
      PORT = 50007
      ADDR = (IP, PORT)
      # Criando socket TCP
      server_socket = socket(AF_INET, SOCK_STREAM)
      # Associando socket a um endereço
      server_socket.bind(ADDR)
      # Abre a porta na qual o servidor vai aguardar conexões
      server_socket.listen(5)
      print(f"Server rodando em {ADDR[0]}:{ADDR[1]}")

      while True:
            # Aceitando conexões TCP
            client_socket, client_addr = server_socket.accept()
            
            print(f"Server conectado ao cliente {client_addr[0]}:{client_addr[1]}\n")
            thread = threading.Thread(target=handle_client, args=(client_socket, client_addr))
            thread.start()

if __name__ == "__main__":
      start_server()