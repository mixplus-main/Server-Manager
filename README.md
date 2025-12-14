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
