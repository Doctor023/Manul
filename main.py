import os
import getpass
import start_page
import ssh_connection
import page_with_not_installed_xray
import page_with_installed_xray
from termcolor import colored, cprint


while True:
    server = start_page.account_message()
    ssh = ssh_connection.connect_ssh(server)
    if ssh != False:
        break

xray_installed = ssh_connection.check_xray(ssh)
if xray_installed:
    print(colored("Xray на сервере уже установлен",'green'))
    while True:
        
        print("""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Добавить пользователя
2. Удалить пользователя
3. Список пользователей
4. Сгенерировать/Перегенерировать ключи (все пользователи будут удалены)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")
        digit = page_with_installed_xray.digit_input()
        if digit == '1':
            private_key = ssh_connection.check_private_key(ssh)
            if private_key == "YOUR_PRIVATE_KEY":
                print("Сначала сгенерируйте ключи")
            else:
                ssh_connection.add_user(ssh, server.ip)


        if digit == '2':
             digit = print("Введите номер пользователя для удаления или напишите exit")
             uuids = ssh_connection.find_users(ssh)
             while True:
                if digit is int:
                    if digit <= len(uuids):
                        ssh_connection.delete_user(ssh, digit, uuids)
                    else:
                        print("Пользователь с таким номером отсутствует")
                break
                 

        if digit == '3':
            promt = ssh_connection.find_users(ssh) # promt is the value for the method to work
        if digit == '4':   
            ssh_connection.generate_keys(ssh)
else:
    digit = page_with_not_installed_xray.digit_input()
    if digit in ('1'):
        ssh_connection.install_xray(ssh)