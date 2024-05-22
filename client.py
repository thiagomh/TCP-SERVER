from socket import socket, AF_INET, SOCK_STREAM
import os

def options_menu(socket: socket):
      print("1-Sair\n2-Arquivo\n3-Chat\n")
      opt = int(input("Escolha uma opção: "))
      match opt:
            case 1:
                  # Enviando pedido pra fechar conexão 
                  socket.send(b"SAIR")
                  # Recebendo confirmação que a conexão foi encerrada
                  resp = socket.recv(1024)
      
                  if resp.decode() == "OK":
                        print("Conexão encerrada")
                        return "SAIR"
            case 2:
                  filename = input("Insira o nome do arquivo (nome.txt): ")
                  socket.send(f"ARQUIVO/{filename}".encode())
                  file_request(socket, filename)
            case 3:
                  socket.send("CHAT".encode())
                  #chat(socket)
            case _:
                  print("Opção inválida.")
                  options_menu(socket)

def file_request(socket: socket, filename):
      if os.path.exists(f"./received_data/{filename}"):
            with open(f"./received_data/{filename}", "w"):
                  pass

      file = open(f"./received_data/{filename}", "a", newline="\r\n")

      data = socket.recv(512)
      if data == b"OK":
            data = socket.recv(512)
            data = data.decode()
            data.split("\n")
            print(data, "\n")

            while data != b"EOF":
                  data = socket.recv(512)
                  data = data.decode()
                  file.write(data)

            file.close()
                  
      else:
            print(data.decode())

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