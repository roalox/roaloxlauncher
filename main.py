import tkinter as tk
from tkinter import ttk, colorchooser
import threading
import time
import random
from PIL import Image, ImageTk
import os

# --- переменные ---
nick_var = tk.StringVar(value="roaloxtest")
client_var = tk.StringVar(value="2010")

head_color = tk.StringVar(value="#ff0000")
body_color = tk.StringVar(value="#00ff00")
left_leg_color = tk.StringVar(value="#0000ff")
right_leg_color = tk.StringVar(value="#ffff00")
arms_color = tk.StringVar(value="#ff00ff")

preview_labels = []

# --- файлы для "загрузки" локально (имитация) ---
local_files = ["main.py", "script.lua", "player_config.lua", "logo.png", "assets/"]

# --- главный корень ---
root = tk.Tk()
root.title("ROaLOX Launcher")
root.geometry("900x750")

# --- Фреймы ---
loading_frame = tk.Frame(root)
main_frame = tk.Frame(root)

loading_frame.place(relx=0.5, rely=0.5, anchor="center")
main_frame.place(relx=0.5, rely=0.5, anchor="center")
main_frame.lower()  # спрятать меню

# --- лого ---
try:
    logo_img = Image.open("logo.png")
except:
    logo_img = Image.new("RGBA", (200, 200), (255, 0, 0, 255))  # красный квадрат демо

logo_size = 200
logo_label = tk.Label(loading_frame)
logo_label.pack(pady=20)

# прогрессбар и статус
pb = ttk.Progressbar(loading_frame, orient="horizontal", length=600, mode="determinate")
pb.pack(pady=10)
status_label = tk.Label(loading_frame, text="Загрузка...", font=("Arial", 16))
status_label.pack(pady=5)

def animate_logo():
    global logo_size
    while getattr(threading.current_thread(), "running", True):
        for delta in range(20):
            logo_size += 1
            update_logo()
            time.sleep(0.02)
        for delta in range(20):
            logo_size -= 1
            update_logo()
            time.sleep(0.02)

def update_logo():
    img_resized = logo_img.resize((logo_size, logo_size), Image.ANTIALIAS)
    tk_img = ImageTk.PhotoImage(img_resized)
    logo_label.config(image=tk_img)
    logo_label.image = tk_img

def load_files_sequence():
    total = len(local_files)
    for i, file in enumerate(local_files, 1):
        status_label.config(text=f"Загрузка {file} ({i}/{total})")
        pb["value"] = (i-1)/total*100
        # имитация загрузки локального файла
        time.sleep(random.uniform(0.5, 1.2))
    pb["value"] = 100
    time.sleep(0.3)
    show_main_menu()

def show_main_menu():
    loading_frame.lower()
    main_frame.lift()
    build_main_ui()

# --- Основное меню ---
def choose_color(var, preview):
    color_code = colorchooser.askcolor(title="Выбери цвет")[1]
    if color_code:
        var.set(color_code)
        preview.config(bg=color_code)

def random_greeting():
    greeting_templates = [
        "Привет, {}!",
        "Готов к эпичным приключениям, {}?",
        "{} — ROaLOX ждёт тебя!",
        "Новая сессия начинается, {}!",
        "Зови друзей и вперёд, {}!"
    ]
    text = random.choice(greeting_templates).format(nick_var.get())
    label_greet.config(text=text)
    root.after(30000, random_greeting)

def randomize_colors():
    for var, preview in zip([head_color, body_color, left_leg_color, right_leg_color, arms_color],
                            preview_labels):
        rand_color = "#%06x" % random.randint(0, 0xFFFFFF)
        var.set(rand_color)
        preview.config(bg=rand_color)

def build_main_ui():
    global label_greet, preview_labels
    label_greet = tk.Label(main_frame, text="", font=("Arial", 24, "bold"), fg="purple")
    label_greet.pack(pady=20)
    random_greeting()

    tk.Label(main_frame, text="Ник персонажа:", font=("Arial", 16)).pack(pady=5)
    tk.Entry(main_frame, textvariable=nick_var, font=("Arial", 16), width=25).pack(pady=5)

    tk.Label(main_frame, text="Версия клиента:", font=("Arial", 16)).pack(pady=5)
    tk.Entry(main_frame, textvariable=client_var, font=("Arial", 16), width=10).pack(pady=5)

    # кастомизация цветов
    parts = [
        ("Голова", head_color),
        ("Тело", body_color),
        ("Левая нога", left_leg_color),
        ("Правая нога", right_leg_color),
        ("Руки", arms_color)
    ]
    preview_labels = []
    for name, var in parts:
        frame = tk.Frame(main_frame)
        frame.pack(pady=5)
        tk.Label(frame, text=name+":", font=("Arial", 14)).pack(side="left", padx=5)
        preview = tk.Label(frame, bg=var.get(), width=5, height=1, relief="sunken")
        preview.pack(side="left", padx=5)
        preview_labels.append(preview)
        tk.Button(frame, text="Выбрать цвет", font=("Arial", 12),
                  command=lambda v=var, p=preview: choose_color(v, p)).pack(side="left", padx=5)

    tk.Button(main_frame, text="🎨 Случайные цвета", font=("Arial", 14, "bold"),
              bg="blue", fg="white", command=randomize_colors).pack(pady=10)

    tk.Button(main_frame, text="▶ Запустить ROaLOX", font=("Arial", 14, "bold"),
              bg="green", fg="white", command=lambda: print("🚀 Запуск игры...")).pack(pady=10)

# --- запуск анимации и загрузки ---
logo_thread = threading.Thread(target=animate_logo, daemon=True)
logo_thread.running = True
logo_thread.start()

load_thread = threading.Thread(target=load_files_sequence, daemon=True)
load_thread.start()

root.mainloop()
