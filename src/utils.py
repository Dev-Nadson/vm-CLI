import os
from dotenv import load_dotenv

load_dotenv()
wi_pass = os.getenv("WI_PASS")
root_pass = os.getenv("RT_PASS")

def verify_pass(password: str, username: str):
    if username == "root":
        return root_pass

    if username == "wiconsult":
        return wi_pass

    if password == None:
        return ValueError(f"Insira a senha do usuário: {username}")
    
    return password