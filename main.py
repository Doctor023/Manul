import start_page
import ssh_connection
import page_with_not_installed_xray
import page_with_installed_xray
from termcolor import colored

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
                print("Generate keys first")
            else:
                ssh_connection.add_user(ssh, server.ip)

        elif digit == '2':
            while True:
                uuids = ssh_connection.find_users(ssh)
                print("Enter the user number to delete or type 'exit'")
                digit = input()
                if digit.lower() == 'exit':
                    break
                try:
                    digit_int = int(digit)
                    if 1 <= digit_int <= len(uuids):
                        ssh_connection.delete_user(ssh, digit_int, uuids)
                        break  # Exit after deletion
                    else:
                        print("No user with this number exists")
                except ValueError:
                    print("Please enter a number or 'exit'")

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
                    print(colored("XRay успешно установлен и настроен!", "green"))

                except Exception as e:
                    print(colored(f"Ошибка: {str(e)}", "red"))
                    logged = False