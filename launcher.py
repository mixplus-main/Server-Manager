import os
import sys
import urllib.request
import subprocess
import tkinter.messagebox as mbox

MANAGER_DIR = "Manager"
SERVER_EXE = os.path.join(MANAGER_DIR, "ServerManager.exe")
URL = "https://github.com/mixplus-main/Server-Manager/releases/latest/download/ServerManager.exe"

def error(msg):
    mbox.showerror("Launcher Error", msg)
    sys.exit(1)

def main():
    try:
        os.makedirs(MANAGER_DIR, exist_ok=True)
    except Exception as e:
        error(f"フォルダ作成失敗\n{e}")

    try:
        urllib.request.urlretrieve(URL, SERVER_EXE)
    except Exception as e:
        error(f"ServerManager のダウンロードに失敗しました\n{e}")

    try:
        subprocess.Popen([SERVER_EXE], cwd=MANAGER_DIR)
    except Exception as e:
        error(f"ServerManager を起動できません\n{e}")

    sys.exit()

if __name__ == "__main__":
    main()
