import paramiko
import subprocess

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
        print("xray устанавливается")
        stdin, stdout, stderr = ssh.exec_command("apt update -y")
        output = stdout.read().decode().strip()
        
        stdin, stdout, stderr = ssh.exec_command("bash -c \"$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)\" @ install")
        output = stdout.read().decode().strip()
        
    except Exception as e:
        print(f"Ошибка при подключении или выполнении команды: {e}")