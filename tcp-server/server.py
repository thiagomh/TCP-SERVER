from socket import socket, AF_INET, SOCK_STREAM
import hashlib
import threading
import os

BUFFER = 1024

def close_connection(socket: socket, addr):
      socket.send(b"OK")
      print(f"Encerrando conexão com cliente {addr[0]}:{addr[1]}\n")
      socket.close()

def send_file(socket: socket, addr, request):
      filename = request[1]
      file_path = f"tcp-server/data/{filename}" 
      if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                  data = file.read()
                  # Calculando dados do arquivo 
                  file_hash = hashlib.sha256(data).hexdigest()
                  file_size = os.path.getsize(file_path)
                  num_segments: int = file_size/BUFFER
                  return_msg = f"OK/{file_size}/{file_hash}/{num_segments}".encode() 
                  socket.send(return_msg)
            if data:
                  segments = []

                  for i in range(0, file_size, BUFFER):
                        segment = data[i:i+BUFFER]
                        segments.append(segment)

                  print("Iniciando envio de pacotes...")

                  for segment in segments:
                        socket.send(segment)

                  print(f"Transferência de {filename} para {addr[0]}:{addr[1]} finalizada.\n")

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
      IP = '192.168.1.18'
      PORT = 50007
      ADDR = (IP, PORT)
      # Criando socket TCP
      server_socket = socket(AF_INET, SOCK_STREAM)
      # Associando socket a um endereço
      server_socket.bind(ADDR)
      # Abre a porta na qual o servidor vai aguardar conexões
      server_socket.listen()
      print(f"Server ouvindo em {ADDR[0]}:{ADDR[1]}")

      while True:
            # Aceitando conexões TCP
            client_socket, client_addr = server_socket.accept()
            
            # Inicializando thread 
            print(f"Server conectado ao cliente {client_addr[0]}:{client_addr[1]}\n")
            thread = threading.Thread(target=handle_client, args=(client_socket, client_addr))
            thread.start()
            print(f"[Número de conexões]: {threading.active_count() - 1}\n")

if __name__ == "__main__":
      start_server()