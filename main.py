import os
import getpass
import start_page
import ssh_connection
import page_with_not_installed_xray
import page_with_installed_xray

while True:
    server = start_page.account_message()
    ssh = ssh_connection.connect_ssh(server)
    if ssh != False:
        break

xray_installed = ssh_connection.check_xray(ssh)
if xray_installed:
    print("Xray установлен")
    digit = page_with_installed_xray.digit_input()
    if digit == 1:
        print("Пользователь добавлен")
else:
    digit = page_with_not_installed_xray.digit_input()
    if digit in ('1'):
        ssh_connection.install_xray(ssh)