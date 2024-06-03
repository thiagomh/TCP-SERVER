from socket import socket, AF_INET, SOCK_STREAM
import hashlib
import threading
import os

BUFFER = 1024

def close_connection(socket: socket, addr):
      socket.send(b"OK")
      print(f"Encerrando conexão com cliente: {addr[0]}:{addr[1]}\n")
      socket.close()

def send_file(socket: socket, addr, request):
      filename = request[1]
      file_path = f"data/{filename}" 
      if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                  data = file.read()
                  file_hash = hashlib.sha256(data).hexdigest()
                  file_size = os.path.getsize(file_path)
                  return_msg = f"OK/{file_size}/{file_hash}".encode() 
                  socket.send(return_msg)
            if data:
                  segments = []

                  for i in range(0, file_size, BUFFER):
                        segment = data[i:i+BUFFER]
                        segments.append(segment)

                  print("Iniciando envio de pacotes...")
                  for segment in segments:
                        socket.send(segment)

                  print("Transferência finalizada.\n")

      else:
            socket.send("NOK/Arquivo não encontrado".encode())

def chat(socket: socket, addr):
      print(f"Iniciando chat com {addr[0]}:{addr[1]}")
      socket.send(b"OK")

      while True: 
            mensagem = socket.recv(1024)
            print(f"Cliente {addr[0]}:{addr[1]} : {mensagem.decode()}")

            if mensagem == b"A":
                  print(f"Encerrando chat com {addr}\n")
                  break

            resposta = input(": ")
            socket.send(resposta.encode())

def handle_client(socket: socket, addr):
      while True:
            request = socket.recv(BUFFER)
            request = request.decode().split("/")

            print(f"request: {request} - {addr}")

            if request[0] == "SAIR":
                  close_connection(socket, addr)
                  break

            elif request[0] == "ARQUIVO":
                  send_file(socket, addr, request)
                  continue
            
            elif request[0] == "CHAT":
                  chat(socket, addr) 
                  continue

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
            
            # Inicializando thread 
            print(f"Server conectado ao cliente {client_addr[0]}:{client_addr[1]}\n")
            thread = threading.Thread(target=handle_client, args=(client_socket, client_addr))
            thread.start()

if __name__ == "__main__":
      start_server()