import paramiko
import re
from colorama import  init, Fore
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
        stdin, stdout, stderr = ssh.exec_command("apt update -y")
        output = stdout.read().decode().strip()
        print(output)
        

        stdin, stdout, stderr = ssh.exec_command("apt install curl -y")
        output = stdout.read().decode().strip()


        stdin, stdout, stderr = ssh.exec_command("bash -c \"$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)\" @ install")
        output = stdout.read().decode().strip()
        print(output)

        stdin, stdout, stderr = ssh.exec_command("touch /usr/local/etc/xray/users.json") # add users.json 
        stdin, stdout, stderr = ssh.exec_command('echo "{}" > /usr/local/etc/xray/users.json')

    except Exception as e:
        print(f"Ошибка при подключении или выполнении команды: {e}")

@staticmethod
def generate_keys(ssh):
    

    stdin, stdout, stderr = ssh.exec_command("xray x25519")
    keys = stdout.read().decode().strip()

    pattern_private_key = r"PrivateKey:\s*([A-Za-z0-9_-]+)"
    pattern_public_key = r"Password:\s*([A-Za-z0-9_-]+)"

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
        sftp = ssh.open_sftp()
        with sftp.file('/usr/local/etc/xray/config.json', 'w') as remote_file:
            remote_file.write(updated_config)

        with sftp.file('/usr/local/etc/xray/public_key.json', 'w') as remote_file:
                remote_file.write(public_key)

    stdin, stdout, stderr = ssh.exec_command("rm /usr/local/etc/xray/users.json") 
    stdin, stdout, stderr = ssh.exec_command("touch /usr/local/etc/xray/users.json") # add users.json 
    stdin, stdout, stderr = ssh.exec_command('echo "{}" > /usr/local/etc/xray/users.json')

    stdin, stdout, stderr = ssh.exec_command("systemctl restart xray")
    print("Ключи сгенерированы")

@staticmethod
def find_users(ssh):

    existing_data = json
    sftp = ssh.open_sftp()
    with sftp.file('/usr/local/etc/xray/users.json', 'r') as remote_file: 
            existing_data = json.load(remote_file)
    users_count = len(existing_data)
    if users_count != 0:
        print(f"Всего пользователей: {users_count}")
        i = 1
        for uuid, username in existing_data.items():
            print(f"{i}. {username}")
            i = i + 1
    else:
        print("Всего пользователей: 0")
    return existing_data

@staticmethod
def check_private_key(ssh):
    stdin, stdout, stderr = ssh.exec_command("cat /usr/local/etc/xray/config.json")
    config = stdout.read().decode('utf-8') 
    pattern = r'"privateKey"\s*:\s*"([^"]+)"'
    matches = re.findall(pattern, config)
    
    if matches:
        return matches[0]
    else:
        print("Приватный ключ не найден в конфигурации")
        return None
    
@staticmethod
def add_user(ssh, server_ip, user):

        stdin, stdout, stderr = ssh.exec_command("xray uuid")
        uuid = stdout.read().decode('utf-8').strip()
        
        stdin, stdout, stderr = ssh.exec_command("cat /usr/local/etc/xray/config.json")
        config = stdout.read().decode('utf-8')   


        updated_config = config.replace("EMPTY", uuid, 1)
        sftp = ssh.open_sftp()
        with sftp.file('/usr/local/etc/xray/config.json', 'w') as remote_file:
            remote_file.write(updated_config)

        user_dict = {uuid : user}     
        with sftp.file('/usr/local/etc/xray/users.json', 'r') as remote_file: 
            existing_data = json.load(remote_file)
            existing_data.update(user_dict)

        with sftp.file('/usr/local/etc/xray/users.json', 'w') as remote_file: # changes in users.json
            json_str = json.dumps(existing_data, ensure_ascii=False, indent=2)
            remote_file.write(json_str)


        print(f"Успешно добавлен пользователь {user} с UUID: {uuid}")

        stdin, stdout, stderr = ssh.exec_command("cat /usr/local/etc/xray/public_key.json")
        public_key = stdout.read().decode('utf-8')       

        print("Необходимо вставить ссылку в VLESS клиент:")
        print(Fore.GREEN + f"vless://{uuid}@{server_ip}:443?security=reality&sni=google.com&alpn=h2&fp=chrome&pbk={public_key}&pbk=su1LPoVoA44umUYDWskmuEwAvGvx9bg8nVfiSgK3Fiw&sid=aabbccdd&type=tcp&flow=xtls-rprx-vision&encryption=none#{user}" + Fore.RESET)

        stdin, stdout, stderr = ssh.exec_command("systemctl restart xray")

@staticmethod
def delete_user(ssh, digit, users):
    if digit != 0:
        digit = digit - 1

    items_list = list(users.items())
    uuid, username = items_list[digit]
    stdin, stdout, stderr = ssh.exec_command("cat /usr/local/etc/xray/config.json")
    config = stdout.read().decode('utf-8')   
    updated_config = config.replace(uuid, "EMPTY", 1)
    sftp = ssh.open_sftp()
    with sftp.file('/usr/local/etc/xray/config.json', 'w') as remote_file:
        remote_file.write(updated_config)
    
    users.pop(uuid)
        
    with sftp.file('/usr/local/etc/xray/users.json', 'w') as remote_file:
        json_str = json.dumps(users, ensure_ascii=False, indent=2)
        remote_file.write(json_str)

    stdin, stdout, stderr = ssh.exec_command("systemctl restart xray")

    print(f"Пользователь {username} удален")
