"""
Hello! Thank you for reading this documentation.

This file explains the basic rules and main APIs
used in ServerManager extensions.

====================
Basic Naming Rules
====================

- Functions end with an underscore (_)
  Example: btn_, add_log_

- Classes end with double underscores (__)
  Example: function__

Important Rules for Extensions
------------------------------

- Do NOT create a new Tk() window
- Do NOT call mainloop()
- Always use the existing manager instance:
    builtins.FUNC_INSTANCE


====================
Main Functions
====================

add_log_
--------
Displays a message in the log box.

Usage:
    add_log_("message", "color", "tab_name")

Arguments:
- message (str): Text to display
- color (str): Text color (e.g. "blue", "white")
- tab_name (str): Log tab name (e.g. "main", "help")


frame_
------
Creates a frame.

Usage:
    frame_(parent)

Arguments:
- parent: Parent widget (usually another frame or window)

Note:
- Usually used internally. No need to modify.


label_
-------
Creates a label.

Usage:
    label_(
        location,
        "text",
        bg="background color",
        fg="font color",
        font="font",
        layout_mode="layout mode",
        x=x,
        y=y
    )

Arguments:
- location: Parent frame
- text (str): Label text
- bg (str): Background color
- fg (str): Font color
- font: Font setting
- layout_mode (str): "pack", "place", or "grid"


log_box_
--------
Creates a log box.

Usage:
    log_box_()
    log_boxes["tab_name"] = log_box

Important:
- You must register the log box using:
      log_boxes["tab_name"] = log_box
- Otherwise, messages cannot be sent to that tab.


scrollbar_
-----------
Creates a scrollbar.

Usage:
    scrollbar_()


listbox_
---------
Creates a listbox.

Usage:
    listbox_(
        bg="background color",
        fg="font color",
        relief=None
    )


btn_
----
Creates a button.

Usage:
    btn_(
        parent,
        "text",
        command=function_to_execute,
        bg="background color",
        fg="font color",
        layout_mode=None,
        x=x,
        y=y,
        row=row,
        col=col
    )

Arguments:
- parent: Parent frame
- text (str): Button text
- command: Function to execute when clicked
- bg (str): Background color
- fg (str): Font color
- layout_mode (str):
    - None or "pack" : pack()
    - "place"        : uses x, y
    - "grid"         : uses row, col
"""

"""
temp Extensions
# Extensions/temp.py
import builtins
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ServerManager1_4_0 import function__

id = "temp"

manager: "function__" = builtins.FUNC_INSTANCE


def show_temp_frame():
    # フレーム作成
    manager.frame_(manager.win)
    manager.label_("Temp Frame")
    manager.log_box_()
    manager.scrollbar_()

    # temp タブとして登録
    manager.log_boxes["temp"] = manager.log_box

    # フレーム表示
    manager.show_frame(manager.frame)

    # ログ出力
    manager.add_log_("temp frame!", "blue", "temp")


# ボタン追加（Main などに置く）
manager.btn_(
    manager.frame_main,
    "Temp",
    command=show_temp_frame,
    bg=manager.btn_color,
    fg=manager.fg,
)

"""



import tkinter as tk
import subprocess
import threading
import importlib
import builtins
import json
import sys
import os
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
from datetime import datetime
from tkinter import ttk



