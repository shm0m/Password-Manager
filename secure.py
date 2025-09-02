import PySimpleGUI as sg
import mysql.connector
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

conn = mysql.connector.connect(host="localhost", user="root", password="", database="password_manager")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS vault (id INT AUTO_INCREMENT PRIMARY KEY, site VARCHAR(255), username VARCHAR(255), password TEXT)")
conn.commit()

sg.theme("DarkTeal9")

layout_master = [
    [sg.Text("Enter Master Password", font=("Helvetica", 14))],
    [sg.Input(password_char="*", key="-MASTER-")],
    [sg.Button("Submit", size=(10,1))]
]
window_master = sg.Window("Secure", layout_master)

while True:
    event, values = window_master.read()
    if event == sg.WIN_CLOSED:
        conn.close()
        exit()
    elif event == "Submit":
        master_password = values["-MASTER-"]
        break
window_master.close()

salt = b"static_salt_change_me"
kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=390000)
key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
cipher = Fernet(key)

def add_password(site, username, pwd):
    encrypted_pwd = cipher.encrypt(pwd.encode())
    c.execute("INSERT INTO vault (site, username, password) VALUES (%s,%s,%s)", (site, username, encrypted_pwd.decode()))
    conn.commit()
    sg.popup("Password added for", site)

def get_password(site):
    c.execute("SELECT username, password FROM vault WHERE site=%s", (site,))
    row = c.fetchone()
    if row:
        username, encrypted_pwd = row
        decrypted_pwd = cipher.decrypt(encrypted_pwd.encode()).decode()
        sg.popup(f"Site: {site}\nUser: {username}\nPassword: {decrypted_pwd}")
    else:
        sg.popup("No password found for this site")

def list_sites():
    c.execute("SELECT site FROM vault")
    rows = c.fetchall()
    if rows:
        sg.popup_scrolled("Saved Sites", "\n".join(r[0] for r in rows))
    else:
        sg.popup("No sites saved")

def update_password(site, new_pwd):
    encrypted_pwd = cipher.encrypt(new_pwd.encode())
    c.execute("UPDATE vault SET password=%s WHERE site=%s", (encrypted_pwd.decode(), site))
    conn.commit()
    sg.popup("Password updated for", site)

def delete_password(site):
    c.execute("DELETE FROM vault WHERE site=%s", (site,))
    conn.commit()
    sg.popup("Password deleted for", site)

layout_main = [
    [sg.Text("Secure Password Manager", font=("Helvetica", 18), justification="center", expand_x=True)],
    [sg.Button("Add Password", size=(25,1)), sg.Button("Retrieve Password", size=(25,1))],
    [sg.Button("Update Password", size=(25,1)), sg.Button("Delete Password", size=(25,1))],
    [sg.Button("List Sites", size=(25,1)), sg.Button("Quit", size=(25,1))]
]

window_main = sg.Window("Secure", layout_main, element_justification="center", finalize=True)

while True:
    event, values = window_main.read()
    if event in (sg.WIN_CLOSED, "Quit"):
        break
    elif event == "Add Password":
        layout_add = [
            [sg.Text("Site"), sg.Input(key="-SITE-")],
            [sg.Text("Username"), sg.Input(key="-USER-")],
            [sg.Text("Password"), sg.Input(password_char="*", key="-PWD-")],
            [sg.Button("Submit"), sg.Button("Cancel")]
        ]
        window_add = sg.Window("Add Password", layout_add)
        e, v = window_add.read()
        if e == "Submit":
            add_password(v["-SITE-"], v["-USER-"], v["-PWD-"])
        window_add.close()
    elif event == "Retrieve Password":
        layout_get = [[sg.Text("Site Name"), sg.Input(key="-SITEGET-")], [sg.Button("Submit"), sg.Button("Cancel")]]
        window_get = sg.Window("Retrieve Password", layout_get)
        e, v = window_get.read()
        if e == "Submit":
            get_password(v["-SITEGET-"])
        window_get.close()
    elif event == "List Sites":
        list_sites()
    elif event == "Update Password":
        layout_upd = [
            [sg.Text("Site Name"), sg.Input(key="-SITEMOD-")],
            [sg.Text("New Password"), sg.Input(password_char="*", key="-PWDNEW-")],
            [sg.Button("Submit"), sg.Button("Cancel")]
        ]
        window_upd = sg.Window("Update Password", layout_upd)
        e, v = window_upd.read()
        if e == "Submit":
            update_password(v["-SITEMOD-"], v["-PWDNEW-"])
        window_upd.close()
    elif event == "Delete Password":
        layout_del = [[sg.Text("Site Name"), sg.Input(key="-SITEDEL-")], [sg.Button("Submit"), sg.Button("Cancel")]]
        window_del = sg.Window("Delete Password", layout_del)
        e, v = window_del.read()
        if e == "Submit":
            delete_password(v["-SITEDEL-"])
        window_del.close()

window_main.close()
conn.close()
