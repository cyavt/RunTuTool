#################################
#### BY NGUYỄN VĂN TRÚC (CYA) ###
#################################
#python3.9
# >_& Linux: 23:57 09-2022
import sys
import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
import requests
from auto import main as run_auto_program

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")

def check_key():
    entered_key = key_entry.get()

    if entered_key in [item["Key"] for item in data.values()]:
        user_name = [item["Name"] for item in data.values() if item["Key"] == entered_key][0]
        show_success_message(user_name)
    else:
        messagebox.showerror("Lỗi", "Sai key rồi :((.")

def show_success_message(user_name):
    message = f"Chạy được rồi nè hihi!\nXin Chào: {user_name}"
    messagebox.showinfo("Thành công", message)
    app.destroy()
    run_auto_program()

def get_data_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Ooops, có lỗi xảy ra: {err}")
    except json.JSONDecodeError as json_err:
        print(f"Error decoding JSON: {json_err}")

data = get_data_from_url("https://cyavt.github.io/autoKey/key.json")

if getattr(sys, 'frozen', False):
    icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
else:
    icon_path = 'icon.ico'

app = tk.Tk()
app.title("Xác thực")
app.iconbitmap(icon_path)
app.geometry('400x200')

# Tạo và định dạng widget
label = tk.Label(app, text="Nhập key:", font=("Arial", 14))
label.pack(pady=10)

key_entry = tk.Entry(app, show="*", font=("Arial", 14))
key_entry.pack(pady=10)

check_button = tk.Button(app, text="Kiểm tra", command=check_key, font=("Arial", 13))
check_button.pack(pady=10)

app.update_idletasks()
width = app.winfo_width()
height = app.winfo_height()
center_window(app, width, height)

app.protocol("WM_DELETE_WINDOW", app.destroy)

app.mainloop()
