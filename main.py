import tkinter as tk
from tkinter import colorchooser, messagebox, ttk
import subprocess
import os
import requests
import webbrowser
import threading
import time
import sys
import re

CONFIG_FILE = "player_config.lua"

# --- GUI главное окно ---
root = tk.Tk()
root.title("ROaLOX Launcher")
root.geometry("900x750")
root.configure(bg="black")

# --- Переменные tkinter (после root!) ---
nick_var = tk.StringVar(master=root, value="roaloxtest")
color_var = tk.StringVar(master=root, value="#ff00ff")
client_var = tk.StringVar(master=root, value="2010")

head_color = tk.StringVar(master=root, value="#ff0000")
body_color = tk.StringVar(master=root, value="#00ff00")
left_leg_color = tk.StringVar(master=root, value="#0000ff")
right_leg_color = tk.StringVar(master=root, value="#ffff00")
arms_color = tk.StringVar(master=root, value="#ff00ff")

# --- Работа с конфигом .lua ---
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            nick_match = re.search(r'nickname\s*=\s*"([^"]*)"', content)
            color_match = re.search(r'color\s*=\s*"([^"]*)"', content)
            client_match = re.search(r'client_version\s*=\s*"([^"]*)"', content)
            head_match = re.search(r'head_color\s*=\s*"([^"]*)"', content)
            body_match = re.search(r'body_color\s*=\s*"([^"]*)"', content)
            left_leg_match = re.search(r'left_leg_color\s*=\s*"([^"]*)"', content)
            right_leg_match = re.search(r'right_leg_color\s*=\s*"([^"]*)"', content)
            arms_match = re.search(r'arms_color\s*=\s*"([^"]*)"', content)

            nick_var.set(nick_match.group(1) if nick_match else "roaloxtest")
            color_var.set(color_match.group(1) if color_match else "#ff00ff")
            color_preview.config(bg=color_var.get())
            client_var.set(client_match.group(1) if client_match else "2010")

            head_color.set(head_match.group(1) if head_match else "#ff0000")
            body_color.set(body_match.group(1) if body_match else "#00ff00")
            left_leg_color.set(left_leg_match.group(1) if left_leg_match else "#0000ff")
            right_leg_color.set(right_leg_match.group(1) if right_leg_match else "#ffff00")
            arms_color.set(arms_match.group(1) if arms_match else "#ff00ff")
    else:
        color_preview.config(bg=color_var.get())

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

# --- UI утилиты ---
def choose_color(var, label):
    color_code = colorchooser.askcolor(title="Выбери цвет")[1]
    if color_code:
        var.set(color_code)
        label.config(bg=color_code)

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

def open_support():
    webbrowser.open("https://t.me/ROaLOXaccount")

# --- Обновление лаунчера ---
def update_file(url, save_path, logs, pb, progress, total_files):
    try:
        r = requests.get(url, stream=True, timeout=10)
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))
        downloaded = 0
        with open(save_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    percent_file = downloaded / total_size if total_size else 1
                    percent_total = (progress + percent_file) / total_files * 100
                    root.after(0, pb.config, {"value": percent_total})
        logs.append(f"[OK] {save_path} обновлён")
    except Exception as e:
        logs.append(f"[ERR] {save_path}: {e}")

def restart_launcher():
    python = sys.executable
    os.execl(python, python, *sys.argv)

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
            root.after(0, label.config, {"text": f"ROaLOX перезагрузится через {i} секунд"})
            time.sleep(1)
        restart_launcher()

    threading.Thread(target=auto_restart, daemon=True).start()

def update_all():
    logs = []
    base = "https://raw.githubusercontent.com/roalox/roaloxlauncher/refs/heads/main/"
    files_to_update = ["main.py", "script.lua", CONFIG_FILE]

    progress_win = tk.Toplevel(root)
    progress_win.title("Обновление...")
    progress_win.geometry("400x150")

    status_label = tk.Label(progress_win, text="Подготовка...", font=("Arial", 12))
    status_label.pack(pady=10)

    pb = ttk.Progressbar(progress_win, length=300, mode="determinate", maximum=100)
    pb.pack(pady=10)

    def do_update():
        total_files = len(files_to_update)
        for idx, file in enumerate(files_to_update):
            root.after(0, status_label.config, {"text": f"Загружается: {file}"})
            update_file(base + file, file, logs, pb, idx, total_files)
        root.after(0, progress_win.destroy)
        root.after(0, show_restart_window, logs)

    threading.Thread(target=do_update, daemon=True).start()

# --- UI Лаунчера ---
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
tk.Button(root, text="Выбрать цвет", command=lambda: choose_color(color_var, color_preview), font=("Arial", 12), width=15).pack(pady=5)
color_preview = tk.Label(root, bg=color_var.get(), width=20, height=1, relief="flat")
color_preview.pack(pady=5)

tk.Label(root, text="Цвет головы:", font=("Arial", 12), bg="#ffffff").pack(pady=5)
tk.Button(root, text="Выбрать", command=lambda: choose_color(head_color, head_preview), font=("Arial", 12), width=15).pack(pady=5)
head_preview = tk.Label(root, bg=head_color.get(), width=20, height=1, relief="flat")
head_preview.pack(pady=5)

tk.Label(root, text="Цвет тела:", font=("Arial", 12), bg="#ffffff").pack(pady=5)
tk.Button(root, text="Выбрать", command=lambda: choose_color(body_color, body_preview), font=("Arial", 12), width=15).pack(pady=5)
body_preview = tk.Label(root, bg=body_color.get(), width=20, height=1, relief="flat")
body_preview.pack(pady=5)

tk.Label(root, text="Цвет левой ноги:", font=("Arial", 12), bg="#ffffff").pack(pady=5)
tk.Button(root, text="Выбрать", command=lambda: choose_color(left_leg_color, left_leg_preview), font=("Arial", 12), width=15).pack(pady=5)
left_leg_preview = tk.Label(root, bg=left_leg_color.get(), width=20, height=1, relief="flat")
left_leg_preview.pack(pady=5)

tk.Label(root, text="Цвет правой ноги:", font=("Arial", 12), bg="#ffffff").pack(pady=5)
tk.Button(root, text="Выбрать", command=lambda: choose_color(right_leg_color, right_leg_preview), font=("Arial", 12), width=15).pack(pady=5)
right_leg_preview = tk.Label(root, bg=right_leg_color.get(), width=20, height=1, relief="flat")
right_leg_preview.pack(pady=5)

tk.Label(root, text="Цвет рук:", font=("Arial", 12), bg="#ffffff").pack(pady=5)
tk.Button(root, text="Выбрать", command=lambda: choose_color(arms_color, arms_preview), font=("Arial", 12), width=15).pack(pady=5)
arms_preview = tk.Label(root, bg=arms_color.get(), width=20, height=1, relief="flat")
arms_preview.pack(pady=5)

tk.Label(root, text="Выберите версию клиента:", font=("Arial", 12), bg="#ffffff").pack(pady=5)
client_options = ["2010", "2011"]
dropdown = tk.OptionMenu(root, client_var, *client_options)
dropdown.config(font=("Arial", 12), width=15)
dropdown.pack(pady=5)

tk.Button(root, text="ЗАПУСТИТЬ ROaLOX", command=run_game,
          bg="green", fg="white", font=("Arial", 14, "bold"), padx=10, pady=8).pack(pady=15)

load_config()
root.mainloop()
