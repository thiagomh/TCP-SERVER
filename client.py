from socket import socket, AF_INET, SOCK_STREAM

def options_menu(socket: socket):
      print("1-Sair\n2-Arquivo\n3-Chat\n")
      opt = int(input("Escolha uma opção: "))
      match opt:
            case 1:
                  socket.send(b"SAIR")
                  resp = socket.recv(1024)
      
                  if resp.decode() == "OK":
                        print("Conexão encerrada")
                        return "SAIR"
            case 2: 
                  socket.send("ARQUIVO".encode())
                  #file_request(socket)
            case 3:
                  socket.send("CHAT".encode())
                  #chat(socket)
            case _:
                  print("Opção inválida.")
                  options_menu(socket)

def start_client():
      # IP e porta referentes ao endereço do server
      IP = '127.0.0.1'
      PORT = 50007
      # Criando socket do cliente
      client_socket = socket(AF_INET, SOCK_STREAM)
      # Requerindo conexão com o server
      client_socket.connect((IP, PORT))

      while True:
            r = options_menu(client_socket)
            if r == "SAIR":
                  break

if __name__ == "__main__":
      start_client()