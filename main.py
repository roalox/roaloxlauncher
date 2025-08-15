import tkinter as tk
from tkinter import colorchooser, messagebox
import subprocess
import os
import requests
import webbrowser
import threading
import time
import sys
import re

CONFIG_FILE = "player_config.lua"

# --- Работа с конфигом в формате .lua ---

def load_config():
    """Загрузка конфигурации из .lua"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            nick_match = re.search(r'nickname\s*=\s*"([^"]*)"', content)
            color_match = re.search(r'color\s*=\s*"([^"]*)"', content)
            client_match = re.search(r'client_version\s*=\s*"([^"]*)"', content)

            nick_var.set(nick_match.group(1) if nick_match else "roalox86401")
            color_var.set(color_match.group(1) if color_match else "#ff00ff")
            color_preview.config(bg=color_var.get())
            client_var.set(client_match.group(1) if client_match else "2010")
    else:
        nick_var.set("roalox77293")
        color_var.set("#ff00ff")
        client_var.set("2010")
        color_preview.config(bg=color_var.get())

def save_config():
    """Сохранение конфигурации в .lua"""
    lua_content = f'''nickname = "{nick_var.get()}"
color = "{color_var.get()}"
client_version = "{client_var.get()}"
'''
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write(lua_content)

# --- UI утилиты ---

def choose_color():
    color_code = colorchooser.askcolor(title="Выбери цвет")[1]
    if color_code:
        color_var.set(color_code)
        color_preview.config(bg=color_code)

def run_game():
    save_config()
    
    game_exe = r"C:\Path\to\ROaLOX.exe"
    lua_script = r"C:\Path\to\script.lua"
    
    if not os.path.exists(game_exe):
        print("Ошибка: игра не найдена!")
        return
    if not os.path.exists(lua_script):
        print("Ошибка: lua скрипт не найден!")
        return

    subprocess.Popen([game_exe, lua_script])

# --- Обновление лаунчера ---

def update_file(url, save_path, logs):
    try:
        r = requests.get(url)
        r.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(r.content)
        logs.append(f"[OK] {save_path} обновлён")
    except Exception as e:
        logs.append(f"[ERR] {save_path}: {e}")

def restart_launcher():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def open_support():
    webbrowser.open("https://t.me/ROaLOXaccount")

def show_restart_window(logs):
    win = tk.Toplevel(root)
    win.title("Обновление завершено")
    win.geometry("500x400")

    text = tk.Text(win, wrap="word", height=15)
    text.pack(fill="both", expand=True, padx=10, pady=10)
    text.insert("end", "\n".join(logs))
    text.config(state="disabled")

    label = tk.Label(win, text="ROaLOX перезагрузится через 5 секунд", font=("Arial", 12))
    label.pack(pady=5)

    btn_frame = tk.Frame(win)
    btn_frame.pack(side="bottom", fill="x", pady=10, padx=10)

    def abort():
        win.destroy()

    def restart_now():
        restart_launcher()

    if any("[ERR]" in log for log in logs):
        tk.Button(btn_frame, text="Всё равно перезагрузить", command=restart_now, bg="green", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Написать в поддержку", command=open_support, bg="blue", fg="white").pack(side="left", padx=5)
    else:
        tk.Button(btn_frame, text="Перезагрузить сейчас", command=restart_now, bg="green", fg="white").pack(side="left", padx=5)

    tk.Button(btn_frame, text="Аборт", command=abort, bg="red", fg="white").pack(side="right", padx=5)

    def auto_restart():
        for i in range(5, 0, -1):
            label.config(text=f"ROaLOX перезагрузится через {i} секунд")
            time.sleep(1)
        restart_launcher()

    threading.Thread(target=auto_restart, daemon=True).start()

def update_all():
    logs = []
    print("=== Обновление файлов с GitHub ===")
    base = "https://raw.githubusercontent.com/roalox/roaloxlauncher/refs/heads/main/"
    files_to_update = ["main.py", "script.lua", CONFIG_FILE]
    for file in files_to_update:
        update_file(base + file, file, logs)
    print("✅ Обновление завершено")
    show_restart_window(logs)

# --- GUI лаунчера ---
root = tk.Tk()
root.title("ROaLOX Launcher")
root.geometry("800x650")

nick_var = tk.StringVar()
color_var = tk.StringVar()
client_var = tk.StringVar()

# фон
if os.path.exists("fon.png"):
    bg_image = tk.PhotoImage(file="fon.png")
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

update_btn = tk.Button(root, text="🔄 Обновить", command=update_all,
                       bg="orange", fg="white", font=("Arial", 10, "bold"))
update_btn.place(relx=1.0, x=-10, y=10, anchor="ne")

tk.Label(root, text="ROaLOX Launcher", font=("Arial", 20, "bold"), bg="#ffffff").pack(pady=15)

tk.Label(root, text="Ник персонажа:", font=("Arial", 12), bg="#ffffff").pack(pady=5)
tk.Entry(root, textvariable=nick_var, font=("Arial", 12), width=20).pack(pady=5)

tk.Label(root, text="Цвет персонажа:", font=("Arial", 12), bg="#ffffff").pack(pady=5)
tk.Button(root, text="Выбрать цвет", command=choose_color, font=("Arial", 12), width=15).pack(pady=5)
color_preview = tk.Label(root, bg="#ff00ff", width=20, height=1, relief="flat")
color_preview.pack(pady=5)

tk.Label(root, text="Выберите версию клиента:", font=("Arial", 12), bg="#ffffff").pack(pady=5)
client_options = ["2010", "2011"]
dropdown = tk.OptionMenu(root, client_var, *client_options)
dropdown.config(font=("Arial", 12), width=15)
dropdown.pack(pady=5)

tk.Button(root, text="ЗАПУСТИТЬ ROaLOX", command=run_game,
          bg="green", fg="white", font=("Arial", 14, "bold"), padx=10, pady=8).pack(pady=15)

load_config()
root.mainloop()

