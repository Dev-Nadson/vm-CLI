import typer
from SSHConfig import exec_command
from utils import verify_pass

app = typer.Typer()

@app.command()
def show_credentials(
    host: str = typer.Argument(..., help="O IP da máquina"), #os ... deixa obrigatório
    username: str = typer.Option("root", "--username", "-u", help="O usuário padrão da máquina"), 
    password: str = typer.Option(None, "--password", "-p", help="Senha do acesso SSH")
    ):

    command = "cat /opt/e-SUS/webserver/config/credenciais.txt"
    password = verify_pass(password, username)

    typer.echo("Conexão com sucesso")

    try:
        response, errors = exec_command(host, username, password, command)

        if response:
            print(f"O comando executado com sucesso:")
            print(response)
        
        if errors:
            print(f"O comando '{command}' retornou erros:")
            print(errors)

    except (ValueError, Exception) as e:
        print(f"Erro de configuração: {e}")


@app.command()
def config_certificate(
    host: str = typer.Argument(..., help="O IP da máquina"), #os ... deixa obrigatório
    username: str = typer.Option("root", "--username", "-u", help="O usuário padrão da máquina"), 
    password: str = typer.Option(None, "--password", "-p", help="Senha do acesso SSH")
    ):

    if username == "root":
        command = ""

@app.command()
def setup_proxmox_nginx():
    pass