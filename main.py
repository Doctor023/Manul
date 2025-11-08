import start_page
import ssh_connection
import page_with_not_installed_xray
import page_with_installed_xray
from colorama import  init, Fore

logged = False

while True:
    # Connect to the server (if not already connected)
    if not logged:
        server = start_page.account_message()
        ssh = ssh_connection.connect_ssh(server)
        if ssh is False:
            continue  # Retry if SSH connection failed

    # Check if XRay is installed
    xray_installed = ssh_connection.check_xray(ssh)

    if xray_installed:
        logged = True  # Mark as logged in
        print(Fore.YELLOW + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" + Fore.RESET)
        print("""1. Добавить пользователя
2. Удалить пользователя
3. Список пользователей
4. Сгенерировать/Перегенерировать ключи (все пользователи будут удалены)""")
        print(Fore.YELLOW + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" + Fore.RESET)

        digit = page_with_installed_xray.digit_input()

        if digit == '1':
            private_key = ssh_connection.check_private_key(ssh)
            if private_key == "YOUR_PRIVATE_KEY":
                print("Сначала сгенерируйте ключи")
            else:
                user = input("Введите имя пользователя: ")
                ssh_connection.add_user(ssh, server.ip, user)

        elif digit == '2':
            while True:
                users = ssh_connection.find_users(ssh)
                print("Введите номер пользователя или напишите exit, чтобы выйти в меню'")
                digit = input()
                if digit.lower() == 'exit':
                    break
                try:
                    digit_int = int(digit)
                    if 1 <= digit_int <= len(users):
                        ssh_connection.delete_user(ssh, digit_int, users)
                    else:
                        print("Пользователя с таким номером не существует")
                except ValueError:
                    print("Введите номер пользователя или напишите 'exit'")

        elif digit == '3':
            ssh_connection.find_users(ssh)  # Simply display the list

        elif digit == '4':
            ssh_connection.generate_keys(ssh)

    else:
       
            digit = page_with_not_installed_xray.digit_input()

            if digit == '1':
                try:
                    # Attempt XRay installation
                    print("Установка XRay...")
                    
                    ssh_connection.install_xray(ssh)

                    # Generate keys after installation
                    print("Генерация ключей...")
                    ssh_connection.generate_keys(ssh)

                    logged = True  # Mark successful installation
                    print(Fore.GREEN + "XRay успешно установлен и настроен!" + Fore.RESET)

                except Exception as e:
                    print(Fore.RED + f"Ошибка: {str(e)}" + Fore.RESET)
                    logged = False