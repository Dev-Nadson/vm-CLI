import paramiko
import typer
import os
from dotenv import load_dotenv

load_dotenv()
path = os.getenv("CERT_PATH")

def exec_command(host: str, username: str, password: str, command: str):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
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

def send_archive(host: str, username: str, password: str, local_path: str):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sftp_client = None

    try:
        client.connect(hostname=host, username=username, password=password)
        typer.secho("Conexão com sucesso!", fg=typer.colors.GREEN, bold=True)
        
        sftp_client = client.open_sftp()

        filename = os.path.basename(local_path)
        remote_file = os.path.join(path, filename)
        sftp_client.put(local_path, remote_file)

        typer.secho(f"Transferência concluída com sucesso: {local_path} -> {path}", fg=typer.colors.GREEN)

    except Exception as e:
        typer.secho(f"Falha na transferência SFTP:", fg=typer.colors.RED, bold=True)
        raise Exception(f"{e}")

    finally:
        if sftp_client:
            sftp_client.close()
        client.close()

def verify_folder_exists(host: str, username: str, password: str):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(hostname=host, username=username, password=password)

        stdin, stdout, stderr = client.exec_command(f"ls {path}")
        errors = stderr.read().decode().strip()

        if errors:
            stdin, stdout, stderr = client.exec_command(f"mkdir -p {path}")
            create_errors = stderr.read().decode().strip()
            
            if create_errors:
                typer.secho(f"Erro ao criar diretório:", fg=typer.colors.RED, bold=True)  
                raise Exception(f"{create_errors}")
        
        typer.secho("Diretório encontrado!", fg=typer.colors.GREEN, bold=True)
        return True

    except Exception as e:
        typer.secho(f"Erro ao verificar/criar diretório:", fg=typer.colors.RED, bold=True)  
        raise Exception(f"{e}")
    
    finally:
        client.close()

