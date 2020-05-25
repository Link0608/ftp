"""
    ftp服务端
"""
import os
from socket import *
from threading import Thread
from time import sleep

server_address = ("0.0.0.0", 9999)
FTP = "/home/tarena/focus/tarena_notes/month01/day18/"


class FTPServer(Thread):
    def __init__(self, connfd):
        self.connfd = connfd
        super().__init__()

    def do_list(self):
        file_list = os.listdir(FTP)
        if not file_list:
            self.connfd.send(b"Fail")
            return
        else:
            self.connfd.send(b"OK")
            sleep(0.1)
            files = "\n".join(file_list)
            self.connfd.send(files.encode())

    def do_download(self, file):
        file_list = os.listdir(FTP)
        if file not in file_list:
            self.connfd.send(b"Fail")
            return
        else:
            self.connfd.send(b"OK")
            sleep(0.1)
            with open(FTP + file, "rb") as fr:
                while True:
                    data = fr.read(1024)
                    if not data:
                        sleep(0.1)
                        self.connfd.send(b"##")
                        break
                    self.connfd.send(data)

    def do_uploading(self, ufile):
        files_folder = os.listdir(FTP)
        if ufile in files_folder:
            self.connfd.send(b"Fail")
            return
        else:
            self.connfd.send(b"OK")
            with open(FTP + ufile, "wb") as fw:
                while True:
                    data = self.connfd.recv(1024)
                    if data == b"##":
                        self.connfd.send("上传成功".encode())
                        break
                    fw.write(data)


    def run(self):
        while True:
            data = self.connfd.recv(1024)
            print(data.decode())
            msg = data.decode().split(" ")
            if msg[0] == "Q":
                self.connfd.close()
                return
            elif msg[0] == "L":
                self.do_list()
            elif msg[0] == "D":
                self.do_download(msg[1])
            elif msg[0] == "U":
                self.do_uploading(msg[1])


def main():
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(server_address)
    sockfd.listen(5)
    while True:
        try:
            connfd, addr = sockfd.accept()
        except KeyboardInterrupt:
            break
        t = FTPServer(connfd)
        t.setDaemon(True)
        t.start()
    sockfd.close()


if __name__ == '__main__':
    main()
