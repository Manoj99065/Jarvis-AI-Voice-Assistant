import os

def open_vscode():
    path = "C:\\Users\\HP\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
    os.startfile(path)
    return "Opening VS Code."