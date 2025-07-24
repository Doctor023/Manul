import sys
import os


def digit_input():
    print("""1. Добавить пользователя
          2. Удалить пользователя
          3. Перегенерировать ключ(uuid всех пользоваталей обновится, необходимо будет заменить конфиг всем)""")
    while True:
        if os.name == 'nt':  # Windows
            import msvcrt
            char = msvcrt.getch().decode('utf-8')  # Байты -> строка
        else:  # Unix/Linux/macOS
            import termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                new_settings = termios.tcgetattr(fd)
                new_settings[3] = new_settings[3] & ~termios.ICANON  # Отключаем буферизацию
                termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)
                char = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        
        if char in ('1', '2', '3'):
            return char