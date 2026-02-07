
# Server Manager

**Version:** 1_5_101

**Edit by:** MixPlus

  本体の自動アップデート検討中

---

  


## Overview

This tool is a GUI for easily managing your Minecraft server.

Starting and stopping the server, backing it up, managing mods and plugins, customizing settings, and more can all be done from a single app.

The GUI is built with Tkinter, and extensions are also available.

  

---

  
## Main Features

- **Server Operation**

- Start/Stop Server

- Send Server Console Commands

- RAM and Slot Configuration

- **Log Management**

- Display Console Output in GUI

- Command History Management (Maximum History Configurable)

- **Settings Management**

- Change Username, Background Color, Text Color, and Button Color

- Save/Reset Settings

- Persistence Using config.json

- **Mod/Plugin Management**

- List the Contents of the server/mods and server/plugins Folders

- Direct Viewing from the List

- **Backup**

- Back Up the Entire Server Directory with the Backup Button

- **Extensions**

- Load Extensions by Simply Placing a `.py` File in the `Extensions` Folder

- Add Functionality to Extension Modules by Implementing the `apply(context)` Function
  

---

  

## Required environment

- Python 3.10 or higher

- Java (to run the Minecraft server)

- Compatible with Windows, macOS, and Linux (audio warnings are only available on Windows)

  

---

  

## How to use

  

### boot

```bash
Run exe or .py (python required for py)

```

  


### Starting and Stopping the Server

Use the GUI button command:

- `start server` → Start the server

- `stop server` → Stop the server

  

### Console Commands

You can enter commands directly into the console input field.

-  `/say Supports Minecraft commands such as message`

-  `clip` → View command history

-  `ver` / `version` → ServerManager version display (incomplete)

-  `clear` → Clear the log and command history

-  `config` → Check and change settings

-  `config view` → Display current settings

-  `config reset` → Reset settings

-  `config set <key> <value> <type>` → Change settings

-  `config remove <key>` → Delete settings

  


### Settings Changes

- The "Settings" tab in the GUI allows you to adjust RAM, number of slots, color, username, and more (currently not reflected on load).

- The "More Settings" tab also allows you to adjust command history and perform backup operations.

- Manage your extensions in the "Extensions" tab

  

---

  

## Directory structure

```

ServerManager/

├─ main.py # Main script

├─ server/ # Minecraft server file storage

│ ├─ mods/

│ └─ plugins/

├─ backup/ # Backup destination

├─ Extensions/ # Extensions

├─ config.json # Configuration file

└─ icon.ico # (Optional) Icon

```

  

---

  

## How to distribute and run


  

### Convert to exe (Windows)

```bash

pyinstaller  --onefile  main.py

pyinstaller  --onefile  --noconsole  main.py

pyinstaller  --onefile  --icon=icon.ico  main.py

```

  

---



# ServerManager Extensions Framework

Hello! Thank you for reading this documentation.

This document explains the rules, structure, and public APIs
used when creating extensions for ServerManager.

---

## Important Rules for Extensions

When writing an extension, you must follow these rules:

- Do NOT create a new tk.Tk() window
- Do NOT call mainloop()
- Do NOT destroy the main window
- Do NOT access global state (e.g. builtins)
- Always use the provided context object

ServerManager already manages:

- The main window
- All frames and tabs
- Log boxes
- Buttons
- Server state

Creating or controlling your own root window will cause crashes.

---

## Extension Entry Point

Each extension must expose an apply(ctx) function.

ServerManager will call this function and pass a context object
that provides controlled access to internal systems.
[Templates](#minimal-extension-example)

Example:

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ServerManager import AppContext

def apply(ctx: "AppContext"):
    ...

---

## AppContext

AppContext is the only object an extension should depend on.

It provides access to the core systems managed by ServerManager.

Available attributes:

- ctx.main
  window, event handlers, logging system

- ctx.gui
  UI helper methods (frame, label, button, etc.)

- ctx.config
  colors, paths, configuration values

- ctx.tab
  tab and frame management

Extensions must not instantiate these classes directly.

---

## Manager / GUI API Reference

All UI-related functions are instance methods accessed through
objects provided by AppContext.

---

### add_log

Displays a message in a log box.

Usage:
ctx.main.add_log("message", "color", "tab_name")

- message: text to display
- color: text color (e.g. blue, white)
- tab_name: log tab name (e.g. main, help)

A log box must be registered before using this function.

---


## Minimal Extension Example



[Templates GitHub](https://github.com/mixplus-main/Server-Manager/blob/main/Extensions/temp.py)
## Summary

- Extensions control the existing GUI
- Extensions receive access via AppContext
- No global state is allowed
-Log boxes must be registered before logging
- All APIs are instance-based and IDE-friendly

This framework is designed as a lightweight, safe plugin system.

Edit by MixPlus

### Others
If you want to add buttons, labels, or other widgets, please create them using the standard tkinter API.



---

  


## Contributors / Credits

- MixPlus (Developer)

- OpenAI ChatGPT (Idea)

- Microsoft Copilot (Idea)

This tool is still incomplete, but we plan to continue updating it.
