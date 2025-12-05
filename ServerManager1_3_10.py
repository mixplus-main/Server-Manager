import tkinter as tk
import subprocess
import threading
import importlib
import json
import sys
import os
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
from datetime import datetime
from tkinter import ttk

class function__:
    def __init__(self, parent):
        self.CONFIG_PATH = "config.json"
        self.btn_color = "#444444"
        self.username = "user"
        self.parent = parent
        self.log_boxes = {}
        self.server = None
        self.bg = "black"
        self.fg = "white"
        self.json = json
        
        self.DEFAULT = {
            "btn_color": "#444444",
            "username": "user",
            "server_jar": "",
            "min_ram": "10",
            "max_ram": "10",
            "save_log": False,
            "slots": "20",
            "bg": "black",
            "fg": "white",
            "eula": False,
            }
            
        try:
            with open(self.CONFIG_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception as e:
            print(f"修正中\nerror:{e}")
            # 壊れてる or 読めない → デフォルトで上書き
            with open(self.CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(self.DEFAULT, f, indent=4, ensure_ascii=False)
            config = self.DEFAULT
        
        
        print("未実装: help\nこれはサーバーの管理目的です。\nファイル生成json保存やファイルの読み込み実行を理解できていません。\nこれがすべて実装されるとサーバー用のjarファイルeulaの同意\nJDKが必須です! JDK機能を搭載するかもしれませんが\njavaサーバーのみです。 jarファイルを選択してください。\nポート開放やipなどのサポートはありません。\nedit by MixPlus")
    
    def fix(self):
        try:
            with open(function.CONFIG_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception as e:
            try:
                print(f"修正中\nerror:{e}")
                if os.path.exists("fix1_3_10.py"):
                    subprocess.run(["python", "fix1_3_10.py"])
                else:
                    print("⚠️ fix1_3_10.py が見つかりません")
                messagebox.showwarning("警告", "コンフィグファイルが破損していたのでリセットされました\n再度設定しなおしてください")
            except Exception:
                pass
        else:
            pass


    def color_ch(self):
        global username, fg, bg, btn_color
            
        if os.path.exists(self.CONFIG_PATH):
            with open(self.CONFIG_PATH, "r", encoding="utf-8") as self.f:
                self.config = json.load(self.f)
        else:
            self.config = {}
            
            # グローバル変数に反映
            self.username = self.config.get("username", "Unknown")
            self.bg = self.config.get("bg", "black") or "black"
            self.fg = self.config.get("fg", "white") or "white"
            self.btn_color = self.config.get("btn_color", "#444444") or "#444444"
    
    def add_log(self, text, color=None, tab="main"):
        self.box = self.log_boxes.get(tab)
        if self.box is None:
            print(text)
            return
        self.box.config(state="normal")
        if color:
            self.box.insert("end", text + "\n", color)
        else:
            self.box.insert("end", text + "\n")
        self.box.see("end")
        self.box.config(state="disabled")
    
    def help_tab(self, parent):
        global add_log
        self.frame = tk.Frame(parent, bg=self.bg)
        self.frame.place(x=0, y=20, width=910, height=490)
        self.label = tk.Label(self.frame, text="Help", bg=self.btn_color, fg=self.fg, font=("arial", 12))
        self.label.pack()
        
        #ここに新しくlog_box
        
        # ログ表示用ボックス
        self.log_box = tk.Text(self.frame, bg=self.bg, fg=self.fg, font=("arial", 14), state="disabled")
        self.log_box.place(x=0, y=30, width=900, height=438)
        
        # スクロールバー
        self.scrollbar = tk.Scrollbar(self.frame, command=self.log_box.yview)
        self.scrollbar.place(x=890, y=30, height=440)
        self.log_box.configure(yscrollcommand=self.scrollbar.set)
        self.log_box.tag_config("red", foreground="red")
        self.log_box.tag_config("green", foreground="green")
        self.log_box.tag_config("blue", foreground="blue")
        self.log_box.tag_config("light_green", foreground="#00FF15")
        self.log_box.tag_config("yellow", foreground="#FFFB01")
        self.log_box.tag_config("light_blue", foreground="#04FFFB")
        
        self.log_boxes['help'] = self.log_box
        
        
        
        self.add_log("　　　　　　　　　　　　　　　　　　　　使い方", "light_green", tab="help")
        self.add_log("1,　　起動できたらSettingタブに移動して　好きに設定しよう!", tab="help")
        self.add_log("　　　サーバーJARファイルや最低最大RAM量を設定してね!", tab="help")
        self.add_log("　　　注意だけど不正な値は入力しないようにね! [RAM設定でinfiniteなど]", tab="help")
        self.add_log("　　　このソフト用のニックネームも決められるよ", tab="help")
        self.add_log("　　　背景色　文字色　ボタンの色を変更できるよ", tab="help")
        self.add_log("　　　変更後は再起動ボタンを押してね\n", tab="help")
        self.add_log("2,　　Mainタブに戻ってサーバー起動ボタンを押してね", tab="help")
        self.add_log("　　　サーバーのファイルはこの.pyまたはexeがある場所に作られるよ", tab="help")
        self.add_log("　　　サーバーはバックグラウンドで起動するよ", tab="help")
        self.add_log("　　　サーバーログも出てくるからね", tab="help")
        self.add_log("　　　テキストボックスでコマンドを送信するとサーバーにも反映されるよ", tab="help")
        self.add_log("　　　サーバーを停止するときは極力サーバーを停止を押さないこと", "red", tab="help")
        self.add_log("　　　/stopをテキストボックスで入力して送信してね\n", "yellow", tab="help")
        self.add_log("　　　　　　　　　　　　　　　　　　　　タブの説明", "light_blue", tab="help")
        self.add_log("1, 　　Mainタブ\n　　　Mainタブではサーバーの起動強制停止　サーバーにコマンド送信　ログの確認\n　　　が利用できます\n", tab="help")
        self.add_log("2, 　　Creditはcreditがあります\n", tab="help")
        self.add_log("3, 　　MODsタブはmodリスト\n", "", tab="help")
        self.add_log("3, 　　Pluginタブはプラグインリスト\n", "", tab="help")
        
        self.add_log("----------------------------------------------------------------------ログ------------------------------------------------------------------------", "yellow", tab="help")
        
        return self.frame
    
    
    def agree(self):
        try:
            with open("eula.txt", "w", encoding="utf-8") as self.file:
                self.file.write("#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://aka.ms/MinecraftEULA).\n")
                self.file.write("eula=true\n")
        
        except Exception as e:
            print("eula.txt 書き込みエラー:", e)
            self.add_log(f"eula.txt 書き込みエラー:{e}")
    
    
    def load_config(self):
            
            if not os.path.exists(self.CONFIG_PATH):
                with open(self.CONFIG_PATH, "w", encoding="utf-8") as f:
                    json.dump(self.default, f, indent=4, ensure_ascii=False)
                return self.default
            try:
                with open(self.CONFIG_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                self.add_log(f"設定ファイル読み込みエラー:{e}")
                print("設定ファイル読み込みエラー:", e)
                return self.default
    
    def save_toggle(self):
        self.save_state.set(not self.save_state.get())
        self.save_log.config(text="ON" if self.save_state.get() else "OFF")
        self.config = self.load_config()
        self.config["save_log"] = self.save_state.get()
        self.save_config(self.config)
    
    def select_jar(self):
        self.path = filedialog.askopenfilename(
            title="サーバーの .jar ファイルを選んでね",
            filetypes=[("Java Archive", "*.jar"), ("すべてのファイル", "*.*")]
        )
        if self.path:
            self.jar_entry.delete(0, tk.END)
            self.jar_entry.insert(0, self.path)
            print("選ばれたファイル:", self.path)
    
    def auto_sync(self):
        global username, fg, bg, btn_color
        self.current = {}
        # セーブ
        try:
            self.current = {k: e.get() for k, e in self.entries.items()}
            #config save用
            self.current["save_log"] = self.save_state.get()
            
            
            self.latest_config = self.load_config()
            if "eula" in self.latest_config:
                self.current["eula"] = self.latest_config["eula"]
            self.save_config(self.current)
            
        except Exception as e:
            print("自動保存エラー:", e)
            self.add_log(f"自動保存エラー:{e}")
        
        # リロード
        try:
            self.latest = self.load_config()
            for k, e in self.entries.items():
                self.latest_val = self.latest.get(k, "")
                if e.get() != self.latest_val:
                    e.delete(0, tk.END)
                    e.insert(0, self.latest_val)
            self.latest_save = self.latest.get("save_log", self.save_state.get())
            if self.latest_save != self.save_state.get():
                self.save_state.set(self.latest.get("save_log", False))
                self.save_log.config(text="ON" if self.save_state.get() else "OFF")
        except Exception as e:
            print("自動リロードエラー:", e)
            self.add_log(f"自動リロードエラー:{e}")
        
        self.frame.after(500, self.auto_sync)
    
    def save_config(self, data):
        try:
            with open(self.CONFIG_PATH, "w", encoding="utf-8") as f:
                self.json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print("設定保存エラー:", e)
            self.add_log(f"設定保存エラー:{e}")
    
    def setting_tab(self, parent):
        global username, fg, bg, btn_color
        self.frame = tk.Frame(parent, bg=f"{self.bg}")
        self.frame.config(bg=self.bg)
        self.frame.place(x=0, y=20, width=910, height=490)
        
        tk.Label(self.frame, text="設定", bg=self.btn_color, fg=self.fg, font=("arial", 14)).pack(pady=10)
        
        try:
            with open(self.CONFIG_PATH, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        except Exception:
            self.config = {}
        
        if not self.config.get("eula", False):
            
            self.answer = messagebox.askyesno(
            "Minecraft EULA",
            "Minecraft EULA (https://aka.ms/MinecraftEULA) に同意しますか？")
            while not self.answer:
                self.answer = messagebox.askyesno(
                    "EULA 未同意",
                    "同意しない場合、再度確認します。\n同意しますか？"
                )
        
        self.config["eula"] = True
        with open(self.CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
        
        self.agree()
        
        # --- 設定ファイルの読み書き ---
        
        
        
        self.config = self.load_config()
        self.entries = {}
        
        # --- サーバーJAR ---
        tk.Label(self.frame, text="サーバーJARファイル:", bg=self.bg, fg=self.fg, font=("arial", 12)).place(x=50, y=60)
        jar_entry = tk.Entry(self.frame, bg=self.btn_color, fg=self.fg, font=("arial", 12), width=40)
        jar_entry.insert(0, self.config.get("server_jar", ""))
        jar_entry.place(x=250, y=60)
        self.entries["server_jar"] = jar_entry
        global save_log, save_state
        self.save_state = tk.BooleanVar(value=self.config.get("save_log", False))
        
        tk.Label(self.frame, text="ログの自動保存", bg=self.bg, fg=self.fg, font=("arial", 12)).place(x=50, y=380)
        self.save_log = tk.Button(self.frame, text="OFF", bg=self.bg, fg=self.fg, font=("arial", 12), command=self.save_toggle, width=8)
        self.save_log.place(x=250, y=380)
        
        
        tk.Button(self.frame, text="参照", command=self.select_jar,
                bg=self.btn_color, fg=self.fg, font=("arial", 10)).place(x=700, y=58, width=80, height=25)
        # --- RAM・スロット数 ---
        self.settings = [
            ("最低RAM", "min_ram", 100),
            ("最大RAM", "max_ram", 140),
            ("スロット数", "slots", 180),
            ("ユーザーネーム", "username", 220),
            ("背景色", "bg", 260),
            ("文字色", "fg", 300),
            ("ボタンの色", "btn_color", 340)
            ]
            
        for text, key, y in self.settings:
            tk.Label(self.frame, text=text, bg=self.bg, fg=self.fg, font=("arial", 12)).place(x=50, y=y)
            self.entry = tk.Entry(self.frame, bg=self.btn_color, fg=self.fg, font=("arial", 12), width=40)
            self.entry.insert(0, self.config.get(key, ""))
            self.entry.place(x=250, y=y)
            self.entries[key] = self.entry
        
        
        
        self.auto_sync()
        return self.frame
    
    def on_enter(self, event=None):
            self.cmd = self.box.get().strip()
            if not self.cmd:
                return
            
            # log_boxにコマンドを色付きで表示
            self.main_log_box.config(state="normal")
            self.main_log_box.tag_config("command", foreground="#15FF00", font=("arial", 12), background=self.bg)  # コマンドの色を黄色に
            self.main_log_box.insert("end", f"<{self.username}> {self.cmd}\n", "command")
            self.main_log_box.see("end")
            self.main_log_box.config(state="disabled")
            if self.server and self.server.stdin:
                self.server.stdin.write(self.cmd + "\n")
                self.server.stdin.flush()
            else:
                self.main_log_box.insert("end", f"[WARN] サーバーが起動していません。\n", "command")
                self.main_log_box.see("end")
                self.main_log_box.config(state="disabled")
            
            self.send_command(self.cmd)  # サーバーに送信
            self.box.delete(0, tk.END)  # 入力欄クリア
        
    def main_tab(self, parent):
        self.frame = tk.Frame(self.parent, bg=self.bg)
        self.frame.config(bg=self.bg)
        self.frame.place(x=0, y=20, width=910, height=490)
        
        # タブ名
        self.label = tk.Label(self.frame, text="Main", bg=self.btn_color, fg=self.fg, font=("arial", 12))
        self.label.pack()
        
        # ログ表示用ボックス
        self.main_log_box = tk.Text(self.frame, bg=self.bg, fg=self.fg, font=("Consolas", 10), state="disabled")
        self.main_log_box.place(x=0, y=30, width=900, height=400)
        self.log_boxes['main'] = self.main_log_box
        # スクロールバー
        self.scrollbar = tk.Scrollbar(self.frame, command=self.main_log_box.yview)
        self.scrollbar.place(x=890, y=30, height=400)
        self.main_log_box.configure(yscrollcommand=self.scrollbar.set)
        
        # --- コマンド送信用エントリ ---
        
        
        self.box = tk.Entry(self.frame, width=90, font=("arial", 15), bg=self.btn_color, fg=self.fg)
        self.box.place(y=440, x=0)
        self.box.bind("<Return>", self.on_enter)  # Enterキーで送信
        
        return self.frame, self.box, self.main_log_box
    
    def credits_tab(self, parent):
        self.frame = tk.Frame(self.parent, bg=self.bg)
        self.frame.place(x=0, y=20, width=910, height=490)
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.label = tk.Label(self.frame, text="Credits", bg=self.btn_color, fg=self.fg, font=("arial", 12))
        self.label.pack()
        
        #縁取り作ってみたこれよりいいの絶対あるけど
        self.listbox = tk.Listbox(self.frame, font=("arial", 12), bg=self.bg, fg=self.fg)
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.mods_path = os.path.join(self.current_dir, "")
        
        
        self.credit = [
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
        self.label = tk.Label(self.frame, text="edit", bg=self.bg, fg="blue", font=("arial", 20))
        self.label.place(x=50, y=350)
        
        self.label = tk.Label(self.frame, text="by", bg=self.bg, fg="#FFAA00", font=("arial", 20))
        self.label.place(x=100, y=350)
        
        self.label = tk.Label(self.frame, text="MixPlus", bg=self.bg, fg="#00FF00", font=("arial", 20))
        self.label.place(x=140, y=350)
        
        self.label.lift()
        
        for i, self.line in enumerate(self.credit):
            self.label = tk.Label(self.frame, text=self.line, font=("Arial", 10), fg=self.fg, bg=self.bg)
            self.label.place(x=30, y=30 + i * 25)
        
        return self.frame
    
    def mods_tab(self, parent):
        self.frame = tk.Frame(parent, bg=self.bg)
        self.frame.place(x=0, y=20, width=910, height=490)
        
        self.label = tk.Label(self.frame, text="Mods List", bg=self.btn_color, fg=self.fg, font=("arial", 12))
        self.label.pack()
        
        
        self.listbox = tk.Listbox(self.frame, font=("arial", 12), bg=self.bg, fg=self.fg)
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.mods_path = os.path.join(self.current_dir, "mods")
        
        if os.path.exists(self.mods_path):
            for item in os.listdir(self.mods_path):
                self.listbox.insert(tk.END, item)
        else:self.listbox.insert(tk.END, "modsフォルダが見つかりませんでした")
        return self.frame
    
    def plugins_tab(self, parent):
        self.frame = tk.Frame(parent, bg=self.bg)
        self.frame.place(x=0, y=20, width=910, height=490)
        self.label = tk.Label(self.frame, text="Plugin List", bg=self.btn_color, fg=self.fg, font=("arial", 12))
        self.label.pack()
        
        self.listbox = tk.Listbox(self.frame, font=("arial", 12), bg=self.bg, fg=self.fg)
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.plugins_path = os.path.join(self.current_dir, "plugins")
        
        if os.path.exists(self.plugins_path):
            for item in os.listdir(self.plugins_path):
                self.listbox.insert(tk.END, item)
        else:self.listbox.insert(tk.END, "pluginsフォルダが見つかりませんでした")
        
        return self.frame
    
    def show_frame(self, frame):
        frame.tkraise()
    
    def append_log(self, text, tab="main"):
        self.box = self.log_boxes.get(tab)
        if self.box is None:
            print(text)
            return
        self.box.config(state="normal")
        self.box.insert("end", text + "\n")
        self.box.see("end")
        self.box.config(state="disabled")
    
    def start_server(self):
        if self.server is not None:
            print("[WARN] すでにサーバーが起動しています。")
            self.append_log("[WARN] すでにサーバーが起動しています。")
            return
        # --- config.json を読み込む ---
        self.config_path = os.path.join(os.path.dirname(__file__), "config.json")
        if not os.path.exists(self.config_path):
            print("[ERROR] config.json が見つかりません。")
            self.add_log("[ERROR] config.json が見つかりません。")
            return
        
        with open(self.config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)
        
        self.jar_path = self.config.get("server_jar", "")
        self.min_ram = self.config.get("min_ram", "1G") or "1G"
        self.max_ram = self.config.get("max_ram", "2G") or "2G"
        if not self.jar_path or not os.path.exists(self.jar_path):
            print("[ERROR] サーバーjarファイルが見つかりません。")
            self.add_log("[ERROR] サーバーjarファイルが見つかりません。", "red")
            self.add_log("[ERROR] サーバーjarファイルが見つかりません。", "red", "help")
            return
        
        print(f"[INFO] サーバーを起動します: {self.jar_path}")
        print(f"[INFO] RAM設定: min={self.min_ram}, max={self.max_ram}")
        self.add_log(f"[INFO] サーバーを起動します: {self.jar_path}", "blue")
        self.add_log(f"[INFO] サーバーを起動します: {self.jar_path}", "blue", "help")
        self.add_log(f"[INFO] サーバーを起動します: {self.jar_path}", "green")
        self.add_log(f"[INFO] サーバーを起動します: {self.jar_path}", "green", "help")
        self.add_log(f"[INFO] RAM設定: min={self.min_ram}, max={self.max_ram}", "blue")
        self.add_log(f"[INFO] RAM設定: min={self.min_ram}, max={self.max_ram}", "blue" "help")
        
        # --- サーバー起動 ---
        self.server = subprocess.Popen(
            ["java", f"-Xmx{self.max_ram}G", f"-Xms{self.min_ram}G", "-jar", self.jar_path, "nogui"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1
        )
        
        print("[INFO] サーバー起動中...")
        self.add_log("[INFO] サーバー起動中...")
        self.add_log("[INFO] サーバー起動中...", "None", "help")
        threading.Thread(target=self.read_output, daemon=True).start()
    
    def read_output(self):
        self.box = self.log_boxes.get("main")  # mainタブのログボックスを使う
        if not self.box:
            return
        
        self.box.tag_config("error", foreground="red")
        self.box.tag_config("info", foreground="cyan")
        
        for line in iter(self.server.stdout.readline, ''):
            print("save_state:", save_state.get())
            self.line = line.strip()
            self.box.config(state="normal")
            
            if "ERROR" in self.line or "Exception" in self.line:
                self.add_log(f"{self.line}\n", "red", "help")
                self.box.insert("end", self.line + "\n", "error")
            elif "INFO" in self.line or "[INFO]" in self.line:
                self.add_log(f"{self.line}\n", "white", "help")
                self.box.insert("end", self.line + "\n", "info")
            else:
                self.add_log(f"{self.line}\n", "blue", "help")
                self.box.insert("end", self.line + "\n")
            
            if save_state.get(self):
                self.today = datetime.now().strftime("%Y-%m-%d")
                self.path = f"Manager_log/{self.today}.txt"
                os.makedirs(os.path.dirname(self.path), exist_ok=True)
                with open(self.path, "a", encoding="utf-8") as f:
                    f.write(f"{line}\n")
            self.box.see("end")
            self.box.config(state="disabled")
    
    def send_command(self, cmd: str):
        if self.server and self.server.stdin:
            self.server.stdin.write(cmd + "\n")
            self.server.stdin.flush()
            print(f"[cmd] {cmd}")
        else:
            print("[WARN] サーバーが起動していません。")
            self.add_log("[WARN] サーバーは起動していません。", "yellow", tab="help")
            self.add_log("[WARN] サーバーは起動していません。", "yellow", tab="main")
    
    def stop_server(self):
        if self.server is None:
            self.add_log("[WARN] サーバーは起動していません。", "yellow")
            self.add_log("[WARN] サーバーは起動していません。", "yellow", tab="help")
            return
        
        try:
            self.add_log("[INFO] サーバーを強制停止中...", "red")
            self.add_log("[INFO] サーバーを強制停止中...", "red", "help")
            self.terminate()  # 強制終了
            self.server.wait(timeout=10)
            self.add_log("[INFO] サーバーを停止しました。", "yellow")
            self.add_log("[INFO] サーバーを停止しました。", "yellow", "help")
        except Exception as e:
            self.pend_log(f"[ERROR] サーバー停止に失敗: {e}")
        finally:
            self.server = None
    
    def on_closing(self):
        self.stop_server()
        if self.server is not None:
            print("サーバーを停止しました。")
        else:
            print("GUIを終了しました。")
        win.destroy()
    
    def app(self):
        print("再起動します。")
        self.exe = sys.executable
        self.script = os.path.abspath(sys.argv[0])
        subprocess.Popen([self.exe, self.script])  # 新しいプロセスを起動
        os._exit(0)  # 今のGUIを終了
        return
    
    def config_reset(self):
        with open(function.CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(self.DEFAULT, f, indent=7, ensure_ascii=False)
        
        return self.DEFAULT

    def load_Extensions(self, window):
        self.extensions_folder = 'Extensions'  # 拡張機能が格納されているフォルダ
        os.makedirs(os.path.dirname("Extensions/temp.py"), exist_ok=True)
        
        if not os.path.exists(self.extensions_folder):
            print(f"{self.extensions_folder} フォルダが存在しません")
            return
        
        self.loaded_extensions = set()  # ← ここでセットを作る
        for filename in os.listdir(self.extensions_folder):
            if filename.endswith('.py') and filename != "__init__.py":  # __init__.py は除外
                self.extension_name = filename[:-3]
                
                if self.extension_name in self.loaded_extensions:  # すでにロード済みならスキップ
                    continue
                self.loaded_extensions.add(self.extension_name)
                try:
                    self.add_log(f"Loaded extension: {self.extension_name}", "green", "help")
                    self.add_log(f"Loaded extension: {self.extension_name}", "green")
                    print(f"Loaded extension: {self.extension_name}")
                    self.extension_module = importlib.import_module(f"Extensions.{self.extension_name}")
                    
                    if hasattr(self.extension_module, "extension_function"):
                        self.extension_module.extension_function(window)
                except Exception as e:
                    print(f"Error loading extension {self.extension_name}: {e}")
                    self.add_log(f"Error loading extension {self.extension_name}: {e}", "red", "help")
                    self.add_log(f"Error loading extension {self.extension_name}: {e}", "red", "main")

if __name__ == "__main__":
    win = tk.Tk()
    function = function__(win)
    function.fix()
    win.title("Server Manager Edit By MixPlus")
    win.geometry("910x490")
    win.minsize(910, 490)
    win.configure(bg=f"{function.bg}")
    win.protocol("WM_DELETE_WINDOW", function.on_closing)
    
    #紐付け
    frame_main, box_main, main_log_box = function.main_tab(win)
    function.show_frame(frame_main)
    frame_credits = function.credits_tab(win)
    frame_mods = function.mods_tab(win)
    frame_plugins = function.plugins_tab(win)
    frame_setting = function.setting_tab(win)
    frame_help = function.help_tab(win)
    
    
    
    
    #start
    start_button = tk.Button(frame_main, text="サーバー起動", command=function.start_server, bg=function.btn_color, fg=function.fg, font=("arial", 12), relief="flat")
    start_button.place(x=0, y=2, width=100, height=20)
    
    #Main
    btn_main = tk.Button(win, text="Main", command=lambda: function.show_frame(frame_main), bg=function.btn_color, fg=function.fg, font=("arial", 12), relief="flat")
    btn_main.place(x=0, y=0, width=100, height=20)
    
    #credits
    btn_credits = tk.Button(win, text="Credits", command=lambda: function.show_frame(frame_credits), bg=function.btn_color, fg=function.fg, font=("arial", 12), relief="flat",)
    btn_credits.place(x=101, y=0, width=100, height=20)
    
    #Mods
    btn_mods = tk.Button(win, text="Mods", command=lambda: function.show_frame(frame_mods), bg=function.btn_color, fg=function.fg, font=("arial", 12), relief="flat")
    btn_mods.place(x=202, y=0, width=100, height=20)
    
        #plugins
    btn_plugins = tk.Button(win, text="Plugins", command=lambda: function.show_frame(frame_plugins), bg=function.btn_color, fg=function.fg, font=("arial", 12), relief="flat")
    btn_plugins.place(x=303, y=0, width=100, height=20)
    
    #Settings
    btn_setting = tk.Button(win, text="Setting", command=lambda: function.show_frame(frame_setting), bg=function.btn_color, fg=function.fg, font=("arial", 12), relief="flat")
    btn_setting.place(x=404, y=0, width=100, height=20)
    
    #stop
    stop_button = tk.Button(frame_main, text="サーバー停止", command=function.stop_server, bg=function.btn_color, fg=function.fg, font=("arial", 12), relief="flat")
    stop_button.place(x=101, y=2, width=100, height=20)
    #restart
    restart_btn = tk.Button(frame_setting, text="GUI再起動", command=function.app, bg=function.btn_color, fg="red", font=("arial", 10))
    restart_btn.place(x=700, y=88, width=80, height=25)
    
    #config_reset
    config_reset_btn = tk.Button(frame_setting, text="コンフィグリセット", command=function.config_reset, bg=function.btn_color, fg="red", font=("arial", 12))
    config_reset_btn.place(x=758, y=440, width=150, height=25)
    
    #help
    btn_help = tk.Button(win, text="Help", command=lambda: function.show_frame(frame_help), bg=function.btn_color, fg=function.fg, font=("arial", 12), relief="flat")
    btn_help.place(x=505, y=0, width=100, height=20)
    
    
    
    function.show_frame(frame_main)
    
    app = function__(win)
    
    # 最初に Main タブを表示
    app.main_tab(win)
    
    function.load_Extensions(win)
    
    win.mainloop()

# No Console
# pyinstaller --onefile --windowed "Server Manager1_3_10.py"

#pyinstaller --onefile "Server Manager1_3_10.py"