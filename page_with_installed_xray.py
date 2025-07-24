import sys
import os


def digit_input():
    while True:
        if os.name == 'nt':  # Windows
            import msvcrt
            char = msvcrt.getch().decode('utf-8') 
        else:  # Unix/Linux/macOS
            import termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                new_settings = termios.tcgetattr(fd)
                new_settings[3] = new_settings[3] & ~termios.ICANON 
                termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)
                char = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        
        if char in ('1', '2', '3', '4'):
            return char