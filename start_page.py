import pwinput
import msvcrt

def account_message():
    ip = input("Введите IP адрес сервера: ").strip()
    login = input("Введите логин: ").strip()
    if login != "root":
        is_root = root_warning()
        if is_root:
            login = "root"
    password = pwinput.pwinput("Введите пароль: ", mask='*')
    server = Server(ip, login, password)
    return server
    
class Server:
    def __init__(self, ip, login, password):
        self.login = login
        self.ip = ip
        self.password = password

def root_warning():
    print("Вы собираетесь войти не под пользователем root, для корректной работы скрипта необходимы права администратора, они есть у текущего пользователя?")
    print("""1. Нет, войти под root
2. Да, я подтверждаю, что заблаговременно повысил права пользователю""")
    char = msvcrt.getch().decode('utf-8')
    if char == '1':
        return True
    if char == '2':
        return False