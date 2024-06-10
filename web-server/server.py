from socket import socket, AF_INET, SOCK_STREAM
import threading
import os

def handle_client(socket: socket, client_addr):
      try:
            request = socket.recv(1024).decode()
            if request:
                  headers = request.split('\n')
                  print(f"Requisição do cliente({client_addr[0]}:{client_addr[1]}): {headers[0]}")

                  method = headers[0].split()[0]
                  route = headers[0].split()[1]
                  
                  if method != 'GET':
                        send_501(socket)
                        socket.close()
                        return 
                  
                  if route.endswith('.html'):
                        send_file(socket, route)
                  
                  elif route.endswith('.jpg') or route.endswith('.png'):
                        send_image(socket, route)
                  
                  elif route.endswith(".ico"):
                        pass

                  else:
                        send_415(socket)

      except Exception as e:
            send_404()
      finally:
            socket.close()

def send_file(socket: socket, route: str):
      file_path = f"web-server/web-pages{route}"
      if os.path.isfile(file_path):
            with open(file_path, "rb") as file:
                  response_body = file.read()

            response_header = ("HTTP/1.1 200 OK\r\n"
                        "Server: Python-Server-TM\r\n"
                        f"Content-Length: {len(response_body)}\r\n"
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
                        "Server: Python-Server-TM\r\n"
                        f"Content-Length: {len(response_body)}\r\n"
                        "\r\n")
            
            socket.send(response_header.encode() + response_body)
      else:
            print("404 ERRO - Arquivo Inexistente.\n")
            send_404(socket)

def send_404(socket: socket):
      response_header = ("HTTP/1.1 404 Not Found\r\n"
                        "Server: Python-Server-TM\r\n"
                        "Content-Type: text/html\r\n"
                        "\r\n")
      response_body = b"<html><body><h1>404 Not Found</h1></body></html>"
      socket.send(response_header.encode() + response_body) 

def send_415(socket: socket):
      response_header = ("HTTP/1.1 415 Unsupported Media Type\r\n"
                        "Server: Python-Server-TM\r\n"
                        "Content-Type: text/html\r\n"
                        "\r\n")
      response_body = b"<html><body><h1>415 Unsupported Media Type</h1></body></html>"
      socket.send(response_header.encode() + response_body)

def send_500(socket: socket):
      response_header = ("HTTP/1.1 500 Internal Server Error\r\n"
                        "Server: Python-Server-TM\r\n"
                        "Content-Type: text/html\r\n"
                        "\r\n")
      response_body = b"<html><body><h1>500 Internal Server Error</h1></body></html>"
      socket.send(response_header.encode() + response_body)

def send_501(socket: socket):
      response_header = ("HTTP/1.1 501 Not Implemented\r\n"
                        "Server: Python-Server-TM\r\n"
                        "Content-Type: text/html\r\n"
                        "\r\n")
      response_body = b"<html><body><h1>501 Not Implemented</h1></body></html>"
      socket.send(response_header.encode() + response_body)

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