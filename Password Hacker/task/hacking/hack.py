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
    while chr_count < 8:
        for first in itertools.product(psw_list, repeat=chr_count):
            if i > len(psw_list) ** chr_count: break
            cur_psw = "".join(first)
            cli_socket.send(cur_psw.encode())
            recv_data = cli_socket.recv(1024).decode()
            if recv_data == "Connection success!":
                print(cur_psw)
                chr_count = 999
                break
            elif recv_data == "Too many attempts":
                print("Too many attempts")
                chr_count = 999
                break
            i += 1
        chr_count += 1





