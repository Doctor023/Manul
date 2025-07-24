import sys
import os
    
@staticmethod
def digit_input():
    print("1. Установить xray")
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
        
        if char == '1': 
            return char

@staticmethod
def install_xray(ssh):
    try:
        stdin, stdout, stderr = ssh.exec_command("whereis xray")
        output = stdout.read().decode().strip()
        if not output or "xray:" in output and len(output.split()) == 1:
            return False
        return True
        
    except Exception as e:
        print(f"Ошибка при подключении или выполнении команды: {e}")