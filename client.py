import socket

HOST = '127.0.0.1'
PORT = 4455

def main():
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