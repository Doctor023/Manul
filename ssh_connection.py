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
    

    stdin, stdout, stderr = ssh.exec_command("xray x25519")
    keys = stdout.read().decode().strip()

    pattern_private_key = r"Private key:\s*([A-Za-z0-9_-]+)"
    pattern_public_key = r"Public key:\s*([A-Za-z0-9_-]+)"

    match_private_key = re.search(pattern_private_key, keys)
    private_key = match_private_key.group(1)

    match_public_key = re.search(pattern_public_key, keys)
    public_key = match_public_key.group(1)

    config = ""
    with open('config.json', 'r', encoding='utf-8') as file:
        for chunk in file:
            config += chunk
            updated_config = re.sub(
                r'("privateKey"\s*:\s*")YOUR_PRIVATE_KEY(")',
                fr'\g<1>{private_key}\g<2>',
                config)
        print(updated_config)
        sftp = ssh.open_sftp()
        with sftp.file('/usr/local/etc/xray/config.json', 'w') as remote_file:
            remote_file.write(updated_config)

        with sftp.file('/usr/local/etc/xray/public_key.json', 'w') as remote_file:
                remote_file.write(public_key)
    

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
        
        print(f"Всего пользователей: {len(valid_uuids)}")
        print("\nUUID:")
        for i, uuid in enumerate(matches, 1):
            print(f"{i}. {valid_uuids}")

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
    
@staticmethod
def add_user(ssh, server_ip):

    # Генерация UUID
        stdin, stdout, stderr = ssh.exec_command("xray uuid")
        uuid = stdout.read().decode('utf-8').strip()
        
        stdin, stdout, stderr = ssh.exec_command("cat /usr/local/etc/xray/config.json")
        config = stdout.read().decode('utf-8')   


        print(config)
        updated_config = config.replace("EMPTY", uuid, 1)
        print(updated_config)
        sftp = ssh.open_sftp()
        with sftp.file('/usr/local/etc/xray/config.json', 'w') as remote_file:
            remote_file.write(updated_config)
        print(f"Успешно добавлен пользователь с UUID: {uuid}")

        stdin, stdout, stderr = ssh.exec_command("cat /usr/local/etc/xray/public_key.json")
        public_key = stdout.read().decode('utf-8')       
        print("Необходимо вставить конфиг в VLESS клиент: " + f"vless://{uuid}@{server_ip}:443?security=reality&sni=google.com&alpn=h2&fp=chrome&pbk={public_key}&encryption=none#manul")