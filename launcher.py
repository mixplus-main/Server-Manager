launcher_ver = "1_0_0"

import os
import sys
import urllib.request
import subprocess
import tkinter as tk
from tkinter import messagebox
import shutil
import json
import time
import webbrowser

SERVER_DIR = os.path.join(os.path.dirname(__file__), "Manager")
EXE_NAME = "ServerManager.exe"
EXE_PATH = os.path.join(SERVER_DIR, EXE_NAME)
# GitHub API で最新リリースの exe を取得
RELEASE_API_URL = "https://api.github.com/repos/mixplus-main/Server-Manager/releases/latest"

def show_error(msg):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("エラー", msg)
    root.destroy()

def download_latest(url):
    try:
        os.makedirs(SERVER_DIR, exist_ok=True)
        tmp_path = os.path.join(SERVER_DIR, "ServerManager_tmp.exe")
        urllib.request.urlretrieve(url, tmp_path)
        shutil.move(tmp_path, EXE_PATH)
    except Exception as e:
        show_error(f"ServerManager.exe のダウンロードに失敗しました:\n{e}")
        sys.exit(1)

def get_latest_release_url():
    try:
        with urllib.request.urlopen(RELEASE_API_URL) as response:
            data = json.load(response)
            for asset in data.get("assets", []):
                if asset["name"].endswith(".exe"):
                    return asset["browser_download_url"]
        show_error("最新版のリリースを取得できませんでした。")
        sys.exit(1)
    except Exception as e:
        show_error(f"リリース情報取得に失敗:\n{e}")
        sys.exit(1)

def launch_exe():
    try:
        subprocess.Popen([EXE_PATH], cwd=SERVER_DIR)
    except Exception as e:
        show_error(f"ServerManager.exe の起動に失敗しました:\n{e}")
        sys.exit(1)

def main():
    latest_url = get_latest_release_url()

    # EXE がなければダウンロード
    if not os.path.exists(EXE_PATH):
        download_latest(latest_url)
    else:
        # 常に最新版に置き換え
        download_latest(latest_url)

    # 起動
    launch_exe()

if __name__ == "__main__":
    main()
