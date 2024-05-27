from socket import socket, AF_INET, SOCK_STREAM
import threading
import os

def handle_client(socket: socket, client_addr):
      request = socket.recv(1024).decode()
      headers = request.split('\n')
      print(f"Requisição do cliente({client_addr[0]}:{client_addr[1]}): {headers[0]}")

      method = headers[0].split()[0]
      route = headers[0].split()[1]
      
      if method != 'GET':
            return 
      
      if route.endswith('.html'):
            send_file(socket, route)
      
      elif route.endswith('.jpg') or route.endswith('.png'):
            return
      
      else:
            print("erro formato")

def send_file(socket: socket, route: str):
      file_path = f"web-pages{route}"
      if os.path.isfile(file_path):
            with open(file_path, "rb") as file:
                  response_body = file.read()

            response_header = (

            )
            socket.send(response_body)
      else:
            print("aRQUIVO NAO ENCONTRADO")

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
            
            # Inicializando thread 
            print(f"Server conectado ao cliente {client_addr[0]}:{client_addr[1]}\n")
            thread = threading.Thread(target=handle_client, args=(client_socket, client_addr))
            thread.start()

if __name__ == "__main__":
      start_server()