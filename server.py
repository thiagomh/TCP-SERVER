import socket
import threading
from hashlib import sha256

IP = '127.0.0.1'
PORT = 4455
ADDR = (IP, PORT)
BUFFER = 1024

def get_file(request):
      try:
            with open(f"data/{request[1]}", "rb") as file:
                        return file.read()
      except:
            return "Arquivo não encontrado"

def send_file(clientSocket: socket, file: bytes):
      segments = []
      for i in range(0, len(file), BUFFER):
            segment = file[i:i+BUFFER]
            
            segments.append(segment)

      i = 0
      while i < len(segments):
            # calcular sum
            h = sha256(segments[i])
            checksum = h.hexdigest()

            packet = segments[i]
            clientSocket.socket.send(packet)
            i += 1

      clientSocket.socket.send('EOF'.encode("utf-8"))
      return  

def client_request2(clientSocket: socket):
      request = clientSocket.socket.recv(1024)
      request = request.decode().split('/')
      
      if request[0] == 'GET':
            file = get_file(request)
            if file == "Arquivo não encontrado":
                  clientSocket.socket.send(file.encode())
            else:
                  send_file(clientSocket, file)
      print("Arquivo não encontrado")
      return            
             

def client_request(clientSocket: socket):
      while True:
            data = clientSocket.recv(1000)

            if not data:
                  print('Bye')
                  break

            data = data[::-1]

            clientSocket.send(data)
      clientSocket.close()

def main():
      # Criando socket TCP 
      serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      # Associando socket a um endereço(IP+PORTA)
      serverSocket.bind(ADDR)
      # Abre a porta na qual no servidor vai aguardar conexões TCP
      serverSocket.listen()
      print(f"Server running {ADDR}")

      while True:
            clientSocket, client_addr = serverSocket.accept()

            print(f"Connected to: {client_addr[0]}:{client_addr[1]}")
            thread = threading.Thread(target=client_request(clientSocket))
            thread.start()

if __name__ == "__main__":
      main()