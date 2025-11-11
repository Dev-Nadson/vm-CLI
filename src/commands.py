import typer
from SSHConfig import exec_command, send_archive, verify_folder_exists
from utils import verify_pass

app = typer.Typer()

@app.command()
def update_pec( 
    version: str = typer.Argument(..., help="Versão do PEC"),
    host: str = typer.Argument(..., help="O IP da máquina"), #os ... deixa obrigatório
    username: str = typer.Option("root", "--username", "-u", help="O usuário padrão da máquina"), 
    password: str = typer.Option(None, "--password", "-p", help="Senha do acesso SSH")
    ):

    command_reboot = f'sudo systemctl restart e-SUS-AB-PostgreSQL.service'
    command_update = f'sudo vmx update-pec -c -u "https://europa.nyc3.cdn.digitaloceanspaces.com/wi-pec-{version}.jar"'
    
    if password == None:
        password = verify_pass(password, username)

    #Adicionar o SUDO
    typer.secho("Conexão com sucesso!", fg=typer.colors.GREEN, bold=True)

    try:
        response, errors = exec_command(host, username, password, command_reboot)
        if response:
            typer.secho("O comando executado com sucesso:", fg=typer.colors.GREEN)
            typer.echo(response)
        
        if errors:
            typer.secho(f"O comando '{command_reboot}' retornou erros:", fg=typer.colors.GREEN)
            raise Exception(errors)

        response, errors = exec_command(host, username, password, command_update)

        if response:
            typer.secho("O comando executado com sucesso:", fg=typer.colors.GREEN)
            typer.echo(response)
        
        if errors:
            typer.secho("O comando '{command}' retornou erros:", fg=typer.colors.RED)
            typer.echo(errors)

    

    except (ValueError, Exception) as e:
        typer.echo(f"Erro de configuração: {e}")


@app.command()
def show_credentials(
    host: str = typer.Argument(..., help="O IP da máquina"), #os ... deixa obrigatório
    username: str = typer.Option("root", "--username", "-u", help="O usuário padrão da máquina"), 
    password: str = typer.Option(None, "--password", "-p", help="Senha do acesso SSH")
    ):

    command = "cat /opt/e-SUS/webserver/config/credenciais.txt"
    if password == None:
        password = verify_pass(password, username)

    typer.secho("Conexão com sucesso!", fg=typer.colors.GREEN, bold=True)

    try:
        response, errors = exec_command(host, username, password, command)

        if response:
            typer.secho("O comando executado com sucesso:", fg=typer.colors.GREEN)
            typer.echo(response)
        
        if errors:
            typer.secho("O comando '{command}' retornou erros:", fg=typer.colors.GREEN)
            typer.echo(errors)

    except (ValueError, Exception) as e:
        typer.echo(f"Erro de configuração: {e}")


@app.command()
def config_certificate(
    host: str = typer.Argument(..., help="O IP da máquina"), #os ... deixa obrigatório
    username: str = typer.Option("root", "--username", "-u", help="O usuário padrão da máquina"), 
    password: str = typer.Option(None, "--password", "-p", help="Senha do acesso SSH"),
    local_path: str = typer.Option(None, "--local-path", "-l", help="Caminho local do arquivo"),
    ):
    if password == None:
        password = verify_pass(password, username)
    
    if username == "root":
        try:
            verify_folder_exists(host, username, password)
            send_archive(host, username, password, local_path)

        except Exception as e:
            typer.echo(f"Falha no Upload: {e}")

    else:
        #Adicionar o SUDO
        try:
            verify_folder_exists(host, username, password)
            send_archive(host, username, password, local_path)

        except Exception as e:
            typer.echo(f"Falha no Upload: {e}")


@app.command()
def setup_proxmox_nginx():
    pass