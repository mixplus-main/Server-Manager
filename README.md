
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

Example:

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ServerManager1_4_0 import AppContext

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


[Templates](https://github.com/mixplus-main/Server-Manager/blob/main/Extensions/temp.py)
## Summary

- Extensions control the existing GUI
- Extensions receive access via AppContext
- No global state is allowed
- Log boxes must be registered before logging
- All APIs are instance-based and IDE-friendly

This framework is designed as a lightweight, safe plugin system.

Edit by MixPlus

### Others
If you want to add buttons, labels, or other widgets, please create them using the standard tkinter API.

