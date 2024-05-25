from socket import socket, AF_INET, SOCK_STREAM
import os
import hashlib

BUFFER = 1024

def options_menu(socket: socket):
      print("1-Sair\n2-Arquivo\n3-Chat\n")
      option = int(input("Escolha uma opção: "))

      if option == 1:  
            socket.send(b"SAIR")
            # Recebendo confirmação que a conexão foi encerrada
            resp = socket.recv(1024)
      
            if resp.decode() == "OK":
                  print("Conexão encerrada")
                  return "SAIR"
            
      elif option == 2:
            filename = input("Insira o nome do arquivo (nome.txt): ")
            socket.send(f"ARQUIVO/{filename}".encode())
            file_request(socket, filename)

      elif option == 3:
            chat(socket)
      
      else:
          print("Opção inválida.")
          options_menu(socket)  

def file_request(socket: socket, filename):
      # Recebendo dados do arquivo (Arquivo encontrado/Tamanho/Hash)
      data = socket.recv(BUFFER).decode().split("/")

      # Arquivo não encontrado
      if data[0] == "NOK":
            print(data[1])
            return 

      # Criando arquivo do lado do cliente
      save_path = f"./received_data/{filename}"
      os.makedirs(os.path.dirname(save_path), exist_ok=True)

      # Abrindo arquivo para escrita binária 
      with open(save_path, "wb") as file: 

            recv_data = b""       
            segment = b""

            while True:
                  # Recebendo segmentoss
                  segment = socket.recv(BUFFER)
                  recv_data += segment
                  
                  # Caso o tamanho do segmento seja menor que o buffer
                  # significa que é o ultimo a ser recebido
                  if len(segment) < BUFFER:
                        break
            
            received_hash = hashlib.sha256(recv_data).hexdigest()
            # Verificando integridade do arquivo      
            if received_hash == data[2]:
                  file.write(recv_data)
                  print(f"Arquivo {filename} recebido e salvo com sucesso.\n")
            else:
                  print("Erro na verificação de integridade do arquivo.\n")
                  
            file.close()

def chat(socket: socket, addr):
      print("[A] - Sair\n")
      socket.send(b"CHAT")
      
      resposta = socket.recv(1024)
      print(f"Server: {resposta.decode()}")

      while True:
            mensagem = input(": ")
            socket.send(mensagem.encode())

            if mensagem == "A":
                  print(f"Encerrando chat...\n")
                  break

            resposta = socket.recv(1024)
            print(f"Server : {resposta.decode()}")

def start_client():
      # IP e porta referentes ao endereço do server
      IP = '127.0.0.1'
      PORT = 50007
      # Criando socket do cliente
      client_socket = socket(AF_INET, SOCK_STREAM)
      # Requerindo conexão com o server
      client_socket.connect((IP, PORT))

      # Loop do menu
      while True:
            r = options_menu(client_socket)
            if r == "SAIR":
                  break

if __name__ == "__main__":
      start_client()