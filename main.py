import tkinter as tk
from tkinter import colorchooser
import json
import subprocess
import os
import requests

# --- Функции лаунчера ---

def load_config():
    """Загрузка конфига с GitHub или локально"""
    config_url = "https://raw.githubusercontent.com/roalox/roaloxlauncher/refs/heads/main/player_config.json"
    try:
        response = requests.get(config_url)
        response.raise_for_status()
        cfg = response.json()
        nick_var.set(cfg.get("nickname", "ZZZ"))
        color_var.set(cfg.get("color", "#ff00ff"))
        color_preview.config(bg=color_var.get())
        client_var.set(cfg.get("client_version", "2010"))
        print("Конфиг загружен с GitHub!")
    except requests.RequestException:
        print("Не удалось загрузить конфиг с GitHub, пробуем локальный...")
        if os.path.exists("player_config.json"):
            with open("player_config.json", "r") as f:
                try:
                    cfg = json.load(f)
                    nick_var.set(cfg.get("nickname", "roalox977412"))
                    color_var.set(cfg.get("color", "#ff00ff"))
                    color_preview.config(bg=color_var.get())
                    client_var.set(cfg.get("client_version", "2010"))
                except json.JSONDecodeError:
                    pass

def choose_color():
    color_code = colorchooser.askcolor(title="Выбери цвет")[1]
    if color_code:
        color_var.set(color_code)
        color_preview.config(bg=color_code)

def update_file(url, save_path):
    try:
        r = requests.get(url)
        r.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(r.content)
        print(f"{save_path} обновлён!")
    except Exception as e:
        print(f"Ошибка при обновлении {save_path}: {e}")

def update_client():
    print("Обновление клиента...")
    update_file("https://raw.githubusercontent.com/roalox/roaloxlauncher/refs/heads/main/script.lua", "script.lua")
    update_file("https://raw.githubusercontent.com/roalox/roaloxlauncher/refs/heads/main/player_config.json", "player_config.json")
    print("Клиент обновлён!")

def update_launcher():
    print("Обновление лаунчера...")
    update_file("https://raw.githubusercontent.com/roalox/roaloxlauncher/refs/heads/main/main.py", "main.py")
    print("Лаунчер обновлён!")

def run_game():
    config = {
        "nickname": nick_var.get(),
        "color": color_var.get(),
        "client_version": client_var.get()
    }
    with open("player_config.json", "w") as f:
        json.dump(config, f)
    
    game_exe = r"C:\Path\to\ROaLOX.exe"
    lua_script = r"C:\Path\to\script.lua"
    
    if not os.path.exists(game_exe):
        print("Ошибка: игра не найдена!")
        return
    if not os.path.exists(lua_script):
        print("Ошибка: lua скрипт не найден!")
        return

    subprocess.Popen([game_exe, lua_script])

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

# виджеты
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

# кнопки
tk.Button(root, text="Обновить клиент", command=update_client,
          bg="blue", fg="white", font=("Arial", 14, "bold"), padx=10, pady=8).pack(pady=15)
tk.Button(root, text="Обновить лаунчер", command=update_launcher,
          bg="purple", fg="white", font=("Arial", 14, "bold"), padx=10, pady=8).pack(pady=5)
tk.Button(root, text="ЗАПУСТИТЬ ROaLOX", command=run_game,
          bg="green", fg="white", font=("Arial", 14, "bold"), padx=10, pady=8).pack(pady=15)

load_config()
root.mainloop()
