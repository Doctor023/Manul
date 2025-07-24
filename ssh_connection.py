import paramiko

@staticmethod
def connect_ssh(server):
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            ssh.connect(
                hostname=server.ip,
                username=server.login,
                password=server.password
            )
            
            print("Успешное подключение! Введите команды (exit для выхода).")
                
        finally:
            ssh.close()
            
    except Exception as e:
        print(f"Ошибка: {e}")