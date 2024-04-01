import tkinter as tk
from tkinter import ttk
import math
from tkinter import messagebox

# Global variables
current_input = ""
memory = 0
ans = None
history = []

def handle_error():
    entry.delete(0, tk.END)
    entry.insert(tk.END, "Error")

def button_click(event):
    global current_input, ans

    button_text = event.widget.cget("text")

    if button_text == "=":
        try:
            result = eval(current_input)
            entry.delete(0, tk.END)
            entry.insert(tk.END, result)
            ans = result
            add_to_history(current_input, result)
        except ZeroDivisionError:
            handle_error()
            entry.insert(tk.END, "Division by Zero")
        except Exception as e:
            handle_error()
            entry.insert(tk.END, str(e))
        current_input = ""
    elif button_text == "C":
        entry.delete(0, tk.END)
        current_input = ""
    elif button_text == "CE":
        entry.delete(0, tk.END)
    elif button_text == "M+":
        try:
            global memory
            memory += float(entry.get())
            current_input = ""
        except Exception as e:
            handle_error()
    elif button_text == "MR":
        entry.delete(0, tk.END)
        entry.insert(tk.END, memory) # type: ignore
        current_input = ""
    elif button_text == "ANS":
        if ans is not None:
            current_input += str(ans)
            entry.insert(tk.END, str(ans))
    elif button_text == "⌫":
        current_input = current_input[:-1]
        entry.delete(0, tk.END)
        entry.insert(tk.END, current_input)
    else:
        current_input += button_text
        entry.insert(tk.END, button_text)

def add_to_history(calculation, result):
    history.append((calculation, result))
    update_history_panel()

def clear_history():
    global history
    history = []
    update_history_panel()

def update_history_panel():
    history_text.config(state=tk.NORMAL)
    history_text.delete(1.0, tk.END)
    for i, (calculation, result) in enumerate(history, start=1):
        history_text.insert(tk.END, f"{i}. {calculation} = {result}\n")
    history_text.config(state=tk.DISABLED)

def on_key(event):
    key = event.char
    if key in "0123456789.+-*/()":
        button_click(tk.Event(widget=None, char=key)) # type: ignore

def clear_memory():
    global memory
    memory = 0

def store_memory():
    global memory
    try:
        memory = float(entry.get())
    except Exception as e:
        handle_error()

def scientific_button_click(event):
    button_text = event.widget.cget("text")

    if button_text in ["sin", "cos", "tan", "ln", "log", "sqrt"]:
        try:
            value = float(entry.get())
            if button_text == "sin":
                result = math.sin(math.radians(value))
            elif button_text == "cos":
                result = math.cos(math.radians(value))
            elif button_text == "tan":
                result = math.tan(math.radians(value))
            elif button_text == "ln":
                result = math.log(value)
            elif button_text == "log":
                result = math.log10(value)
            elif button_text == "sqrt":
                result = math.sqrt(value)
            entry.delete(0, tk.END)
            entry.insert(tk.END, result) # type: ignore
        except Exception as e:
            handle_error()

def show_user_guide():
    user_guide_text = """
    User Guide

    Calculator:
    - Enter numbers and perform basic operations (+, -, *, /).
    - Press '=' to calculate the result.
    - 'C' clears the input field, 'CE' clears the last entry.
    - 'M+' adds the current result to memory.
    - 'MR' recalls the value from memory.
    - 'ANS' inserts the previous result.
    - '⌫' deletes the last character.

    Scientific Functions:
    - Additional functions: sin, cos, tan, ln, log, sqrt.
    - Enter the number, then click the function button.

    History:
    - The history panel shows previous calculations.
    - 'Clear History' removes the history.

    Memory:
    - 'M+' adds the result to memory.
    - 'MR' recalls the value from memory.
    - 'MC' clears the memory.

    Keyboard Shortcuts:
    - Use the keyboard for input and calculations.

    Enjoy using the calculator!
    """
    messagebox.showinfo("User Guide", user_guide_text)

def show_about_page():
    about_text = """
    Scientific Calculator

    Version 2.0

    Created by Anmol Yaseen

    This calculator application was developed as a versatile tool for basic and scientific calculations. It includes a user guide and an about page to help you get started.

    Features:
    - Basic calculator operations (+, -, *, /).
    - Scientific functions (sin, cos, tan, ln, log, sqrt).
    - Memory functions (M+, MR, MC).
    - Keyboard input support.
    - History panel to track previous calculations.

    Thank you for using our calculator!
    """
    messagebox.showinfo("About Calculator", about_text)

# Create the main window
root = tk.Tk()
root.title("Calculator")

# Create a styled theme for ttk buttons
style = ttk.Style()
style.configure("TButton", padding=10, font=('Helvetica', 14))

# Create the entry field with improved styling
entry = tk.Entry(root, width=20, font=('Helvetica', 24))
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, ipadx=10, ipady=10, sticky="nsew")

# Create frames for calculator buttons
button_frame = ttk.Frame(root)
button_frame.grid(row=1, column=0, columnspan=4)

# Define button labels for the calculator
button_labels = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '=', '+',
    'C', 'CE', 'M+', 'MR', '⌫',
    'sin', 'cos', 'tan', 'ln', 'log', 'sqrt',
]

# Create and arrange calculator ttk buttons
row_val = 1
col_val = 0
buttons = []

for label in button_labels:
    button = ttk.Button(button_frame, text=label)
    button.grid(row=row_val, column=col_val, padx=5, pady=5, sticky="nsew")
    button.bind("<Button-1>", button_click)
    if label in ["sin", "cos", "tan", "ln", "log", "sqrt"]:
        button.bind("<Button-1>", scientific_button_click)
    buttons.append(button)

    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

# Create a history panel
history_panel = ttk.LabelFrame(root, text="History")
history_panel.grid(row=1, column=4, rowspan=6, padx=10, pady=10, sticky="nsew")

history_text = tk.Text(history_panel, height=10, width=30, wrap=tk.WORD)
history_text.pack(fill=tk.BOTH, expand=True)
history_text.config(state=tk.DISABLED)

# Create a clear history button
clear_history_button = ttk.Button(history_panel, text="Clear History", command=clear_history)
clear_history_button.pack()

# Bind keyboard events
root.bind("<Key>", on_key)

# Add a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create a File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=root.quit)

# Create a Memory menu
memory_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Memory", menu=memory_menu)
memory_menu.add_command(label="M+", command=store_memory)
memory_menu.add_command(label="MR", command=lambda: entry.insert(tk.END, memory)) # type: ignore
memory_menu.add_command(label="MC", command=clear_memory)

# Create a Help menu
help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="User Guide", command=show_user_guide)
help_menu.add_command(label="About", command=show_about_page)

root.mainloop()
