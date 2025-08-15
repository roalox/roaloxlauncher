import tkinter as tk
from tkinter import ttk, colorchooser
from PIL import Image, ImageTk
import threading, time, os, subprocess, re, webbrowser

CONFIG_FILE = "player_config.lua"

# --- переменные ---
nick_var = tk.StringVar(value="roaloxtest")
color_var = tk.StringVar(value="#ff00ff")
client_var = tk.StringVar(value="2010")

head_color = tk.StringVar(value="#ff0000")
body_color = tk.StringVar(value="#00ff00")
left_leg_color = tk.StringVar(value="#0000ff")
right_leg_color = tk.StringVar(value="#ffff00")
arms_color = tk.StringVar(value="#ff00ff")

# --- GUI ---
root = tk.Tk()
root.title("ROaLOX Launcher")
root.geometry("900x750")
root.configure(bg="black")

# --- загрузка конфига .lua ---
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            nick_match = re.search(r'nickname\s*=\s*"([^"]*)"', content)
            color_match = re.search(r'color\s*=\s*"([^"]*)"', content)
            client_match = re.search(r'client_version\s*=\s*"([^"]*)"', content)
            nick_var.set(nick_match.group(1) if nick_match else "roaloxtest")
            color_var.set(color_match.group(1) if color_match else "#ff00ff")
            client_var.set(client_match.group(1) if client_match else "2010")
    else:
        nick_var.set("roaloxtest")
        color_var.set("#ff00ff")
        client_var.set("2010")

def save_config():
    lua_content = f'''nickname = "{nick_var.get()}"
color = "{color_var.get()}"
client_version = "{client_var.get()}"
head_color = "{head_color.get()}"
body_color = "{body_color.get()}"
left_leg_color = "{left_leg_color.get()}"
right_leg_color = "{right_leg_color.get()}"
arms_color = "{arms_color.get()}"
'''
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write(lua_content)

# --- утилиты ---
def choose_color(var, preview=None):
    color_code = colorchooser.askcolor(title="Выбери цвет")[1]
    if color_code:
        var.set(color_code)
        if preview:
            preview.config(bg=color_code)

def run_game():
    save_config()
    game_exe = r"C:\Path\to\ROaLOX.exe"
    lua_script = r"C:\Path\to\script.lua"
    if os.path.exists(game_exe) and os.path.exists(lua_script):
        subprocess.Popen([game_exe, lua_script])
    else:
        tk.messagebox.showerror("Ошибка", "Игра или lua скрипт не найдены!")

def open_support():
    webbrowser.open("https://t.me/ROaLOXaccount")

# --- фрейм загрузки с логотипом ---
load_frame = tk.Frame(root, bg="black")
load_frame.place(relwidth=1, relheight=1)
logo_path = "logo.png"
if os.path.exists(logo_path):
    img = Image.open(logo_path).resize((200, 200))
    logo_img = ImageTk.PhotoImage(img)
    logo_label = tk.Label(load_frame, image=logo_img, bg="black")
    logo_label.pack(expand=True)
progress = ttk.Progressbar(load_frame, length=400, mode="determinate")
progress.pack(pady=20)

def fake_load():
    steps = ["Загрузка файлов лаунчера...", "Инициализация GUI...", "Применение конфигурации...", "Финализация..."]
    for i, step in enumerate(steps):
        progress["value"] = (i+1)/len(steps)*100
        root.update_idletasks()
        logo_label.config(width=200 + i*5, height=200 + i*5)
        time.sleep(0.7)
    load_frame.destroy()
    build_main_menu()

def build_main_menu():
    # главный интерфейс
    tk.Label(root, text=f"Привет, {nick_var.get()}!", font=("Arial", 20, "bold")).pack(pady=10)
    tk.Label(root, text="Ник персонажа:").pack()
    tk.Entry(root, textvariable=nick_var).pack()
    tk.Label(root, text="Цвет персонажа:").pack()
    color_btn = tk.Button(root, text="Выбрать цвет", command=lambda: choose_color(color_var, color_preview))
    color_btn.pack()
    color_preview = tk.Label(root, bg=color_var.get(), width=20, height=1)
    color_preview.pack()
    tk.Label(root, text="Выберите версию клиента:").pack()
    tk.OptionMenu(root, client_var, "2010", "2011").pack()
    tk.Button(root, text="ЗАПУСТИТЬ ROaLOX", command=run_game, bg="green", fg="white").pack(pady=10)

# --- запуск ---
load_config()
threading.Thread(target=fake_load, daemon=True).start()
root.mainloop()
