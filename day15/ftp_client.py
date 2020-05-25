"""
    ftp客户端
"""
from socket import *
from time import sleep

server_address = ("127.0.0.1", 9999)


class FTPClient:
    """
        FTP客户端
    """
    def __init__(self, sockfd):
        self.sockfd = sockfd

    def do_list(self):
        """
            查看文件库所有文件
        """
        msg = "L"
        self.sockfd.send(msg.encode())
        data = self.sockfd.recv(128).decode()
        if data == "OK":
            files = self.sockfd.recv(1024 * 1024)
            print(files.decode())
        else:
            print("文件库为空")

    def do_download(self, dfile, where):
        """
            下载文件库内容
        :param dfile: 需要下载的文件
        :param where: 下载文件存放的位置
        """
        msg = "D " + dfile
        self.sockfd.send(msg.encode())
        data = self.sockfd.recv(128).decode()
        if data == "OK":
            with open(where, "wb") as fw:
                while True:
                    file = self.sockfd.recv(1024)
                    if file == b"##":
                        break
                    fw.write(file)
        else:
            print("没有该文件")

    def do_uploading(self, file):
        ufile = file.split("/")[-1]
        msg = "U " + ufile
        self.sockfd.send(msg.encode())
        data = self.sockfd.recv(128).decode()
        if data == "OK":
            with open(file, "rb") as fr:
                while True:
                    data = fr.read(1024)
                    if not data:
                        sleep(0.1)
                        self.sockfd.send(b"##")
                        print(self.sockfd.recv(128).decode())
                        break
                    self.sockfd.send(data)
        else:
            print("文件名已存在")

    def do_quit(self):
        self.sockfd.send(b"Q")
        self.sockfd.close()
        print("感谢使用")
        return

def main():
    sockfd = socket()
    sockfd.connect(server_address)
    ftp = FTPClient(sockfd)
    while True:
        print("""
                █▔▔▔▔▔▔▔▔▔▔▔▔▔▔ORDER▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔█
                ┃                                  ┃
                ┃             l-list               ┃
                ┃             d-download           ┃
                ┃             u-uploading          ┃
                ┃             q-quit               ┃
                █▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁█
              """)

        cmd = input("请输入指令：")
        if cmd == "l":
            ftp.do_list()
        elif cmd == "d":
            dfile = input("请输入要下载的文件：")
            where = input("请输入下载位置：")
            ftp.do_download(dfile, where)
        elif cmd == "u":
            ufile = input("请输入要上传的文件：")
            ftp.do_uploading(ufile)
        elif cmd == "q":
            ftp.do_quit()
            break
        else:
            print("输入错误，请重新输入")
            continue


if __name__ == '__main__':
    main()
