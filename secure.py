import mysql.connector
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="password_manager"
)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS vault (
    id INT AUTO_INCREMENT PRIMARY KEY,
    site VARCHAR(255),
    username VARCHAR(255),
    password TEXT
)
""")
conn.commit()


salt = b"mon_salt_fixe_et_unique"


MASTER_PASSWORD = Prompt.ask("Mot de passe maitre", password=True)

# Génération clé Fernet
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=390000,
)
key = base64.urlsafe_b64encode(kdf.derive(MASTER_PASSWORD.encode()))
cipher = Fernet(key)

console.print("[green]Mot de passe maitre accepte[/green]\n")


def verify_master():
    try:
        c.execute("SELECT password FROM vault LIMIT 1")
        row = c.fetchone()
        if row:
            
            cipher.decrypt(row[0].encode())
        return True
    except (InvalidToken, TypeError):
        return True  
    except Exception:
        return False

if not verify_master():
    console.print("[red]Mot de passe maitre incorrect ou base corrompue[/red]")
    exit()


def add_password(site, username, pwd):
    encrypted_pwd = cipher.encrypt(pwd.encode())
    c.execute("INSERT INTO vault (site, username, password) VALUES (%s, %s, %s)",
              (site, username, encrypted_pwd.decode()))
    conn.commit()
    console.print(f"[green][+] Mot de passe ajoute pour {site}[/green]")
    Prompt.ask("Appuyez sur Entrée pour continuer")

def get_password(site):
    c.execute("SELECT username, password FROM vault WHERE site=%s", (site,))
    row = c.fetchone()
    if row:
        username, encrypted_pwd = row
        try:
            decrypted_pwd = cipher.decrypt(encrypted_pwd.encode()).decode()
            console.print(f"[bold]Site:[/bold] {site}\n[bold]User:[/bold] {username}\n[bold]Password:[/bold] {decrypted_pwd}")
        except InvalidToken:
            console.print("[red][-] Impossible de dechiffrer le mot de passe (mauvais mot de passe maitre?)[/red]")
    else:
        console.print("[red][-] Aucun mot de passe trouve pour ce site[/red]")
    Prompt.ask("Appuyez sur Entrée pour continuer")

def list_sites():
    c.execute("SELECT site FROM vault")
    rows = c.fetchall()
    if rows:
        table = Table(title="Sites enregistres")
        table.add_column("Site", justify="left")
        for r in rows:
            table.add_row(r[0])
        console.print(table)
    else:
        console.print("[red][-] Aucun site enregistre[/red]")
    Prompt.ask("Appuyez sur Entrée pour continuer")


while True:
    table = Table(title="Password Manager")
    table.add_column("Option", justify="center")
    table.add_column("Action", justify="left")
    table.add_row("1", "Ajouter un mot de passe")
    table.add_row("2", "Recuperer un mot de passe")
    table.add_row("3", "Lister les sites")
    table.add_row("4", "Quitter")
    console.print(table)

    choice = Prompt.ask("Choix", choices=["1","2","3","4"])

    if choice == "1":
        site = Prompt.ask("Site")
        username = Prompt.ask("Username")
        pwd = Prompt.ask("Password", password=True)
        add_password(site, username, pwd)
    elif choice == "2":
        site = Prompt.ask("Nom du site")
        get_password(site)
    elif choice == "3":
        list_sites()
    elif choice == "4":
        break

conn.close()
