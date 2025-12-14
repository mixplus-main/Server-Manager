# ServerManager Extensions Framework

Hello! Thank you for reading this documentation.

This document explains the basic rules, structure, and main APIs  
used when creating extensions for **ServerManager**.

---

## Basic Naming Rules

- **Functions end with an underscore (`_`)**
  - Examples:
    - `btn_`
    - `add_log_`
    - `frame_`

- **Classes end with double underscores (`__`)**
  - Example:
    - `function__`

> Note:  
> Some internal helper functions may not strictly follow this rule,  
> but **public APIs for extensions do**.

---

## Important Rules for Extensions

When writing an extension, you **must** follow these rules:

- ❌ Do NOT create a new `tk.Tk()` window
- ❌ Do NOT call `mainloop()`
- ❌ Do NOT destroy the window
- ✅ Always use the existing manager instance

### Manager Instance

Extensions must use the global manager instance provided by ServerManager:

```python
import builtins
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ServerManager1_4_0 import function__

manager: "function__" = builtins.FUNC_INSTANCE
This instance already manages:

The main window (win)

All frames

Log boxes

Buttons

Server process state

⚠ Creating a new GUI root will cause crashes.

Main Functions (API Reference)
add_log_
Displays a message in a log box.

Usage:

python
コードをコピーする
add_log_("message", "color", "tab_name")
Arguments:

message (str): Text to display

color (str): Text color (e.g. "blue", "white")

tab_name (str): Log tab name (e.g. "main", "help")

frame_
Creates a new frame.

Usage:

python
コードをコピーする
frame_(parent)
Arguments:

parent: Parent widget (usually manager.win)

Note:

This function sets manager.frame

Usually used internally

label_
Creates a label inside the current frame.

Usage:

python
コードをコピーする
label_(
    "text",
    bg="background color",
    fg="font color",
    font=("arial", 12),
    layout_mode="pack",
    x=0,
    y=0
)
layout_mode options:

"pack" (default)

"place"

"grid"

log_box_
Creates a log box (tk.Text).

Usage:

python
コードをコピーする
log_box_()
log_boxes["tab_name"] = log_box
⚠ Important:
You must register the log box:

python
コードをコピーする
log_boxes["tab_name"] = log_box
If you forget this, add_log_ will not work for that tab.

scrollbar_
Creates and attaches a scrollbar to the current log box.

Usage:

python
コードをコピーする
scrollbar_()
listbox_
Creates a list box.

Usage:

python
コードをコピーする
listbox_(
    bg="background color",
    fg="font color",
    relief=None
)
btn_
Creates a button.

Usage:

python
コードをコピーする
btn_(
    parent,
    "text",
    command=function_to_execute,
    bg="background color",
    fg="font color",
    layout_mode=None,
    x=0,
    y=0,
    row=0,
    col=0
)
layout_mode behavior:

None or "pack" → pack()

"place" → uses x, y

"grid" → uses row, col

Minimal Extension Example
python
コードをコピーする
# Extensions/temp.py
import builtins
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ServerManager1_4_0 import function__

id = "temp"

manager: "function__" = builtins.FUNC_INSTANCE


def show_temp_frame():
    # Create a new frame
    manager.frame_(manager.win)
    manager.label_("Temp Frame")
    manager.log_box_()
    manager.scrollbar_()

    # Register log box
    manager.log_boxes["temp"] = manager.log_box

    # Show the frame
    manager.show_frame(manager.frame)

    # Output log message
    manager.add_log_("temp frame!", "blue", "temp")


# Add a button to the Main tab
manager.btn_(
    manager.frame_main,
    "Temp",
    command=show_temp_frame,
    bg=manager.btn_color,
    fg=manager.fg,
)
Summary
Extensions control the existing GUI

Do not create new windows

Always use builtins.FUNC_INSTANCE

Register log boxes before calling add_log_

Follow naming rules for consistency

This framework behaves like a lightweight plugin system.

Happy hacking 🚀
Edit by MixPlus
