import socket

def request_options(clientSocket: socket):
      print("1-SAIR\n2-Abrir arquivo\n3-Chat")
      opt = input("Escolha uma opção: ")
      match opt:
            case 1:
                  close_connection(clientSocket)
            case 2:
                  file_request(clientSocket)
            case 3:
                  chat(clientSocket)
            case _:
                  print("Opção inválida")
                  request_options()      
      return 

def hash_func():
      return

def close_connection(clientSocket: socket):
      clientSocket.socket.send("SAIR".encode())
      msg = clientSocket.recv(1024)
      if msg == b"SAIR":
            print("Conexão encerrada.")
            clientSocket.close()
            return

def file_request(clientSocket: socket):
      request = input("Qual arquivo deseja abrir? ")

      request = request.encode()
      clientSocket.socket.send(request)

      return 

def chat(clientSocket: socket):
      return 

def main():
      HOST = '127.0.0.1'
      PORT = 4455
      clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

      clientSocket.connect((HOST, PORT))

      msg = "oiiiii"
      while True:
            clientSocket.send(msg.encode())
            data = clientSocket.recv(1000)

            print("Server: ", str(data.decode()))

            ans = input('\nDo you want to continue(y/n) :')
            if ans == 'y':
                  continue
            else:
                  break
      clientSocket.close()


if __name__ == "__main__":
      main()