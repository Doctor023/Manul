import pwinput


def account_message():
    ip = input("Введите IP адрес сервера: ").strip()
    login = input("Введите логин: ").strip()
    password = pwinput.pwinput("Введите пароль: ", mask='*')
    server = Server(ip, login, password)
    return server

class Server:
    def __init__(self, ip, login, password):
        self.login = login
        self.ip = ip
        self.password = password