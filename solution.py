from socket import *
# In order to terminate the program
import sys


def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # Prepare a server socket
    serverSocket.bind(("", port))
    serverSocket.listen(1)

    while True:
        # Establish the connection
        connectionSocket, addr = serverSocket.accept()  # https://docs.python.org/3/library/socket.html#socket.socket.accept
        try:

            try:
                message = connectionSocket.recv(1024)  # https://docs.python.org/3/library/socket.html#socket.socket.recv
                filename = message.split()[1]
                f = open(filename[1:])
                outputdata = f.read()

                # Send one HTTP header line into socket.
                status = "HTTP/1.1 200 OK\r\n"
                connectionSocket.send(status.encode())

                # Send the content of the requested file to the client
                for i in range(0, len(outputdata)-1):
                    connectionSocket.send(outputdata[i].encode())

                connectionSocket.send("\r\n".encode())
                connectionSocket.close()
            except IOError:
                # Send response message for file not found (404)
                status = "HTTP/1.1 404 Not Found\r\n"
                connectionSocket.send(status.encode())

                # Close client socket
                connectionSocket.close()

        except (ConnectionResetError, BrokenPipeError):
            pass

    serverSocket.close()
    sys.exit()  # Terminate the program after sending the corresponding data


if __name__ == "__main__":
    webServer(13331)
