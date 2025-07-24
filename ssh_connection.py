import paramiko
import re
import json

@staticmethod
def connect_ssh(server):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(
            hostname=server.ip,
            username=server.login,
            password=server.password
        )
        return ssh
            
    except Exception as e:
        print(f"Ошибка: {e}")
        return False

@staticmethod
def check_xray(ssh):
    try:
        stdin, stdout, stderr = ssh.exec_command("whereis xray")
        output = stdout.read().decode().strip()
        if not output or "xray:" in output and len(output.split()) == 1:
            return False
        return True
        
    except Exception as e:
        print(f"Ошибка при подключении или выполнении команды: {e}")

@staticmethod
def install_xray(ssh):
    try:
        print("xray устанавливается...")
        stdin, stdout, stderr = ssh.exec_command("apt update -y")
        output = stdout.read().decode().strip()
        print(output)
        

        tdin, stdout, stderr = ssh.exec_command("apt install curl -y")
        output = stdout.read().decode().strip()


        stdin, stdout, stderr = ssh.exec_command("bash -c \"$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)\" @ install")
        output = stdout.read().decode().strip()
        print(output)
        print("xray установлен")
    except Exception as e:
        print(f"Ошибка при подключении или выполнении команды: {e}")

@staticmethod
def generate_keys(ssh):
    config = ""
    with open('config.json', 'r', encoding='utf-8') as file:
        for chunk in file:
            config += chunk
        sftp = ssh.open_sftp()
        with sftp.file('/usr/local/etc/xray.config.json', 'w') as remote_file:
            remote_file.write(config)
        print ("Конфиг обновлен")
    stdin, stdout, stderr = ssh.exec_command("xray x25519")
    keys = stdout.read().decode().strip()
    print(keys)

@staticmethod
def find_users(ssh):
    try:
        stdin, stdout, stderr = ssh.exec_command("cat /usr/local/etc/xray.config.json")
        content = stdout.read().decode('utf-8')  
        errors = stderr.read().decode('utf-8')
        
        if errors:
            print(f"Ошибка: {errors}")
            return


        uuid_pattern = r'"id"\s*:\s*"([^"]+)"'
        matches = re.findall(uuid_pattern, content)

        valid_uuids = [uuid for uuid in matches if len(uuid) == 36]
        
        print(f"Найдено ID: {len(matches)}")
        print(f"Валидных UUID: {len(valid_uuids)}")
        print("\nЗначения ID:")
        for i, uuid in enumerate(matches, 1):
            print(f"{i}. {uuid}")

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

@staticmethod
def check_private_key(ssh):
    stdin, stdout, stderr = ssh.exec_command("cat /usr/local/etc/xray.config.json")
    config = stdout.read().decode('utf-8') 
    pattern = r'"privateKey"\s*:\s*"([^"]+)"'
    matches = re.findall(pattern, config)
    
    if matches:
        return matches[0]
    else:
        print("Приватный ключ не найден в конфигурации")
        return None
    
