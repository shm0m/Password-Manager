import PySimpleGUI as sg

layout = [[sg.Text("Hello World")], [sg.Button("OK")]]
window = sg.Window("Secure GUI", layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "OK":
        break