class function__:
    def __init__(self, win):
        self.VERSION = "1_4_0"
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.CONFIG_PATH = "config.json"
        self.btn_color = "#444444"
        self.layout_mode = "pack"
        self.username = "user"
        self.log_boxes = {}
        self.server = None
        self.bg = "black"
        self.fg = "white"
        self.layout_mode = "pack"
        
        self.win = win
        self.win.title("Server Manager Edit By MixPlus")
        self.win.geometry("910x490")
        self.win.minsize(910, 490)
        self.win.configure(bg=f"{self.bg}")
        self.win.protocol("WM_DELETE_WINDOW", self.on_closing_)
        
        self.CONFIG = {
                "btn_color": "#444444",
                "username": "user",
                "server_jar": "",
                "min_ram": "10",
                "max_ram": "10",
                "slots": "20",
                "bg": "black",
                "fg": "white",
                "eula": False,
                "save_log": False,
                "server": None,
            }
        
        print("ファイル生成json保存やファイルの読み込み実行を理解できていません。\nこれがすべて実装されるとサーバー用のjarファイルeulaの同意\nJDKが必須です! JDK機能を搭載するかもしれませんが\njavaサーバーのみです。 jarファイルを選択してください。\nポート開放やipなどのサポートはありません。\nEdit By MixPlus")
        
        try:
            with open(self.CONFIG_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception as e:
            self.fix_()
        self.color_ch_()
    
    def fix_(self):
        with open(self.CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(self.CONFIG, f, indent=4, ensure_ascii=False)
            return
        return
    
    def on_closing_(self):
        self.stop_server_()
        self.win.destroy()
        if self.server is not None:
            print("サーバーを停止しました。")
        else:
            print("GUIを終了しました。")
        return
    
    def start_server_(self):
        if self.server is not None:
            print("[WARN] すでにサーバーが起動しています。")
            self.add_log_("[WARN] すでにサーバーが起動しています。")
            return
        # --- config.json を読み込む ---
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        if not os.path.exists(config_path):
            print("[ERROR] config.json が見つかりません。")
            self.add_log_("[ERROR] config.json が見つかりません。")
            return
        
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        jar_path = config.get("server_jar", "")
        min_ram = config.get("min_ram", "1G") or "1G"
        max_ram = config.get("max_ram", "2G") or "2G"
        if not jar_path or not os.path.exists(jar_path):
            print("[ERROR] サーバーjarファイルが見つかりません。")
            self.add_log_("[ERROR] サーバーjarファイルが見つかりません。", "red")
            self.add_log_("[ERROR] サーバーjarファイルが見つかりません。", "red", "help")
            return
        
        print(f"[INFO] サーバーを起動します: {jar_path}")
        print(f"[INFO] RAM設定: min={min_ram}, max={max_ram}")
        self.add_log_(f"[INFO] サーバーを起動します: {jar_path}", "blue")
        self.add_log_(f"[INFO] サーバーを起動します: {jar_path}", "blue", "help")
        self.add_log_(f"[INFO] RAM設定: min={min_ram}, max={max_ram}", "blue")
        self.add_log_(f"[INFO] RAM設定: min={min_ram}, max={max_ram}", "blue", "help")
        
        # --- サーバー起動 ---
        self.server = subprocess.Popen(
            ["java", f"-Xmx{max_ram}G", f"-Xms{min_ram}G", "-jar", jar_path, "nogui"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1
        )
        
        threading.Thread(target=self.read_output_, daemon=True).start()
    
    def stop_server_(self):
        if self.server is None:
            self.add_log_("[WARN] サーバーは起動していません。", "yellow")
            self.add_log_("[WARN] サーバーは起動していません。", "yellow", tab="help")
            return
        try:
            self.send_command_("/stop")
            self.add_log_("[INFO] サーバーを停止中...", "red")
            self.add_log_("[INFO] サーバーを停止中...", "red", "help")
            self.win.after(10000, self.server.terminate)  # OK
            self.add_log_("[INFO] サーバーを停止しました。", "yellow")
            self.add_log_("[INFO] サーバーを停止しました。", "yellow", "help")
        except Exception as e:
            self.add_log_(f"[ERROR] サーバー停止に失敗: {e}")
        finally:
            self.server = None
    
    def send_command_(self, cmd: str):
        if cmd.startswith("/"):
            if self.server and self.server.stdin:
                self.server.stdin.write(cmd + "\n")
                self.server.stdin.flush()
                print(f"[cmd] {cmd}")
            else:
                print("[WARN] サーバーが起動していません。")
                self.add_log_("[WARN] サーバーは起動していません。", "yellow", tab="help")
                self.add_log_("[WARN] サーバーは起動していません。", "yellow", tab="main")
    
    def read_output_(self):
        box = self.log_boxes.get("main")  # mainタブのログボックスを使う
        if not box:
            return
        
        box.tag_config("error", foreground="red")
        box.tag_config("info", foreground="cyan")
        
        for line in iter(self.server.stdout.readline, ''):
            line = line.strip()
            box.config(state="normal")
            
            if "ERROR" in line or "Exception" in line:
                self.add_log_(f"{line}\n", "red", "help")
                box.insert("end", line + "\n", "error")
            elif "INFO" in line or "[INFO]" in line:
                self.add_log_(f"{line}\n", "white", "help")
                box.insert("end", line + "\n", "info")
            else:
                self.add_log_(f"{line}\n", "blue", "help")
                box.insert("end", line + "\n")
            
            if self.save_state.get():
                today = datetime.now().strftime("%Y-%m-%d")
                path = f"Manager_log/{today}.txt"
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "a", encoding="utf-8") as f:
                    f.write(f"{line}\n")
            box.see("end")
            box.config(state="disabled")
    
    def color_ch_(self):
        if os.path.exists(self.CONFIG_PATH):
            with open(self.CONFIG_PATH, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        else:
            self.config = {}
        
        # グローバル変数に反映
        self.username = self.config.get("username", "Unknown")
        self.bg = self.config.get("bg", "black") or "black"
        self.fg = self.config.get("fg", "white") or "white"
        self.btn_color = self.config.get("btn_color", "#444444") or "#444444"
    
    def gui_(self):
        self.frame_main, self.box_main, self.log_box = self.main_tab_(win)
        self.show_frame(self.frame_main)
        self.frame_credits = self.credits_tab_(win)
        self.frame_mods = self.mods_tab_(win)
        self.frame_plugins = self.plugins_tab_(win)
        self.frame_setting = self.setting_tab_(win)
        self.frame_help = self.help_tab_(win)
        self.frame_Extensions = self.Extensions_tab_(win)
        
        #main tab
        self.btn_(win, "Main", command=lambda: self.show_frame(self.frame_main), bg=self.btn_color, fg=self.fg, layout_mode="place", x=0, y=0, width=100, height=20, relief="flat")
        
        #credits
        self.btn_(win, "Credits", command=lambda: self.show_frame(self.frame_credits), bg=self.btn_color, fg=self.fg, layout_mode="place", x=101, y=0, width=100, height=20, relief="flat")
        
        #Mods
        self.btn_(win, "Mods", command=lambda: self.show_frame(self.frame_mods), bg=self.btn_color, fg=self.fg, layout_mode="place", x=202, y=0, width=100, height=20, relief="flat")
        
        #plugins
        self.btn_(win, "Plugins", command=lambda: self.show_frame(self.frame_plugins), bg=self.btn_color, fg=self.fg, layout_mode="place", x=303, y=0, width=100, height=20, relief="flat")
        
        #Settings
        self.btn_(win, "Setting", command=lambda: self.show_frame(self.frame_setting), bg=self.btn_color, fg=self.fg, layout_mode="place", x=404, y=0, width=100, height=20 ,relief="flat")
        
        #help
        self.btn_(win,"Help", command=lambda: self.show_frame(self.frame_help), bg=self.btn_color, fg=self.fg, layout_mode="place", x=505, y=0, width=100, height=20, relief="flat")
        
        #Extensions
        self.btn_(self.frame_setting, "拡張機能", command=lambda: self.show_frame(self.frame_Extensions), bg=self.btn_color, fg=self.fg, font=("arial", 10), layout_mode="place", x=700, y=118, width=80, height=25)
        #button
        self.btn_(self.frame_setting, "GUI再起動", command=self.app_, bg=self.btn_color, fg="red", font=("arial", 10), layout_mode="place", x=758, y=410, width=150, height=25)
        self.btn_(self.frame_setting, "コンフィグリセット", command=self.config_reset_, bg=self.btn_color, fg="red", layout_mode="place", x=758, y=440, width=150, height=25)
        self.btn_(self.frame_main, "サーバー起動", command=self.start_server_, bg=self.btn_color, fg=self.fg, relief="flat", layout_mode="place", x=0, y=2, width=100, height=20)
        self.btn_(self.frame_main, "サーバー停止", command=self.stop_server_, bg=self.btn_color, fg=self.fg, relief="flat", layout_mode="place", x=101, y=2, width=100, height=20)
    
    def main_tab_(self, parent):
        self.frame_(parent)
        self.label_("Main")
        self.log_box_()
        self.scrollbar_()
        self.text_box = tk.Entry(self.frame, width=90, font=("arial", 15), bg=self.btn_color, fg=self.fg)
        self.text_box.place(y=440, x=0)
        self.text_box.bind("<Return>", self.on_enter)
        self.log_boxes['main'] = self.log_box
        return self.frame, self.text_box, self.log_box
    
    def credits_tab_(self, parent):
        self.frame_(parent)
        self.scrollbar_()
        self.label_("Credits")
        
        credit = [
        "この""ツールはminecraftサーバーを管理するために作られました。",
        "Open AI chatgpt   Microsoft Copilot",
        "との会話によって設計されました。",
        "guiの設計などの情報をいただきました。",
        "このツールはまだ未完成ですが",
        "完成してもおそらくアップデートが続くでしょう。",
        "作者のほしい機能などを搭載していきます。",
        "できるだけ一つのファイルにしようと思っていますが"
        "複数のファイル版も作成する予定です。",
        "                    協力者:2                     テスター:1",
        "Open AI chatgpt   Microsoft Copilot   MixPlus",
        #"\n \n \nedit by MixPlus",
    ]
        self.label_("edit", fg="blue",  layout_mode="place", x=50, y=350)
        self.label_("by", fg="#FFAA00", layout_mode="place", x=100, y=350)
        self.label_("MixPlus", fg="#00FF00", x=140, y=350)
        for i, line in enumerate(credit):
            
            self.label_(line, bg=self.bg, fg=self.fg, layout_mode="place", x=30, y=30 + i * 25)
        return self.frame
    
    def mods_tab_(self, parent):
        self.frame_(parent)
        self.label_("Mods List")
        self.scrollbar_
        self.listbox_()
        mods_path = os.path.join(self.current_dir, "mods")
        if os.path.exists(mods_path):
            for item in os.listdir(mods_path):
                self.listbox.insert(tk.END, item)
        else:
            self.listbox.insert(tk.END, "modsフォルダが見つかりませんでした")
        return self.frame
    
    def Extensions_tab_(self, parent):
        self.frame_(parent)
        self.label_("Extensions List")
        self.scrollbar_
        self.listbox_()
        Extensions_path = os.path.join(self.current_dir, "Extensions")
        if os.path.exists(Extensions_path):
            for item in os.listdir(Extensions_path):
                self.listbox.insert(tk.END, item)
        else:
            self.listbox.insert(tk.END, "pluginsフォルダが見つかりませんでした")
        self.btn_(self.frame, "←戻る", command=lambda: self.show_frame(self.frame_setting), bg=self.btn_color, fg=self.fg, layout_mode="place", x=825, y=0, width=80, height=25)
        return self.frame
    
    def plugins_tab_(self, parent):
        self.frame_(parent)
        self.label_("Plugin List")
        self.scrollbar_
        self.listbox_()
        plugins_path = os.path.join(self.current_dir, "plugins")
        if os.path.exists(plugins_path):
            for item in os.listdir(plugins_path):
                self.listbox.insert(tk.END, item)
        else:
            self.listbox.insert(tk.END, "pluginsフォルダが見つかりませんでした")
        return self.frame
    
    def setting_tab_(self, parent):
        self.frame_(parent)
        self.label_("設定")
        
        try:
            with open(self.CONFIG_PATH, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        except Exception:
            self.config = {}
        if not self.config.get("eula", False):
            answer = messagebox.askyesno("Minecraft EULA", "Minecraft EULA (https://aka.ms/MinecraftEULA) に同意しますか？")
        
        self.config["eula"] = True
        with open(self.CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
        
        self.config = self.load_config_()
        self.entries = {}
        
        self.label_("サーバーJARファイル:", layout_mode="place", x=50, y=60)
        self.jar_entry = tk.Entry(self.frame, bg=self.btn_color, fg=self.fg, font=("arial", 12), width=40)
        self.jar_entry.insert(0, self.config.get("server_jar", ""))
        self.jar_entry.place(x=250, y=60)
        self.entries["server_jar"] = self.jar_entry
        self.save_state = tk.BooleanVar(value=self.config.get("save_log", False))
        self.label_("ログの自動保存", layout_mode="place", x=50, y=380)
        self.save_log = tk.Button(self.frame, text="OFF", bg=self.bg, fg=self.fg, font=("arial", 12), command=self.save_toggle_, width=8)
        self.save_log.place(x=250, y=380)
        
        self.btn_(self.frame, "参照", command=self.select_jar_, bg=self.btn_color, fg=self.fg, layout_mode="place", x=700, y=58, width=80, height=25)
        settings = [
        ("最低RAM", "min_ram", 100),
        ("最大RAM", "max_ram", 140),
        ("スロット数", "slots", 180),
        ("ユーザーネーム", "username", 220),
        ("背景色", "bg", 260),
        ("文字色", "fg", 300),
        ("ボタンの色", "btn_color", 340),
        
        ]
        
        for text, key, y in settings:
            tk.Label(self.frame, text=text, bg=self.bg, fg=self.fg, font=("arial", 12)).place(x=50, y=y)
            entry = tk.Entry(self.frame, bg=self.btn_color, fg=self.fg, font=("arial", 12), width=40)
            entry.insert(0, self.config.get(key, ""))
            entry.place(x=250, y=y)
            self.entries[key] = entry
        self.auto_sync_()
        return self.frame
    
    def help_tab_(self, parent):
        self.frame_(parent)
        self.label_("Help")
        self.log_box_(x=0, y=30, width=900, height=438)
        self.scrollbar_()
        self.log_boxes['help'] = self.log_box
        self.help_log_("help")
        return self.frame
    
    def help_log_(self, tab):
        self.add_log_("　　　　　　　　　　　　　　　　　　　　使い方", "#33FF00", tab=tab)
        self.add_log_("1,　　起動できたらSettingタブに移動して　好きに設定しよう!\n　　　サーバーJARファイルや最低最大RAM量を設定してね!", tab=tab)
        self.add_log_("　　　注意だけど不正な値は入力しないようにね! [RAM設定でinfiniteなど]", "red", tab=tab)
        self.add_log_("　　　このソフト用のニックネームも決められるよ\n　　　背景色　文字色　ボタンの色を変更できるよ\n　　　変更後は再起動ボタンを押してね\n", tab=tab)
        self.add_log_("2,　　Mainタブに戻ってサーバー起動ボタンを押してね\n　　　サーバーのファイルはこの.pyまたはexeがある場所に作られるよ", tab=tab)
        self.add_log_("　　　サーバーはバックグラウンドで起動するよ\n　　　サーバーログも出てくるからね\n　　　テキストボックスでコマンドを送信するとサーバーにも反映されるよ", tab=tab)
        self.add_log_("　　　/stopをテキストボックスで入力して送信してね\n", "yellow", tab=tab)
        self.add_log_("　　　　　　　　　　　　　　　　　　　　タブの説明", "blue", tab=tab)
        self.add_log_("1, 　　Mainタブ\n　　　Mainタブではサーバーの起動強制停止　サーバーにコマンド送信　ログの確認\n　　　が利用できます\n", tab=tab)
        self.add_log_("2, 　　Creditはcreditがあります\n", tab=tab)
        self.add_log_("3, 　　MODsタブはmodリスト\n", "", tab=tab)
        self.add_log_("3, 　　Pluginタブはプラグインリスト\n", "", tab=tab)
        
        self.add_log_("----------------------------------------------------------------------ログ------------------------------------------------------------------------", "yellow", tab="help")
        
        return
    
    def load_Extensions(self, window):
        if self.config.get("server", False):
            self.add_log_("\n以前サーバーが起動したまま。停止した可能性があります\n", "red")
        
        extensions_folder = 'Extensions'  # 拡張機能が格納されているフォルダ
        os.makedirs(os.path.dirname("Extensions/temp.py"), exist_ok=True)
        
        if not os.path.exists(extensions_folder):
            print(f"{extensions_folder} フォルダが存在しません")
            return
        
        loaded_extensions = set()  # 重複ロード防止
        
        # インスタンスを builtins にセット
        builtins.FUNC_INSTANCE = self

        for filename in os.listdir(extensions_folder):
            if filename.endswith('.py') and filename != "__init__.py":
                extension_name = filename[:-3]
                
                if extension_name in loaded_extensions:  # すでにロード済みならスキップ
                    continue
                loaded_extensions.add(extension_name)
                
                try:
                    self.add_log_(f"Loaded extension: {extension_name}", "green", "help")
                    self.add_log_(f"Loaded extension: {extension_name}", "green")
                    print(f"Loaded extension: {extension_name}")
                    
                    extension_module = importlib.import_module(f"Extensions.{extension_name}")
                    
                    # 拡張機能側に init_extension 関数があれば呼ぶ
                    if hasattr(extension_module, "init_extension"):
                        extension_module.init_extension()
                    
                except Exception as e:
                    print(f"Error loading extension {extension_name}: {e}")
                    self.add_log_(f"Error loading extension {extension_name}: {e}", "red", "help")
                    self.add_log_(f"Error loading extension {extension_name}: {e}", "red", "main")
    
    def auto_sync_(self):
        current = {}
        # セーブ
        try:
            current = {k: e.get() for k, e in self.entries.items()}
            #config save用
            current["save_log"] = self.save_state.get()
            current["server"] = self.server is not None
            
            latest_config = self.load_config_()
            if "eula" in latest_config:
                current["eula"] = latest_config["eula"]
            self.save_config_(current)
            
        except Exception as e:
            print("自動保存エラー:", e)
            self.add_log_(f"自動保存エラー:{e}")
        
        # リロード
        try:
            latest = self.load_config_()
            for k, e in self.entries.items():
                latest_val = latest.get(k, "")
                if e.get() != latest_val:
                    e.delete(0, tk.END)
                    e.insert(0, latest_val)
            latest_save = latest.get("save_log", self.save_state.get())
            if latest_save != self.save_state.get():
                self.save_state.set(latest.get("save_log", False))
                self.save_log.config(text="ON" if self.save_state.get() else "OFF")
        except Exception as e:
            print("自動リロードエラー:", e)
            self.add_log_(f"自動リロードエラー:{e}")
        
        
        #username = latest.get("username", "Unknown")  # ← グローバル変数として作る
        
        
        # 5秒ごとに繰り返す
        self.frame.after(500, self.auto_sync_)
    
    def select_jar_(self):
        path = filedialog.askopenfilename(title="サーバーの .jar ファイルを選んでね", filetypes=[("Java Archive", "*.jar"), ("すべてのファイル", "*.*")])
        if path:
            self.jar_entry.delete(0, tk.END)
            self.jar_entry.insert(0, path)
            print("選ばれたファイル:", path)
    
    def save_toggle_(self):
        self.save_state.set(not self.save_state.get())
        self.save_log.config(text="ON" if self.save_state.get() else "OFF")
        self.config["save_log"] = self.save_state.get()
        self.save_config_(self.config)
    
    def agree_(self):
        try:
            with open("eula.txt", "w", encoding="utf-8") as file:
                file.write("#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://aka.ms/MinecraftEULA).\n")
                file.write("eula=true\n")
        
        except Exception as e:
            print("eula.txt 書き込みエラー:", e)
            self.add_log_(f"eula.txt 書き込みエラー:{e}")
    
    def load_config_(self):
        if not os.path.exists(self.CONFIG_PATH):
            with open(self.CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(self.DEFAULT, f, indent=4, ensure_ascii=False)
            return self.DEFAULT
        try:
            with open(self.CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            self.add_log_(f"設定ファイル読み込みエラー:{e}")
            print("設定ファイル読み込みエラー:", e)
            return self.DEFAULT
    
    def save_config_(self, data):
        try:
            with open(self.CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print("設定保存エラー:", e)
            self.add_log_(f"設定保存エラー:{e}")
    
    def frame_(self, parent):
        self.frame = tk.Frame(parent, bg=self.bg)
        self.frame.place(x=0, y=20, width=910, height=490)
    
    def label_(self, text, bg=None, fg=None, layout_mode=None, x=None, y=None):
        lbl = tk.Label(self.frame, text=text, bg=bg, fg=fg, font=("arial", 12))
        
        # place
        if layout_mode == "place":
            lbl.place(x=x if x is not None else 0, y=y if y is not None else 0)
            
        # grid
        elif layout_mode == "grid":
            row = y if y is not None else 0
            col = x if x is not None else 0
            lbl.grid(row=row, column=col, padx=5, pady=5)
            
        # pack（デフォルト）
        else:
            lbl.pack(pady=0)
            
        return lbl
    
    def scrollbar_(self):
        # Scrollbar作成
        self.scrollbar_widget = tk.Scrollbar(self.frame, command=self.log_box.yview)
        self.scrollbar_widget.place(x=890, y=30, height=400)
        
        # log_box に scrollbar を紐付け
        self.log_box.configure(yscrollcommand=self.scrollbar_widget.set)
    
    def log_box_(self, x=0, y=30, width=900, height=400):
        self.log_box = tk.Text(self.frame, bg=self.bg, fg=self.fg, font=("arial", 12), state="disabled")
        self.log_box.place(x=x, y=y, width=width, height=height)
        if hasattr(self, "scrollbar_widget"):
            self.log_box.configure(yscrollcommand=self.scrollbar_widget.set)
    
    def listbox_(self, bg=None, fg=None, relief=None):
        self.listbox = tk.Listbox(self.frame, font=("arial", 12), bg=bg, fg=fg)
        self.listbox.config(yscrollcommand=self.scrollbar_widget.set)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def btn_(self, iframe, text, command=None, bg=None, fg=None, layout_mode=None, x=None, y=None, width=100, height=20, font=("arial", 12), relief=None ):
        butt = tk.Button(iframe, text=text, command=command, bg=bg, fg=fg, font=font, relief=relief)
        
        
        # place
        if layout_mode == "place":
            butt.place(x=x if x is not None else 0, y=y if y is not None else 0, width=width if width is not None else 0, height=height if height is not None else 0)
            
        # grid
        elif layout_mode == "grid":
            row = y if y is not None else 0
            col = x if x is not None else 0
            butt.grid(row=row, column=col, padx=5, pady=5)
            
        # pack（デフォルト）
        else:
            butt.pack(pady=0)
            
        return butt
    
    def add_log_(self, text, color=None, tab="main"):
        box = self.log_boxes.get(tab)
        if box is None:
            print(text)
            return
        
        box.config(state="normal")
        
        if color:
            # タグがなければ作る
            if color not in box.tag_names():
                box.tag_config(color, foreground=color)
            box.insert("end", text + "\n", color)
        else:
            box.insert("end", text + "\n")
            
        box.see("end")
        box.config(state="disabled")
    
    def show_frame(self, frame):
        frame.tkraise()
    
    def on_enter(self, event=None):
        cmd = self.text_box.get().strip()
        if not cmd:
            return
        
        # log_boxにコマンドを色付きで表示
        self.add_log_(f"<{self.username}> {cmd}", "#00FF1f")
        #custom command
        self.send_command_(cmd)
        if "server" in cmd:
            print(f"Server: {self.server}")
            self.add_log_(f"Server: {self.server}", "#FF00C8")
        elif "help" in cmd:
            self.help_log_("main")
        elif cmd.startswith("."):
            tell_cmd = f"/say @a [Server] {cmd[1:]}"
            if self.server and self.server.stdin:
                self.server.stdin.write(tell_cmd + "\n")
                self.server.stdin.flush()
            self.add_log_(f"<{self.username}> {tell_cmd}", "#00FF1f")
        elif "command" in cmd:
            print(f"server: サーバーの状態\nhelp: このプロジェクトのhelp\n.: .好きなメッセージ　これでサーバーに送信される")
            self.add_log_(f"server: サーバーの状態\nhelp: このプロジェクトのhelp\n.: .好きなメッセージ　これでサーバーに送信される")
            self.add_log_(f"server: サーバーの状態\nhelp: このプロジェクトのhelp\n.: .好きなメッセージ　これでサーバーに送信される", None, "help")
        # 入力欄クリア
        self.text_box.delete(0, tk.END)
    
    def app_(self):
        print("再起動します。")
        exe = sys.executable
        script = os.path.abspath(sys.argv[0])
        subprocess.Popen([exe, script])  # 新しいプロセスを起動 停止
        self.win.destroy()
        return
    
    def config_reset_(self):
        self.fix_()
        self.app_()
        return self.fix_, self.app_
    
    def none_(self):
        pass

if __name__ == "__main__":
    win = tk.Tk()
    function = function__(win) 
    function.gui_()
    
    
    function.frame_main.lift()
    function.load_Extensions(win)
    function.win.mainloop()
