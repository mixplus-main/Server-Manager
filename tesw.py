"""
フレーム
self.frame_(parent)

ラベル
self.label("Main")

ログボックス(表示)
self.log_box_()

スクロールバー
self.scrollbar_()
"""




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
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.CONFIG_PATH = "config.json"
        self.btn_color = "#444444"
        self.layout_mode = "pack"   # デフォルトレイアウト
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
        self.win.protocol("WM_DELETE_WINDOW", self.on_closing)
        
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
            }
        
        print("未実装: help\nこれはサーバーの管理目的です。\nファイル生成json保存やファイルの読み込み実行を理解できていません。\nこれがすべて実装されるとサーバー用のjarファイルeulaの同意\nJDKが必須です! JDK機能を搭載するかもしれませんが\njavaサーバーのみです。 jarファイルを選択してください。\nポート開放やipなどのサポートはありません。\nEdit By MixPlus")
        
        try:
            with open(self.CONFIG_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception as e:
            self.fix()
        
        self.color_ch()
        
    def fix(self):
        with open(self.CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(self.CONFIG, f, indent=4, ensure_ascii=False)
            return
        return
    
    def on_closing(self):
        self.stop_server()
        self.win.destroy()
        if self.server is not None:
            print("サーバーを停止しました。")
        else:
            print("GUIを終了しました。")
    
    def stop_server(self):
        global server
        if self.server is None:
            #self.add_log("[WARN] サーバーは起動していません。", "yellow")
            #self.add_log("[WARN] サーバーは起動していません。", "yellow", tab="help")
            return
        try:
            self.dd_log("[INFO] サーバーを強制停止中...", "red")
            #self.add_log("[INFO] サーバーを強制停止中...", "red", "help")
            self.server.terminate()  # 強制終了
            self.server.wait(timeout=10)
            #self.add_log("[INFO] サーバーを停止しました。", "yellow")
            #self.add_log("[INFO] サーバーを停止しました。", "yellow", "help")
        except Exception as e:
            self.dd_log(f"[ERROR] サーバー停止に失敗: {e}")
        finally:
            self.server = None
    
    def color_ch(self):
        global username, fg, bg, btn_color
        
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
    
    def gui(self):
        self.frame_main, self.box_main, self.log_box = self.main_tab(win)
        self.show_frame(self.frame_main)
        self.frame_credits = self.credits_tab(win)
        self.frame_mods = self.mods_tab(win)
        self.frame_plugins = self.plugins_tab(win)
        self.frame_setting = self.setting_tab(win)
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
        
        #button
        self.btn_(self.frame_setting, "GUI再起動", command=self.app, bg=self.btn_color, fg="red", font=("arial", 10), layout_mode="place", x=700, y=88, width=80, height=25)
        self.btn_(self.frame_setting, "コンフィグリセット", command=self.config_reset, bg=self.btn_color, fg="red", layout_mode="place", x=758, y=440, width=150, height=25)
        
    def main_tab(self, parent):
        self.frame_(parent)
        self.label("Main")
        self.log_box_()
        self.scrollbar_()
        self.text_box = tk.Entry(self.frame, width=90, font=("arial", 15), bg=self.btn_color, fg=self.fg)
        self.text_box.place(y=440, x=0)
        self.text_box.bind("<Return>", self.on_enter)
        self.log_boxes['main'] = self.log_box
        return self.frame, self.text_box, self.log_box
    
    def credits_tab(self, parent):
        self.frame_(parent)
        self.scrollbar_()
        self.label("Credits")
        
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
        self.label("edit", fg="blue",  layout_mode="place", x=50, y=350)
        self.label("by", fg="#FFAA00", layout_mode="place", x=100, y=350)
        self.label("MixPlus", fg="#00FF00", x=140, y=350)
        for i, line in enumerate(credit):
            
            self.label(line, bg=self.bg, fg=self.fg, layout_mode="place", x=30, y=30 + i * 25)
        return self.frame
    
    def mods_tab(self, parent):
        self.frame_(parent)
        self.label("Mods List")
        self.scrollbar_
        self.listbox_()
        mods_path = os.path.join(self.current_dir, "mods")
        if os.path.exists(mods_path):
            for item in os.listdir(mods_path):
                self.listbox.insert(tk.END, item)
        else:
            self.listbox.insert(tk.END, "modsフォルダが見つかりませんでした")
        return self.frame
    
    def plugins_tab(self, parent):
        self.frame_(parent)
        self.label("Plugin List")
        self.scrollbar_
        self.listbox_()
        plugins_path = os.path.join(self.current_dir, "plugins")
        if os.path.exists(plugins_path):
            for item in os.listdir(plugins_path):
                self.listbox.insert(tk.END, item)
        else:
            self.listbox.insert(tk.END, "pluginsフォルダが見つかりませんでした")
        return self.frame
    
    def setting_tab(self, parent):
        self.frame_(parent)
        self.label("設定")
        
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
        
        self.config = self.load_config()
        self.entries = {}
        
        self.label("サーバーJARファイル:", layout_mode="place", x=50, y=60)
        self.jar_entry = tk.Entry(self.frame, bg=self.btn_color, fg=self.fg, font=("arial", 12), width=40)
        self.jar_entry.insert(0, self.config.get("server_jar", ""))
        self.jar_entry.place(x=250, y=60)
        self.entries["server_jar"] = self.jar_entry
        self.save_state = tk.BooleanVar(value=self.config.get("save_log", False))
        self.label("ログの自動保存", layout_mode="place", x=50, y=380)
        self.save_log = tk.Button(self.frame, text="OFF", bg=self.bg, fg=self.fg, font=("arial", 12), command=self.save_toggle, width=8)
        self.save_log.place(x=250, y=380)
        
        self.btn_(self.frame, "参照", command=self.select_jar, bg=self.btn_color, fg=self.fg, layout_mode="place", x=700, y=58, width=80, height=25)
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
        self.auto_sync()
        return self.frame
    
    def auto_sync(self):
        current = {}
        # セーブ
        try:
            current = {k: e.get() for k, e in self.entries.items()}
            #config save用
            current["save_log"] = self.save_state.get()
            
            
            latest_config = self.load_config()
            if "eula" in latest_config:
                current["eula"] = latest_config["eula"]
            self.save_config(current)
            
        except Exception as e:
            print("自動保存エラー:", e)
            #self.add_log(f"自動保存エラー:{e}")
        
        # リロード
        try:
            latest = self.load_config()
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
            #self.add_log(f"自動リロードエラー:{e}")
        
        
        #username = latest.get("username", "Unknown")  # ← グローバル変数として作る
        
        
        # 5秒ごとに繰り返す
        self.frame.after(500, self.auto_sync)
        
    def select_jar(self):
        path = filedialog.askopenfilename(title="サーバーの .jar ファイルを選んでね", filetypes=[("Java Archive", "*.jar"), ("すべてのファイル", "*.*")])
        if path:
            self.jar_entry.delete(0, tk.END)
            self.jar_entry.insert(0, path)
            print("選ばれたファイル:", path)
    
    def save_toggle(self):
        self.save_state.set(not self.save_state.get())
        self.save_log.config(text="ON" if self.save_state.get() else "OFF")
        self.config["save_log"] = self.save_state.get()
        self.save_config(self.config)
    
    def agree(self):
        try:
            with open("eula.txt", "w", encoding="utf-8") as file:
                file.write("#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://aka.ms/MinecraftEULA).\n")
                file.write("eula=true\n")
        
        except Exception as e:
            print("eula.txt 書き込みエラー:", e)
            #self.add_log(f"eula.txt 書き込みエラー:{e}")
    
    def load_config(self):
        if not os.path.exists(self.CONFIG_PATH):
            with open(self.CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(self.DEFAULT, f, indent=4, ensure_ascii=False)
            return self.DEFAULT
        try:
            with open(self.CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            #self.add_log(f"設定ファイル読み込みエラー:{e}")
            print("設定ファイル読み込みエラー:", e)
            return self.DEFAULT
    
    def save_config(self, data):
        try:
            with open(self.CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print("設定保存エラー:", e)
            #self.add_log(f"設定保存エラー:{e}")
    
    def frame_(self, parent):
        self.frame = tk.Frame(parent, bg=self.bg)
        self.frame.place(x=0, y=20, width=910, height=490)
    
    def label(self, text, bg=None, fg=None, layout_mode=None, x=None, y=None):
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
        
    def log_box_(self):
        self.log_box = tk.Text(self.frame, bg=self.bg, fg=self.fg, font=("Consolas", 10), state="disabled")
        self.log_box.place(x=0, y=30, width=900, height=400)
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
    
    def show_frame(self, frame):
        frame.tkraise()
    
    def on_enter(self, event=None):
        cmd = self.text_box.get().strip()
        if not cmd:
            return
        
        # log_boxにコマンドを色付きで表示
        self.log_box.config(state="normal")
        self.log_box.tag_config("command", foreground="#15FF00", font=("arial", 12), background=self.bg)  # コマンドの色を黄色に
        self.log_box.insert("end", f"<{self.username}> {cmd}\n", "command")
        self.log_box.see("end")
        self.log_box.config(state="disabled")
        if self.server and self.server.stdin:
            self.server.stdin.write(cmd + "\n")
            self.server.stdin.flush()
        else:
            self.log_box.insert("end", f"[WARN] サーバーが起動していません。\n", "command")
            self.log_box.see("end")
            self.log_box.config(state="disabled")
        
        #self.send_command(cmd)  # サーバーに送信
        self.text_box.delete(0, tk.END)  # 入力欄クリア
    
    def app(self):
        print("再起動します。")
        exe = sys.executable
        script = os.path.abspath(sys.argv[0])
        subprocess.Popen([exe, script])  # 新しいプロセスを起動
        os._exit(0)  # 今のGUIを終了
        return
    
    def config_reset(self):
        self.fix()
        self.app()
        return self.fix


win = tk.Tk()
function = function__()
function.gui()
function.frame_main.lift()
function.win.mainloop()
