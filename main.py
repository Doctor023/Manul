import start_page
import ssh_connection
import page_with_not_installed_xray
import page_with_installed_xray
from termcolor import colored

logged = False

while True:
    # Подключаемся к серверу (если ещё не подключены)
    if not logged:
        server = start_page.account_message()
        ssh = ssh_connection.connect_ssh(server)
        if ssh is False:
            continue  # Переподключение, если SSH не удалось

    # Проверяем, установлен ли XRay
    xray_installed = ssh_connection.check_xray(ssh)

    if xray_installed:
        logged = True  # Помечаем, что вход выполнен
        print(colored("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", 'yellow'))
        print("""1. Добавить пользователя
2. Удалить пользователя
3. Список пользователей
4. Сгенерировать/Перегенерировать ключи (все пользователи будут удалены)""")
        print(colored("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", 'yellow'))

        digit = page_with_installed_xray.digit_input()

        if digit == '1':
            private_key = ssh_connection.check_private_key(ssh)
            if private_key == "YOUR_PRIVATE_KEY":
                print("Сначала сгенерируйте ключи")
            else:
                ssh_connection.add_user(ssh, server.ip)

        elif digit == '2':
            while True:
                uuids = ssh_connection.find_users(ssh)
                print("Введите номер пользователя для удаления или напишите exit")
                digit = input()
                if digit.lower() == 'exit':
                    break
                try:
                    digit_int = int(digit)
                    if 1 <= digit_int <= len(uuids):
                        ssh_connection.delete_user(ssh, digit_int, uuids)
                        break  # Выход после удаления
                    else:
                        print("Пользователь с таким номером отсутствует")
                except ValueError:
                    print("Пожалуйста, введите номер или 'exit'")

        elif digit == '3':
            ssh_connection.find_users(ssh)  # Просто выводим список

        elif digit == '4':
            ssh_connection.generate_keys(ssh)

    else:
        # Если XRay не установлен, предлагаем установить
        digit = page_with_not_installed_xray.digit_input()
        if digit == '1':
            ssh_connection.install_xray(ssh)
            ssh_connection.generate_keys(ssh)
            logged = True  # После установки помечаем вход как выполненный