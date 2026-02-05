MAIN_VERSION = "1_5_101"

import importlib.util
import tkinter as tk
import subprocess
import webbrowser
import traceback
import threading
import winsound
import shutil
import json
import sys
import os
from tkinter import filedialog, messagebox
from tkinter import colorchooser
from collections import deque
from datetime import datetime

def beep():
    if sys.platform.startswith("win"):
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)  # Windows標準警告音
    else:
        print("\a", end="", flush=True)  # Linux/macOS ターミナルベル

class Config:
    DEFAULT_CONFIG = {
    "server_jar": "",
    "btn_color": "#444444",
    "username": "user",
    "bg": "black",
    "fg": "white",
    "history_size": 10,
    "min_ram": "10",
    "max_ram": "10",
    "slots": "20",
    "server": False,
    "eula": False,
    "debug": False,
    "reset": False
    }
    
    def __init__(self):
        log = tk.Tk()
        log.withdraw()
        
        self.BASE_DIR = (
            os.path.dirname(sys.executable)
            if getattr(sys, "frozen", False)
            else os.path.dirname(os.path.abspath(__file__))
        )
        
        self.CONFIG_PATH = os.path.join(self.BASE_DIR, "config.json")
        self.EULA_PATH = os.path.join(self.BASE_DIR, "server", "eula.txt")
        
        self.MAX_FILE_SIZE = 300 #KB
        self.MAX_FILE_SIZE *= 1024
        
        
        self.load()
        
        if self.reset:
            self._reset_config()
            self.load()
    
    def load(self):
        if os.path.exists(self.CONFIG_PATH) and os.path.getsize(self.CONFIG_PATH) > self.MAX_FILE_SIZE:
            beep()
            reset = messagebox.askyesno("警告", f"config.jsonのファイルサイズが{self.MAX_FILE_SIZE // 1024}KBを超えたためリセットされます")
            print("ファイルサイズが大きすぎたためコンフィグがリセットされました")
            if reset:
                self._reset_config()
            else:
                beep()
                false = messagebox.askyesno("警告", "本当によろしいですか?")
                if false:
                    sys.exit()
                else:
                    self._reset_config()
        
        if not os.path.exists(self.CONFIG_PATH):
            self.config_dict = self.DEFAULT_CONFIG.copy()
            self.save()
        
        try:
            with open(self.CONFIG_PATH, encoding="utf-8") as f:
                self.config_dict = json.load(f)
        except (json.JSONDecodeError, OSError):
            self._reset_config()
        
        self.server_jar = self.config_dict.get("server_jar", "")
        self.min_ram = self.config_dict.get("min_ram", 10)
        self.max_ram = self.config_dict.get("max_ram", 10)
        self.slots = self.config_dict.get("slots", 20)
        self.username = self.config_dict.get("username", "user")
        self.bg = self.config_dict.get("bg", "black")
        self.fg = self.config_dict.get("fg", "white")
        self.btn_color = self.config_dict.get("btn_color", "#444444")
        self.server_state = self.config_dict.get("server", None)
        self.history_size = int(self.config_dict.get("history_size", 10))
        self.eula = self.config_dict.get("eula", False)
        self.debug = self.config_dict.get("debug", False)
        self.reset = self.config_dict.get("reset", False)
    
    def save(self, key=None, data=None, cast=str):
        if key is not None:
            if not callable(cast):
                raise TypeError("cast must be callable")
            self.config_dict[key] = cast(data)
            
        
        with open(self.CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(self.config_dict, f, indent=4, ensure_ascii=False)
    
    def remove(self, key):
        self.config_dict.pop(key, None)
        
        with open(self.CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(self.config_dict, f, indent=4, ensure_ascii=False)
    
    def _reset_config(self):
        self.config_dict = self.DEFAULT_CONFIG.copy()
        self.save()

class MAIN:
    def __init__(self, win):
        global MAIN_INSTANCE
        MAIN_INSTANCE = self
        #class
        self.CFG = Config()
        self.tab = TAB(self.CFG, self,)
        self.gui = GUI(win, self.CFG, self.tab, self)
        self.win = win
        self.context = AppContext(
            cfg=self.CFG,
            main=self,
            tab=self.tab,
            gui=self.gui
        )
        #path
        self.BASE_DIR = (
            os.path.dirname(sys.executable)
            if getattr(sys, "frozen", False)
            else os.path.dirname(os.path.abspath(__file__))
        )
        self.SERVER_DIR = os.path.join(self.BASE_DIR, "server")
        self.BACKUP_DIR = os.path.join(self.BASE_DIR, "backup")
        self.EXTENSIONS_PATH = os.path.join(self.BASE_DIR, "Extensions")
        
        os.makedirs(self.SERVER_DIR, exist_ok=True)
        os.makedirs(self.BACKUP_DIR, exist_ok=True)
        os.makedirs(self.EXTENSIONS_PATH, exist_ok=True)
        
        self.clip = deque(maxlen=self.CFG.history_size)
        self.clip_index = 0
        #log
        self.log_boxes = {}
        
        self.server = None
        
        self.gui.run(self.load_extensions)
    
    def on_enter(self, event=None):
        raw_cmd = self.tab.Entry_main.get()
        if not raw_cmd:
            return
        
        cmd = raw_cmd.strip()
        if not cmd:
            return
        
        self.add_log(f"<{self.CFG.username}> {cmd}", "#00FF1f"); self.send_command(cmd)
        self.clip.append(cmd)
        self.clip_index = 0
        self.tab.Entry_main.delete(0, tk.END)
        
        parts = cmd.split()
        if not parts:
            return
        
        # custom commands
        if parts[0] == "clip":
            data = ", ".join(map(str, self.clip))
            print(data)
            self.add_log(data)
        
        elif cmd.startswith("."):
            if self.server and self.server.stdin:
                self.send_command(f"/say {cmd[1:]}")
        
        elif parts[0] in ("ver", "version"):
            msg = f"ServerManager:{MAIN_VERSION}"
            print(msg)
            self.add_log(msg, "#0044FF")
        
        elif parts[0] == "clear":
            self.clear_all()
        
        elif parts[0] == "server":
            print(f"Server: {self.server}"); self.add_log(f"Server: {self.server}", "#FF00C8")
        
        # config / cfg
        elif parts[0] in ("config", "cfg"):
            
            if len(parts) < 2:
                self.add_log("Usage: config <reset|view|set|remove>", "red")
                return
            
            sub = parts[1]
            
            if sub == "reset":
                self.CFG._reset_config()
                self.add_log("Config reset", "red")
            
            elif sub in ("view", "json", "data"):
                self.add_log(json.dumps(self.CFG.config_dict, indent=4))
            
            elif sub == "set":
                if len(parts) < 5:
                    self.add_log("Usage: config set <key> <value> <type>", "red")
                    return
                
                key = parts[2]
                value_str = parts[3]
                type_str = parts[4]
                
                CASTERS = {
                    "int": int,
                    "float": float,
                    "str": str,
                    "bool": lambda x: x if isinstance(x, bool) else str(x).lower() == "true",
                }
                
                caster = CASTERS.get(type_str)
                if not caster:
                    self.add_log(f"Unknown type: {type_str}", "red")
                    return
                
                try:
                    value = caster(value_str)
                except ValueError:
                    self.add_log(f"Invalid value for type {type_str}", "red")
                    return
                
                self.CFG.save(key, value, caster)
                self.add_log(f"Config set: {key} = {value} ({type_str})", "green")
            
            elif sub == "remove":
                if len(parts) < 3:
                    self.add_log("Usage: config remove <key>", "red")
                    return
                key = parts[2]
                self.CFG.remove(key)
        
        elif parts[0] == "Extensions":
            self.__Extensions__()
    
    def add_log(self, text, color=None, tab="main"):
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
        
        box.see("end"); box.config(state="disabled")
    
    def clip_up(self, event):
        if not self.clip:
            return "break"
        
        if self.clip_index < len(self.clip):
            self.clip_index += 1
            
        self.tab.Entry_main.delete(0, tk.END)
        self.tab.Entry_main.insert(0, self.clip[-self.clip_index])
        
        return "break"
    
    def clip_down_(self, event):
        if not self.clip:
            return "break"
        
        if self.clip_index > 1:
            self.clip_index -= 1
            self.tab.Entry_main.delete(0, tk.END)
            self.tab.Entry_main.insert(0, self.clip[-self.clip_index])
        else:
            # 最新（入力なし状態）に戻る
            self.clip_index = 0
            self.tab.Entry_main.delete(0, tk.END)
            
        return "break"
    
    def clear_all(self):
        self.clip.clear()
        self.clip_index = 0
        
        self.tab.Entry_main.delete(0, tk.END)
        
        for box in self.tab.text:
            box.config(state="normal")
            box.delete("1.0", tk.END)
            box.config(state="disabled")
        self.add_log("削除されました", "red")
        self.add_log(self.tab.credit, None, "credit")
        self.add_log("edit by MixPlus", "#00FFFF", "credit")
    
    def read_output(self):
        box = self.log_boxes.get("main")  # mainタブのログボックスを使う
        if not box:
            return
        
        box.tag_config("error", foreground="red"); box.tag_config("info", foreground="cyan")
        for line in iter(self.server.stdout.readline, ''):
            line = line.strip()
            if "Yggdrasil Key Fetcher/ERROR" in line:
                self.add_log(line, "red")
                box.insert("end", line + "\n", "error")
                continue
            if line.startswith("at "):
                continue
            
            box.config(state="normal")
            if "ERROR" in line or "Exception" in line:
                    self.add_log(f"{line}\n", "red", "help"); box.insert("end", line + "\n", "error")
            elif "INFO" in line or "[INFO]" in line:
                self.add_log(f"{line}\n", "white", "help"); box.insert("end", line + "\n", "info")
            elif "WARN" in line or "[WARN]" in line:
                self.add_log(f"{line}\n", "#FCF803",); box.insert("end", line + "\n", "warn")
            else:
                self.add_log(f"{line}\n", "blue", "help"); box.insert("end", line + "\n")
            
            print(line); box.see("end"); box.config(state="disabled")
    
    def server_start(self):
        if self.server is not None:
            print("[WARN] すでにサーバーが起動しています。"); self.add_log("[WARN] すでにサーバーが起動しています。")
            return
        
        elif not os.path.exists(self.CFG.CONFIG_PATH):
            print("[ERROR] config.json が見つかりません。"); self.add_log("[ERROR] config.json が見つかりません。")
            return
        
        if not self.CFG.server_jar or not os.path.exists(self.CFG.server_jar):
            print("[ERROR] サーバーjarファイルが見つかりません。")
            self.add_log("[ERROR] サーバーjarファイルが見つかりません。", "red")
            return
        
        print(f"[INFO] サーバーを起動します: {self.CFG.server_jar}")
        print(f"[INFO] RAM設定: min={self.CFG.min_ram}GB, max={self.CFG.max_ram}GB")
        self.add_log(f"[INFO] サーバーを起動します: {self.CFG.server_jar}")
        self.add_log(f"[INFO] RAM設定: min={self.CFG.min_ram}GB, max={self.CFG.max_ram}")
        
        self.server = subprocess.Popen(
            ["java", f"-Xmx{self.CFG.max_ram}G", f"-Xms{self.CFG.min_ram}G", "-jar", self.CFG.server_jar, "nogui"],
            cwd=self.SERVER_DIR,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1
        )
        threading.Thread(target=self.read_output, daemon=True).start()
        self.CFG.save("server", True, bool)
    
    def stop_server(self):
        if self.server is None:
            self.add_log("[WARN] サーバーは起動していません。", "yellow")
            return
        
        try:
            self.send_command("/stop")
            self.add_log("[INFO] サーバーを停止中...", "red")
            self.win.after(10000, self.server.terminate)  # OK
            self.add_log("[INFO] サーバーを停止しました。", "yellow")
        except Exception as e:
            self.add_log(f"[ERROR] サーバー停止に失敗: {e}")
        finally:
            self.server = None
            self.CFG.save("server", False, bool)
    
    def send_command(self, cmd: str):
        if cmd.startswith("/"):
            if self.server and self.server.stdin:
                self.server.stdin.write(cmd + "\n"); self.server.stdin.flush(); print(f"[cmd] {cmd}")
            else:
                print("[WARN] サーバーが起動していません。")
                self.add_log("[WARN] サーバーは起動していません。", "yellow")
    
    def server_backup(self):
        print(datetime.now())
        BACKUP_DIR = os.path.join(self.BACKUP_DIR, datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        shutil.copytree(self.SERVER_DIR, BACKUP_DIR, dirs_exist_ok=True)
        print("Backup created:", BACKUP_DIR)
        self.add_log(f"Backup created:{BACKUP_DIR}")
        messagebox.showinfo("情報", "バックアップが完了しました")
    
    def load_extensions(self):
            path = self.EXTENSIONS_PATH
            
            for file in os.listdir(path):
                if not file.endswith(".py"):
                    continue
                if file.startswith("_"):
                    continue
                
                full = os.path.join(path, file)
                name = f"ext_{file[:-3]}"  # 衝突回避
                
                try:
                    spec = importlib.util.spec_from_file_location(name, full)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    
                    if hasattr(mod, "apply"):
                        mod.apply(self.context)
                        self.add_log(f"[EXT] loaded: {file}", "cyan")
                    else:
                        self.add_log(f"[EXT] skip (no apply): {file}", "yellow")
                    
                except Exception:
                    self.add_log(f"[EXT] error: {file}", "red")
                    traceback.print_exc()

class TAB:
    def __init__(self, cfg, main):
        self.main = main
        self.CFG = cfg
        
        # 見た目制御用（色変更）
        self.frames = []
        self.labels = []
        self.buttons = []
        self.scrollbars = []
        self.entry = []
        self.text = []
        self.listboxes = []
        self.Scale = []
    
    def main_tab(self, parent):
        frame_main = tk.Frame(parent, bg=self.CFG.bg); frame_main.place(x=0, y=20, width=910, height=490)
        main_label = tk.Label(frame_main, text="Main", bg=self.CFG.bg, fg=self.CFG.fg, font=("arial", 12)); main_label.pack()
        
        self.log_main = tk.Text(
            frame_main,
            bg=self.CFG.bg, fg=self.CFG.fg,
            font=("arial", 12), state="disabled"); self.log_main.place(x=0, y=30, width=900, height=405)
        
        scroll = tk.Scrollbar(frame_main, command=self.log_main.yview); scroll.place(x=890, y=30, height=400)
        self.log_main.config(yscrollcommand=scroll.set)
        
        self.Entry_main = tk.Entry(frame_main, width=90, font=("arial", 15), bg=self.CFG.btn_color, fg=self.CFG.fg); self.Entry_main.place(y=440, x=0)
        
        server_btn = tk.Button(frame_main, text="start server", command=self.main.server_start, bg=self.CFG.btn_color, fg=self.CFG.fg, font=("arial", 12), relief="flat") ; server_btn.place(x=0, y=2, width=100, height=20)
        stop_server_btn = tk.Button(frame_main, text="stop server", command=self.main.stop_server, bg=self.CFG.btn_color, fg=self.CFG.fg, font=("arial", 12), relief="flat") ; stop_server_btn.place(x=101, y=2, width=100, height=20)
        
        #setting
        self.frames.append(frame_main)
        self.labels.append(main_label)
        self.text.append(self.log_main)
        self.scrollbars.append(scroll)
        self.entry.append(self.Entry_main)
        self.buttons.extend([server_btn, stop_server_btn])
        
        self.Entry_main.bind("<Return>", self.main.on_enter)
        self.Entry_main.bind("<Up>", self.main.clip_up)
        self.Entry_main.bind("<Down>", self.main.clip_down_)
        self.main.log_boxes['main'] = self.log_main
        return frame_main, main_label
    
    def credit_tab(self, parent):
        frame_credit = tk.Frame(parent, bg=self.CFG.bg); frame_credit.place(x=0, y=20, width=910, height=490)
        credit_label = tk.Label(frame_credit, text="Credit", bg=self.CFG.bg, fg=self.CFG.fg, font=("arial", 12)); credit_label.pack()
        
        log_credit = tk.Text(
            frame_credit,
            bg=self.CFG.bg, fg=self.CFG.fg,
            font=("arial", 12), state="disabled"); log_credit.place(x=0, y=30, width=900, height=400)
        
        scroll = tk.Scrollbar(frame_credit, command=log_credit.yview); scroll.place(x=890, y=30, height=400)
        log_credit.config(yscrollcommand=scroll.set)
        
        self.main.log_boxes['credit'] = log_credit
        self.import_list = """
import tkinter as tk
import subprocess
import webbrowser
import threading
import importlib
import builtins
import winsound
import shutil
import json
import sys
import os
from tkinter import filedialog, messagebox, ttk
from tkinter import colorchooser
from collections import deque
"""
        
        self.credit = f"""
このツールはminecraftサーバーを管理するために作られました。
Open AI chatgpt   Microsoft Copilot
との会話によって設計されました。
guiの設計などの情報をいただきました。
このツールはまだ未完成ですが
完成してもおそらくアップデートが続くでしょう。
作者のほしい機能などを搭載していきます。
できるだけ一つのファイルにしようと思っていますが複数のファイル版も作成する予定です。
                    協力者:2                     テスター:1
Open AI chatgpt   Microsoft Copilot   MixPlus

利用したモジュール\n{self.import_list}



"""
        self.main.add_log(self.credit, None, "credit")
        self.main.add_log("edit by MixPlus", "#00FFFF", "credit")
        
        self.frames.append(frame_credit)
        self.labels.append(credit_label)
        self.text.append(log_credit)
        self.scrollbars.append(scroll)
        return frame_credit, credit_label, log_credit, scroll
    
    def mods_tab(self, parent):
        frame_mods = tk.Frame(parent, bg=self.CFG.bg); frame_mods.place(x=0, y=20, width=910, height=490)
        mods_label = tk.Label(frame_mods, text="Mods", bg=self.CFG.bg, fg=self.CFG.fg, font=("arial", 12)); mods_label.pack()
        
        listbox = tk.Listbox(frame_mods, font=("arial", 12), bg=self.CFG.bg, fg=self.CFG.fg); listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll = tk.Scrollbar(frame_mods, command=listbox); scroll.place(x=890, y=30, height=400)
        
        listbox.config(yscrollcommand=scroll.set)
        
        mods_path = os.path.join(self.CFG.BASE_DIR, "server", "mods")
        if os.path.exists(mods_path):
            for item in os.listdir(mods_path):
                listbox.insert(tk.END, item)
        else:
            listbox.insert(tk.END, "modsフォルダが見つかりませんでした")
        self.frames.append(frame_mods)
        self.labels.append(mods_label)
        self.listboxes.append(listbox)
        self.scrollbars.append(scroll)
        return frame_mods
    
    def plugins_tab(self, parent):
        frame_plugin = tk.Frame(parent, bg=self.CFG.bg); frame_plugin.place(x=0, y=20, width=910, height=490)
        plugin_label = tk.Label(frame_plugin, text="Plugin", bg=self.CFG.bg, fg=self.CFG.fg, font=("arial", 12)); plugin_label.pack()
        
        listbox = tk.Listbox(frame_plugin, font=("arial", 12), bg=self.CFG.bg, fg=self.CFG.fg); listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll = tk.Scrollbar(frame_plugin, command=listbox); scroll.place(x=890, y=30, height=400)
        
        listbox.config(yscrollcommand=scroll.set)
        
        plugin_path = os.path.join(self.CFG.BASE_DIR, "server", "plugins")
        if os.path.exists(plugin_path):
            for item in os.listdir(plugin_path):
                listbox.insert(tk.END, item)
        else:
            listbox.insert(tk.END, "pluginsフォルダが見つかりませんでした")
        self.frames.append(frame_plugin)
        self.labels.append(plugin_label)
        self.listboxes.append(listbox)
        self.scrollbars.append(scroll)
        return frame_plugin
    
    def setting_tab(self, parent):
        self.frame_setting = tk.Frame(parent, bg=self.CFG.bg); self.frame_setting.place(x=0, y=20, width=910, height=490)
        setting_label = tk.Label(self.frame_setting, text="Setting", bg=self.CFG.bg, fg=self.CFG.fg, font=("arial", 12)); setting_label.pack()
        
        reference = tk.Button(self.frame_setting, text="reference", command=self.select_jar, bg=self.CFG.btn_color, fg=self.CFG.fg, font=("arial", 10)); reference.place(x=700, y=58)
        
        settings = [
        ("Server JAR File", "server_jar", 60),
        ("Username", "username", 220),
        ("background color", "bg", 260),
        ("Text color", "fg", 300),
        ("Button Color", "btn_color", 340),
        ]
        
        settings_type = [
            ("Minimum RAM", "min_ram", 100, "GB"),
            ("Max RAM", "max_ram", 140, "GB"),
            ("Number of slots", "slots", 180, None),
        ]
        
        pick = [
            ("bg", 260),
            ("fg", 300),
            ("btn_color", 340),
        ]
        
        self.setting_entry_dict = {}
        
        for text, key, y in settings:
            text_label = tk.Label(self.frame_setting, text=text, bg=self.CFG.btn_color, fg=self.CFG.fg, font=("arial", 12))
            text_label.place(x=50, y=y)
            
            self.setting_entry = tk.Entry(self.frame_setting, bg=self.CFG.btn_color, fg=self.CFG.fg, font=("arial", 12), width=40)
            self.setting_entry.insert(0, self.CFG.config_dict.get(key, ""))
            self.setting_entry.place(x=250, y=y)
            
            self.setting_entry_dict[key] = self.setting_entry
            # フォーカスを離したときに保存
            self.setting_entry.bind("<FocusOut>", lambda e, k=key, ent=self.setting_entry: self.CFG.save(k, ent.get()))
            
            # reset ボタンも個別の Entry を渡す
            reset = tk.Button(self.frame_setting, text="Rest", 
                            command=lambda k=key, ent=self.setting_entry: self.reset_color_one(k, ent),
                            bg=self.CFG.btn_color, fg=self.CFG.fg, font=("arial", 10))
            reset.place(x=620, y=y, width=70)
            
            self.labels.append(text_label)
            self.entry.append(self.setting_entry)
            self.buttons.append(reset)
        
        for text, key, y, unit in settings_type:
            if unit is None:
                unit = ""

            default = int(self.CFG.DEFAULT_CONFIG.get(key, 10))

            value_label = tk.Label(
                self.frame_setting,
                text=f"{default}{unit}",
                font=("arial", 12),
                bg=self.CFG.bg,
                fg=self.CFG.fg
            )
            value_label.place(x=200, y=y)

            text_label = tk.Label(
                self.frame_setting,
                text=text,
                bg=self.CFG.btn_color,
                fg=self.CFG.fg,
                font=("arial", 12)
            )
            text_label.place(x=50, y=y)

            scale = tk.Scale(
                self.frame_setting,
                from_=1,
                to=50,
                orient="horizontal",
                font=("arial", 12),
                showvalue=False,
                bg=self.CFG.bg,
                fg=self.CFG.fg,
                command=lambda v, k=key, lbl=value_label, u=unit: (
                    lbl.config(text=f"{v}{u}"),
                    self.CFG.save(k, str(v))
                )
            )
            scale.place(x=250, y=y, width=363)
            scale.set(default)
            
            # Reset ボタン
            reset_btn = tk.Button(
                self.frame_setting,
                text="Reset",
                font=("arial", 10),
                bg=self.CFG.btn_color,
                fg=self.CFG.fg,
                command=lambda s=scale, d=default, lbl=value_label, k=key, u=unit: (
                    s.set(d),
                    lbl.config(text=f"{d}{u}"),
                    self.CFG.save(k, str(d))
                )
            )
            reset_btn.place(x=620, y=y, width=70)
            self.buttons.append(reset_btn)
            self.labels.extend([value_label, text_label])
        
        for key, y in pick:
            btn_pick = tk.Button(self.frame_setting, text="Select Color", command=lambda k=key: self.pick_color(k), bg=self.CFG.btn_color, fg=self.CFG.fg)
            btn_pick.place(x=700, y=y)
            self.buttons.append(btn_pick)
        
        self.frames.append(self.frame_setting)
        self.labels.extend([setting_label, text_label])
        self.entry.extend([self.setting_entry])
        self.buttons.extend([reference, reset])
        return self.frame_setting, reference
    
    def Extensions_tab(self, parent):
        self.frame_Extension = tk.Frame(parent, bg=self.CFG.bg); self.frame_Extension.place(x=0, y=20, width=910, height=490)
        label_Extension = tk.Label(self.frame_Extension, text="Extensions", bg=self.CFG.bg, fg=self.CFG.fg, font=("arial", 12)); label_Extension.pack()
        
        listbox = tk.Listbox(self.frame_Extension, font=("arial", 12), bg=self.CFG.bg, fg=self.CFG.fg); listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll = tk.Scrollbar(self.frame_Extension, command=listbox); scroll.place(x=890, y=30, height=400)
        if os.path.exists(self.main.EXTENSIONS_PATH):
            if self.main.EXTENSIONS_PATH.endswith('.py') and self.main.EXTENSIONS_PATH != "__init__.py":
                for item in os.listdir(self.main.EXTENSIONS_PATH):
                    listbox.insert(tk.END, item)
        else:
            listbox.insert(tk.END, "Extensionsフォルダが見つかりませんでした")
        self.frames.append(self.frame_Extension)
        self.labels.append(label_Extension)
        self.listboxes.append(listbox)
        self.scrollbars.append(scroll)
        return self.frame_Extension
    
    def more_setting(self, parent):
        self.frame_more = tk.Frame(parent, bg=self.CFG.bg); self.frame_more.place(x=0, y=20, width=910, height=490)
        label_more = tk.Label(self.frame_more, text="More Settings", bg=self.CFG.bg, fg=self.CFG.fg, font=("arial", 12)); label_more.pack()
        
        backup = tk.Button(self.frame_more, text="backup", command=self.main.server_backup, bg=self.CFG.bg, fg=self.CFG.fg, font=("arial", 12)); backup.place(x=723, y=30, width=100, height=25)
        
        max_clip = tk.Label(self.frame_more, text="Maximum Number of Clips", bg=self.CFG.bg, fg=self.CFG.fg, font=("arial", 12)); max_clip.place(x=50, y=60)
        
        value_label = tk.Label(
                        self.frame_more,
                        text=f"0",
                        font=("arial", 12),
                        bg=self.CFG.bg,
                        fg=self.CFG.fg
                    )
        value_label.place(x=250, y=60)
        
        scale = tk.Scale(
                        self.frame_more,
                        from_=1,
                        to=50,
                        orient="horizontal",
                        font=("arial", 12),
                        showvalue=False,
                        bg=self.CFG.bg,
                        fg=self.CFG.fg,
                        command=lambda v, k="history_size", lbl=value_label: (
                            lbl.config(text=f"{v}"),
                            self.CFG.save(k, str(v))
                        )
                    )
        scale.place(x=250, y=60)
        return self.frame_more
    
    def select_jar(self):
        path = filedialog.askopenfilename(title="サーバーの .jar ファイルを選んでね", filetypes=[("Java Archive", "*.jar"), ("すべてのファイル", "*.*")])
        if path:
            box = self.setting_entry_dict.get("server_jar", "")
            box.delete(0, tk.END)
            box.insert(0, path)
            self.CFG.save("server_jar", path)
            print("選ばれたファイル:", path)
    
    def apply_colors(self):
        for f in self.frames:
            f.configure(bg=self.CFG.bg)
        
        for l in self.labels:
            l.configure(bg=self.CFG.bg, fg=self.CFG.fg)
        
        for e in self.entry:
            e.configure(bg=self.CFG.btn_color, fg=self.CFG.fg)
        
        for t in self.text:
            t.configure(bg=self.CFG.bg, fg=self.CFG.fg)
        
        for b in self.buttons:
            b.configure(bg=self.CFG.btn_color, fg=self.CFG.fg)
        
        for list in self.listboxes:
            list.configure(bg=self.CFG.bg, fg=self.CFG.fg)
        
        for Scale in self.Scale:
            Scale.configure(bg=self.CFG.bg, fg=self.CFG.fg)
        
        
        if self.CFG.debug:
            all_widgets = [self.frames, self.labels, self.entry, self.text, self.buttons]
            for lst in all_widgets:
                print(", ".join([str(x) for x in lst]))  # map より確実
    
    def reset_color_one(self, key, entry):
        default = self.CFG.DEFAULT_CONFIG.get(key)
        if default is None:
            return
        entry.delete(0, tk.END)
        entry.insert(0, default)
        self.CFG.save(key, default)
    
    def pick_color(self, key):
        color = colorchooser.askcolor(title=f"Select the color of {key}")
        if not color[1]:
            return
        
        entry = self.setting_entry_dict[key]
        if entry:
            entry.delete(0, tk.END)
            entry.insert(0, color[1])
            setattr(self, key, color[1])
            self.CFG.save(key, entry.get())
            self.apply_colors()

class GUI:
    def __init__(self, win, cfg, tab, main):
        self.main = main
        self.tab = tab
        self.CFG = cfg
        self.after_ids = []
        self.win = win; self.setting_gui()
        self.eula()
        
        self.reload_config_loop()
    
    def setting_gui(self):
        self.win.title(f"Server Manager")
        self.win.geometry("910x490")
        self.win.minsize(910, 490)
        self.win.configure(bg=self.CFG.bg)
        self.win.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def show_frame(self, frame):
        frame.tkraise()
    
    def run(self, load):
        self.main_frame, _ = self.tab.main_tab(self.win)
        self.credit_frame, _, _, _ = self.tab.credit_tab(self.win)
        self.mods_frame = self.tab.mods_tab(self.win)
        self.plugin_frame = self.tab.plugins_tab(self.win)
        self.setting_frame, _ = self.tab.setting_tab(self.win)
        self.Extension_frame = self.tab.Extensions_tab(self.win)
        self.more_frame = self.tab.more_setting(self.win)
        #button
        return_btn = tk.Button(self.tab.frame_Extension, text="←Return", command=lambda: self.show_frame(self.setting_frame), bg=self.CFG.btn_color, fg=self.CFG.fg, font=("arial", 10)); return_btn.place(x=845, y=0)
        #restart
        restart_btn = tk.Button(self.tab.frame_setting, text="Restart", command=self.app, bg=self.CFG.btn_color, fg=self.CFG.fg, font=("arial", 10)); restart_btn.place(x=855, y=445)#x=758, y=410
        
        
        #main
        btn_main = tk.Button(
            self.win, text="Main",
            bg=self.CFG.btn_color, fg=self.CFG.fg,
            command=lambda: self.show_frame(self.main_frame),
            relief="flat", font=("arial", 12)); btn_main.place(x=0, y=0, width=100, height=20)
        
        #credit
        btn_credit = tk.Button(
            self.win, text="Credit",
            bg=self.CFG.btn_color, fg=self.CFG.fg,
            command=lambda: self.show_frame(self.credit_frame),
            relief="flat", font=("arial", 12)); btn_credit.place(x=101, y=0, width=100, height=20)
        
        #mods
        btn_mods = tk.Button(
            self.win, text="Mods",
            bg=self.CFG.btn_color, fg=self.CFG.fg,
            command=lambda: self.show_frame(self.mods_frame),
            relief="flat", font=("arial", 12)); btn_mods.place(x=202, y=0, width=100, height=20)
        
        #plugins
        btn_plugins = tk.Button(
            self.win, text="Plugins",
            bg=self.CFG.btn_color, fg=self.CFG.fg,
            command=lambda: self.show_frame(self.plugin_frame),
            relief="flat", font=("arial", 12)); btn_plugins.place(x=303, y=0, width=100, height=20)
        
        #setting
        btn_setting = tk.Button(
            self.win, text="Settings",
            bg=self.CFG.btn_color, fg=self.CFG.fg,
            command=lambda: self.show_frame(self.setting_frame),
            relief="flat", font=("arial", 12)); btn_setting.place(x=404, y=0, width=100, height=20)
        
        #Extension
        btn_Extension = tk.Button(
            self.tab.frame_setting, text="extensions",
            bg=self.CFG.btn_color, fg=self.CFG.fg,
            command=lambda: self.show_frame(self.Extension_frame),
            font=("arial", 10)); btn_Extension.place(x=700, y=90)
        
        #More Settings
        btn_more = tk.Button(
            self.tab.frame_setting, text="more settings",
            bg=self.CFG.btn_color, fg=self.CFG.fg,
            command=lambda: self.show_frame(self.more_frame),
            font=("arial", 10)); btn_more.place(x=700, y=123)
        
        
        self.tab.buttons.extend([
            btn_main, btn_credit, btn_mods,
            btn_plugins, btn_setting,
            btn_Extension, return_btn,
            btn_more, restart_btn])
        
        self.show_frame(self.main_frame)
        
        if self.CFG.server_state:
            self.main.add_log("\n以前サーバーが起動したまま。停止した可能性があります\n", "red")
        load()
        self.win.mainloop()
    
    def reload_config_loop(self):
        if not (self.win and self.win.winfo_exists()):
            return
        #color update
        self.tab.apply_colors()
        self.win.configure(bg=self.CFG.bg)
        self.CFG.load()
        
        self.after_ids.append(self.win.after(1000, self.reload_config_loop))
        return
    
    def eula(self):
        if not self.CFG.eula:
            self.win.withdraw()
            beep()
            answer = messagebox.askyesno(
            "Minecraft EULA",
            "Minecraft EULA (https://aka.ms/MinecraftEULA) に同意しますか？"
        )
            if answer:
                self.CFG.save("eula", True, bool)
                self.win.deiconify()
            else:
                webbrowser.open("https://aka.ms/MinecraftEULA")
                sys.exit()
        elif self.CFG.eula:
            with open(self.CFG.EULA_PATH, "w", encoding="utf-8") as f:
                f.write("#By changing the setting below to TRUE you are indicating your agreement to our EULA\n")
                f.write("eula=true\n")
        
        self.after_ids.append(self.win.after(5000, self.eula))
    
    def on_close(self):
        self.main.stop_server()
        for id in self.after_ids:
            self.win.after_cancel(id)
        self.after_ids.clear()
        self.win.destroy()
        sys.exit()
        return
    
    def app(self, reset=False):
        if reset:
            self.cfg._reset_config()
        exe = sys.executable; script = os.path.abspath(sys.argv[0])
        subprocess.Popen([exe, script]); self.on_close()
        return

class AppContext:
    def __init__(self, cfg: Config, main: MAIN, tab: TAB, gui: GUI):
        self.cfg = cfg
        self.main = main
        self.tab = tab
        self.gui = gui

if __name__ == "__main__":
    print(f'''
pyinstaller --onefile "{__file__}"

pyinstaller --onefile --noconsole "{__file__}"

pyinstaller --onefile --icon=icon.ico "{__file__}"
''')
    win = tk.Tk()
    main = MAIN(win)
