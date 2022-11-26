import socket
import argparse
import string
import itertools
import time
psw_list = (list(string.ascii_lowercase) + list(string.digits))

argums = argparse.ArgumentParser("ip, port")
argums.add_argument("ip_address")
argums.add_argument("port")

str_arg = argums.parse_args()

start_time = time.time()

with socket.socket() as cli_socket:
    cli_socket.connect((str_arg.ip_address, int(str_arg.port)))
    i = 0
    n = 1
    while n < 8:
        for first in itertools.product(psw_list, repeat=n):
            if i > len(psw_list) ** n: break
            cur_psw = "".join(first)
            cli_socket.send(cur_psw.encode())
            recv_data = cli_socket.recv(1024).decode()
            if recv_data == "Connection success!":
                # print("Connection success!")
                print(cur_psw)
                n = 999
                break
            elif recv_data == "Too many attempts":
                print("Too many attempts")
                break
                n = 999
            i += 1
        n += 1





