from socket import socket, AF_INET, SOCK_STREAM
import threading
import os

def handle_client(socket: socket, client_addr):
      request = socket.recv(1024).decode()
      if request:
            headers = request.split('\n')
            print(f"Requisição do cliente({client_addr[0]}:{client_addr[1]}): {headers[0]}")

            method = headers[0].split()[0]
            route = headers[0].split()[1]
            
            if method != 'GET':
                  send_405(socket)
                  return 
            
            if route.endswith('.html'):
                  send_file(socket, route)
            
            elif route.endswith('.jpg') or route.endswith('.png'):
                  send_image(socket, route)
            
            elif route.endswith(".ico"):
                  pass

            else:
                  print("erro formato")

      socket.close()

def send_file(socket: socket, route: str):
      file_path = f"web-server/web-pages{route}"
      if os.path.isfile(file_path):
            with open(file_path, "rb") as file:
                  response_body = file.read()

            response_header = ("HTTP/1.1 200 OK\r\n"
                        "Server: Microsoft-IIS/4.0\r\n"
                        f"Content-Length: {len(response_body)}\r\n"
                        "Connection: close\r\n"
                        "\r\n")
            socket.send(response_header.encode("utf-8") + response_body)
      else:
            print("ERRO - Arquivo inexistente.\n")
            send_404(socket)

def send_image(socket: socket, route: str):
      file_path = f"web-server/images{route}"
      if os.path.isfile(file_path):
            with open(file_path, "rb") as file:
                  response_body = file.read()

            response_header = ("HTTP/1.1 200 OK\r\n"
                        "Server: Microsoft-IIS/4.0\r\n"
                        f"Content-Length: {len(response_body)}\r\n"
                        "Connection: close\r\n"
                        "\r\n")
            
            socket.send(response_header.encode() + response_body)
      else:
            print("404 ERRO - Arquivo Inexistente.\n")
            send_404(socket)

def send_404(socket: socket):
      response_header = ("HTTP/1.1 404 Not Found\r\n"
                        "Server: Microsoft-IIS/4.0\r\n"
                        "Content-Type: text/html\r\n"
                        "Connection: close\r\n"
                        "\r\n")
      response_body = b"<html><body><h1>404 Not Found</h1></body></html>"
      socket.send(response_header.encode() + response_body) 

def send_405(socket: socket):
      pass

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