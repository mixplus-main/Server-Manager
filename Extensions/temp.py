
import tkinter as tk
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ServerManager import AppContext, MAIN, GUI, Config, TAB

def apply(ctx: "AppContext"):
    t = Temp(ctx)

class Temp:
    def __init__(self, ctx: "AppContext"):
        self.main: "MAIN" = ctx.main
        self.gui: "GUI" = ctx.gui
        self.CFG: "Config" = ctx.cfg
        self.tab: "TAB" = ctx.tab
        
        Temp_frame = tk.Button(self.main.win, text="Temp", command=self.Temp_tab, bg=self.CFG.btn_color, fg=self.CFG.fg)
        Temp_frame.pack()
    
    def Temp_tab(self):
        if "frame_temp" not in self.tab.frames or not self.tab.frames["frame_temp"].winfo_exists():
            frame_temp = tk.Frame(self.main.win, bg=self.CFG.bg); frame_temp.place(x=0, y=20, width=910, height=490)
        
        
        temp_label = tk.Label(frame_temp, text="Temp", bg=self.CFG.bg, fg=self.CFG.fg, font=("arial", 12)); temp_label.pack()
        
        log_temp = tk.Text(
            frame_temp,
            bg=self.CFG.bg, fg=self.CFG.fg,
            font=("arial", 12), state="disabled"); log_temp.place(x=0, y=30, width=900, height=405)
        
        scroll = tk.Scrollbar(frame_temp, command=log_temp.yview); scroll.place(x=890, y=30, height=400)
        log_temp.config(yscrollcommand=scroll.set)
        
        
        #setting
        self.tab.frames.append(frame_temp)
        self.tab.labels.append(temp_label)
        self.tab.text.append(log_temp)
        self.tab.scrollbars.append(scroll)
        
        self.main.log_boxes['temp'] = log_temp
        for _ in range(100):
            self.main.add_log("Temp", "green", "temp")
        return frame_temp, temp_label
