# ServerManager Extensions Framework

Hello! Thank you for reading this documentation.

This document explains the basic rules, structure, and main APIs  
used when creating extensions for **ServerManager**.

---

## Basic Naming Rules


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

```python
import builtins
from ServerManager1_4_0 import function__

manager: "function__" = builtins.FUNC_INSTANCE
```

This instance already manages:

- The main window (`win`)
- All frames
- Log boxes
- Buttons
- Server state

Creating a new GUI root will cause crashes.

---

## Main Functions (API Reference)

### add_log_

Displays a message in a log box.

```python
add_log_("message", "color", "tab_name")
```

- **message** (str): Text to display  
- **color** (str): Text color (e.g. `"blue"`, `"white"`)  
- **tab_name** (str): Log tab name (e.g. `"main"`, `"help"`)  

---

### frame_

Creates a new frame.

```python
frame_(parent)
```

- **parent**: Parent widget (usually `manager.win`)

> Note:  
> This function sets `manager.frame` internally.

---

### label_

Creates a label inside the current frame.

```python
label_(
    "text",
    bg="background color",
    fg="font color",
    font=("arial", 12),
    layout_mode="pack",
    x=0,
    y=0
)
```

Layout modes:

- `"pack"` (default)
- `"place"`
- `"grid"`

---

### log_box_

Creates a log box (`tk.Text`).

```python
log_box_()
manager.log_boxes["tab_name"] = manager.log_box
```

> Important:  
> You **must** register the log box before using `add_log_`.

---

### scrollbar_

Creates and attaches a scrollbar.

```python
scrollbar_()
```

---

### listbox_

Creates a list box.

```python
listbox_(
    bg="background color",
    fg="font color",
    relief=None
)
```

---

### btn_

Creates a button.

```python
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
```

Layout behavior:

- `None` or `"pack"` → `pack()`
- `"place"` → uses `x`, `y`
- `"grid"` → uses `row`, `col`

---

## Minimal Extension Example

```python
# Extensions/temp.py
import builtins

from ServerManager1_4_0 import function__

id = "temp"

manager: "function__" = builtins.FUNC_INSTANCE


def show_temp_frame():
    manager.frame_(manager.win)
    manager.label_("Temp Frame")
    manager.log_box_()
    manager.scrollbar_()

    manager.log_boxes["temp"] = manager.log_box
    manager.show_frame(manager.frame)
    manager.add_log_("temp frame!", "blue", "temp")


manager.btn_(
    manager.frame_main,
    "Temp",
    command=show_temp_frame,
    bg=manager.btn_color,
    fg=manager.fg,
)
```

---

## Summary

- Extensions control the existing GUI — they do not create one
- Always use `builtins.FUNC_INSTANCE`
- Register log boxes before using `add_log_`
- Follow naming rules for consistency

This framework is designed as a lightweight plugin system.

Edit by MixPlus
