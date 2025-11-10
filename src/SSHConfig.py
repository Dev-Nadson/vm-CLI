import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def exec_command(host: str, username: str, password: str, command: str):
    try:
        client.connect(hostname=host, username=username, password=password)
        
        stdin, stdout, stderr = client.exec_command(command)

        response = stdout.read().decode().strip()
        errors = stderr.read().decode().strip()

        return response, errors

    except (paramiko.AuthenticationException, paramiko.SSHException) as e: 
        print(f"Falha no acesso SSH. Detalhe: {e}")

    finally:
        client.close()

def send_archive(host: str, username: str, password: str, local_path: str, remote_path: str):
    
    sftp_client = None
    try:
        client.connect(hostname=host, username=username, password=password)

        sftp_client = client.open_sftp()
        sftp_client.put(local_path, remote_path)

        print(f"Transferência concluída com sucesso: {local_path} -> {remote_path}")

    except Exception as e:
        raise Exception(f"Falha na transferência SFTP: {e}")

    finally:
        if sftp_client:
            sftp_client.close()
        client.close()

