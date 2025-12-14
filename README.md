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
- ✅ Always use the existing manager instance:

```python
builtins.FUNC_INSTANCE
