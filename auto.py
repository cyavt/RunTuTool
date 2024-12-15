#################################
#### BY NGUYỄN VĂN TRÚC (CYA) ###
#################################
#python3.9
# >_& Linux: 23:57 09-2022
import sys
import os
from bs4 import BeautifulSoup
import threading
import time
import tkinter as tk
import webbrowser
from tkinter import ttk, DISABLED, NORMAL, filedialog
from tkinter import font
from tkinter.ttk import Style
import requests

# getKey
response = requests.get('https://cyavt.github.io/autoKey/setting.json')

def main():
    if response.status_code == 200:
        json_data = response.json()
        IP = json_data["IP"]
        LOGIN_PATH = json_data["LOGIN_PATH"]
        CMT_PATH = json_data["CMT_PATH"]
        ADD_PATH = json_data["ADD_PATH"]
        RM_PATH = json_data["RM_PATH"]
        NAME = json_data["NAME"]
        NAME_MDK = json_data["NAME_MDK"]
        TimeOutLogin = json_data["TimeOutLogin"]
        TimeOutDK = json_data["TimeOutDK"]
    else:
        print(f"Failed to fetch JSON data. Status code: {response.status_code}")

    USERNAME = ''
    PASSWORD = ''

    login_data = ''
    http_IP = ''
    LOGIN_URL = ''
    CMT_URL = ''
    DATA_FILE = ''
    MDK = ''
    PATH = ''
    running = False

    def center_window(window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        window.geometry(f"{width}x{height}+{x}+{y}")

    def choose_file():
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)

    def clear_console():
        console_text.delete("1.0", tk.END)

    def xu_ly():
        global console_text, running, mmh_data, LOGIN_URL, CMT_URL, NAME, login_data, TimeOutLogin, TimeOutDK, DATA_FILE, MDK, PATH
        running = False
        time.sleep(3)
        console_text.config(state=NORMAL)
        clear_console()
        try:
            with open(DATA_FILE, 'r') as file:
                lines = [line.strip() for line in file.readlines()]
            mmh_data = {NAME: lines}
            print(MDK)
            if MDK is not None:
                mmh_data['mdk'] = MDK
            print(mmh_data)
            console_text.insert(tk.END, f"DỮ LIỆU MÔN HỌC: {mmh_data}\n")
        except FileNotFoundError:
            stop_xu_ly()
            print(f"File {DATA_FILE} not found.")
            console_text.insert(tk.END, f"File {DATA_FILE} không tồn tại.")
        except Exception as e:
            stop_xu_ly()
            print(f"An error occurred: {e}")
            console_text.insert(tk.END, f"An error occurred: {e}")

        while not running:
            with requests.Session() as session:
                session.cookies.clear()
                try:
                    # Perform login
                    post = session.post(LOGIN_URL, data=login_data, timeout=TimeOutLogin, allow_redirects=False)
                    post.raise_for_status()
                    post.encoding = 'utf-8'

                    # Check if login was successful
                    if post.status_code == 200:
                        html_content = post.text
                        soup = BeautifulSoup(html_content, 'html.parser')
                        main_middle_element = soup.find('td', class_='main-middle', id='pagemain')
                        welcome_text = main_middle_element.get_text(strip=True)
                        if 'Xin chào sinh viên' in welcome_text:
                            student_name = welcome_text.split("Xin chào sinh viên ")[1].split("Thực hiện bởi")[
                                0].strip()
                            console_text.insert(tk.END, f"\nĐã đăng nhập tài khoản: {student_name}")
                            console_text.see(tk.END)
                        else:
                            console_text.insert(tk.END, f"\nLỗi hiển thi tên sv")
                            console_text.see(tk.END)
                        time.sleep(0.5)

                        # Perform CMT
                        post_CMT = session.post(CMT_URL, data=mmh_data, timeout=TimeOutDK, allow_redirects=False)
                        post_CMT.encoding = 'utf-8'
                        if post_CMT.status_code == 200 and "Kết quả" in post_CMT.text:
                            if PATH == ADD_PATH:
                                if "Hết chỗ" in post_CMT.text:
                                    console_text.insert(tk.END, f"\nLỗi: Hết chỗ")
                                    console_text.see(tk.END)
                                else:
                                    console_text.insert(tk.END, f"\nĐã thêm môn học")
                                    console_text.see(tk.END)
                                    running = True
                            elif PATH == RM_PATH:
                                console_text.insert(tk.END, f"\nĐã xóa môn")
                                console_text.see(tk.END)
                                running = True
                            else:
                                print("\nĐK Môn học thành công")
                                console_text.insert(tk.END, f"\nChúc mừng bạn {student_name} đã đăng ký thành công !")
                                console_text.see(tk.END)
                                running = True
                        elif post_CMT.status_code == 302:
                            print("\nĐã đăng ký môn học")
                            console_text.insert(tk.END, f"\nLỗi: Bạn đã đăng ký hoặc sai mã | E: {post_CMT.status_code}")
                            console_text.see(tk.END)
                            time.sleep(2)
                        elif "Xin mời đăng nhập" in post_CMT.text:
                            print("\nLỗi: Đăng nhập thất bại")
                            console_text.insert(tk.END, f"\nLỗi: Đăng nhập thất bại | E: {post_CMT.status_code}")
                            console_text.see(tk.END)
                            time.sleep(2)
                        else:
                            console_text.insert(tk.END,
                                                f"\nLỗi không xác định, vui lòng liên hệ CYA | E: {post_CMT.status_code}")
                            console_text.see(tk.END)
                            time.sleep(2)
                        # cookie = session.cookies.get_dict()
                        # print("Cookie:", cookie)
                    else:
                        print(f"\nLogin failed with status code: {post.status_code}")
                        console_text.insert(tk.END, f"\nSai tài khoản hoặc mật khẩu: {post.status_code}")
                        console_text.see(tk.END)
                        time.sleep(2)

                except requests.exceptions.RequestException as e:
                    print(f"Error: {e}")
                    console_text.insert(tk.END, f"\nTrang web đang quá tải, đang thử lại...")
                    console_text.see(tk.END)
                    time.sleep(2)
        console_text.insert(tk.END, f"\n------------------------------------\nĐã Dừng....")
        console_text.see(tk.END)
        console_text.config(state=DISABLED)
        submit_button.config(state="normal")
        submit_button.config(text="CHẠY TỰ ĐỘNG")

    def start_auto():
        global running
        running = True
        submit_button.config(state="disabled")
        submit_button.config(text="Đang chạy...")
        auto_thread = threading.Thread(target=xu_ly)
        auto_thread.start()

    def stop_xu_ly():
        global running
        running = True
        submit_button.config(state="normal")
        submit_button.config(text="RUN AUTO")

    def VariableConsole():
        global SetRun, console_text, LOGIN_URL, CMT_URL, login_data, NAME, TimeOutLogin, TimeOutDK, DATA_FILE
        if SetRun:
            # Hiển thị thông báo trong console
            console_text.insert(tk.END, f"Thông Tin\n")
            console_text.insert(tk.END, f"URL LOGIN: {LOGIN_URL}\n")
            console_text.insert(tk.END, f"URL ĐK: {CMT_URL}\n")
            console_text.insert(tk.END, f"Login Data: {login_data}\n")
            console_text.insert(tk.END, f"Name: {NAME}\n")
            console_text.insert(tk.END, f"Time Out Login: {TimeOutLogin} | Time Out ĐK: {TimeOutDK}\n")
            console_text.insert(tk.END, f"File Path: {DATA_FILE}\n")
            console_text.insert(tk.END, f"------------------------------------\n")
            console_text.insert(tk.END, f"VUI LÒNG KIÊN TRÌ CHỜ ĐỢI ĐỂ BẮT ĐẦU CHẠY....\n")
            start_auto()
        else:
            console_text.insert(tk.END, f"Không được để trống các ô nhập\n")
            console_text.config(state=DISABLED)
            console_text.insert(tk.END, f"------------------------------------\n")

    def runDK():
        global SetRun, IP, LOGIN_PATH, PATH, NAME, TimeOutLogin, TimeOutDK, USERNAME, PASSWORD, login_data, http_IP, LOGIN_URL, CMT_URL, DATA_FILE, MDK, console_text, entry_mdk

        console_text.config(state=NORMAL)
        clear_console()
        # Get the values from the entry widgets
        IP = entry_ip.get()
        LOGIN_PATH = entry_loginPath.get()
        PATH = entry_cmtPath.get()
        NAME = entry_name.get()
        TimeOutLogin = int(entry_timeOutLogin.get())
        TimeOutDK = int(entry_timeOutDK.get())

        USERNAME = entry_username.get()
        PASSWORD = entry_password.get()
        DATA_FILE = entry_file_path.get()
        MDK = entry_mdk.get() if entry_mdk and hasattr(entry_mdk, 'get') else None
        # print(entry_mdk)
        # print(MDK)
        login_data = {"maSV": [USERNAME], "pw": [PASSWORD]}
        http_IP = f'http://{IP}:80/'
        LOGIN_URL = http_IP + LOGIN_PATH
        CMT_URL = http_IP + PATH

        if not all([IP, LOGIN_PATH, PATH, NAME, TimeOutLogin, TimeOutDK, USERNAME, PASSWORD, DATA_FILE]) or (MDK is not None and MDK == ''):
            SetRun = False
        else:
            SetRun = True
        # Disable console
        VariableConsole()

    # class UpdateEntryMdk:
    #     def __init__(self):
    #         self.entry_mdk = "initial_value"
    #
    # update_mdk_object = UpdateEntryMdk()
    def Main_display():
        global console_text, submit_button, stop_button, entry_file_path, entry_username, entry_password, entry_timeOutDK, entry_timeOutLogin, entry_name, entry_cmtPath, entry_loginPath, entry_ip, selected_option, app, entry_mdk

        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
        else:
            icon_path = 'icon.ico'

        # Create the main window
        app = tk.Tk()
        app.title("Auto TC")
        app.iconbitmap(icon_path)
        # app.option_add("*Font", ("Inconsolata", 10, "bold"))

        # app.geometry('0+10+10')
        # Control the window size
        app.resizable(width=False, height=False)

        # ------------ Display 1 ------------
        s = Style()
        s.configure('My1.TFrame', background='gray', relief='sunken', borderwidth=5)
        frame1 = ttk.Frame(app, padding=10)
        frame1.grid(row=0, column=0, columnspan=3, rowspan=1, sticky="we")
        frame1.config(style='My1.TFrame')  # Đổi màu nền
        frame1.grid_rowconfigure(0, weight=1)
        frame1.grid_columnconfigure(0, weight=1)
        frame1.config(width=300)
        frame1.config(height=50)
        frame1.grid_propagate(True)

        # create a label widget
        label_tieude = ttk.Label(frame1, text="TOOL AUTO - DKTC", font=("Inconsolata", 13, "bold"),
                                 foreground="white", background="gray", anchor="center")
        label_tieude.grid(row=0, column=0, sticky="we")

        label_thongbao = ttk.Label(frame1,
                                   text="Tool có chỉ chức năng hỗ trợ chạy tự động như nhập tay, mọi vấn đề ảnh hưởng đến việc ĐKTC, tác giả không chịu trách nhiệm\nLưu ý: Các tùy chỉnh mặc định đã chỉnh cho phù hợp, vui lòng không thay đổi !",
                                   font=("Inconsolata", 10, "italic"), foreground="white", background="gray",
                                   anchor="center",
                                   justify="center", wraplength=700)
        label_thongbao.grid(row=1, column=0, sticky="we")

        link_label = tk.Label(frame1, text="CODE BY CYA", font=("Inconsolata", 10, "italic"), foreground="blue",
                              anchor="center", justify="center", cursor="hand2", relief="flat", borderwidth=0,
                              background="gray")
        link_label.grid(row=2, column=0, sticky="se")
        link_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://www.facebook.com/cya57"))

        # ------------ Display 2 ------------
        s = Style()
        s.configure('My2.TFrame', relief='sunken', padding=(20, 15), borderwidth=0)
        frame2 = ttk.Frame(app, padding=10)
        frame2.grid(row=1, column=0, columnspan=4, rowspan=1, sticky="we")
        frame2.config(style='My2.TFrame')

        def show_entry():
            global entry_mdk
            print(selected_option.get())
            if selected_option.get() == "ADD" or selected_option.get() == "RM":
                label_mdk = ttk.Label(frame2, text="Nhập mã đăng ký:", font=("Inconsolata", 10, "bold"))
                label_mdk.grid(row=0, column=3, padx=0, pady=5)
                if entry_mdk is None:
                    entry_mdk = ttk.Entry(frame2)
                    entry_mdk.grid(row=0, column=4, padx=0, pady=5)
                if selected_option.get() == "ADD":
                    selected_option.set("ADD")
                    entry_cmtPath.delete(0, tk.END)
                    entry_cmtPath.insert(0, ADD_PATH)
                elif selected_option.get() == "RM":
                    selected_option.set("RM")
                    entry_cmtPath.delete(0, tk.END)
                    entry_cmtPath.insert(0, RM_PATH)
                entry_name.delete(0, tk.END)
                entry_name.insert(0, NAME_MDK)
            else:
                entry_cmtPath.delete(0, tk.END)
                entry_cmtPath.insert(0, CMT_PATH)
                entry_name.delete(0, tk.END)
                entry_name.insert(0, NAME)
                # If neither checkbox is selected, remove the label and entry widget
                for widget in frame2.grid_slaves():
                    if widget.grid_info()["column"] == 3:
                        widget.grid_forget()
                    elif widget.grid_info()["column"] == 4:
                        widget.grid_forget()
                entry_mdk = None

        selected_option = tk.StringVar()
        selected_option.set("DK")
        radiobutton1 = tk.Radiobutton(frame2, text="Đăng ký môn", variable=selected_option, value="DK",
                                      font=("Inconsolata", 10, "bold"), command=show_entry)
        radiobutton1.grid(row=0, column=0, columnspan=1, pady=10, padx=10, sticky="w")

        radiobutton2 = tk.Radiobutton(frame2, text="Thêm môn", variable=selected_option, value="ADD",
                                      font=("Inconsolata", 10, "bold"), command=show_entry)
        radiobutton2.grid(row=0, column=1, columnspan=1, pady=10, padx=10, sticky="w")

        radiobutton3 = tk.Radiobutton(frame2, text="Xóa môn", variable=selected_option, value="RM",
                                      font=("Inconsolata", 10, "bold"), command=show_entry)
        radiobutton3.grid(row=0, column=2, columnspan=1, pady=10, padx=10, sticky="w")

        # ------------ Display 3 ------------
        custom_font = font.Font(family="Inconsolata", size=11)
        cell_width = 30
        s = Style()
        s.configure('My3.TFrame', relief='sunken', padding=(20, 15), borderwidth=0, width=200, height=50)
        frame3 = ttk.Frame(app, padding=10)
        frame3.grid(row=2, column=0, columnspan=3, rowspan=11, sticky="we")
        frame3.config(style='My3.TFrame')
        frame3.grid_propagate(True)

        # IP
        label_ip = ttk.Label(frame3, text="IP:", font=custom_font)
        label_ip.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry_ip = ttk.Entry(frame3, show="*", width=cell_width)
        entry_ip.configure(font=custom_font)
        entry_ip.insert(0, IP)
        entry_ip.grid(row=0, column=1, padx=5, pady=5)

        # URL LOGIN
        label_loginPath = ttk.Label(frame3, text="LOGIN PATH:", font=custom_font)
        label_loginPath.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        entry_loginPath = ttk.Entry(frame3, show="*", width=cell_width)
        entry_loginPath.configure(font=custom_font)
        entry_loginPath.insert(0, LOGIN_PATH)
        entry_loginPath.grid(row=1, column=1, padx=5, pady=5)

        # URL ĐK
        label_cmtPath = ttk.Label(frame3, text="COMMIT PATH:", font=custom_font)
        label_cmtPath.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        entry_cmtPath = ttk.Entry(frame3, show="*", width=cell_width)
        entry_cmtPath.configure(font=custom_font)
        entry_cmtPath.insert(0, CMT_PATH)
        entry_cmtPath.grid(row=2, column=1, padx=5, pady=5)

        # NAME KEY
        label_name = ttk.Label(frame3, text="KEY NAME:", font=custom_font)
        label_name.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        entry_name = ttk.Entry(frame3, show="*", width=cell_width)
        entry_name.configure(font=custom_font)
        entry_name.insert(0, NAME)
        entry_name.grid(row=3, column=1, padx=5, pady=5)

        # TimeOut Login
        label_timeOutLogin = ttk.Label(frame3, text="TIMEOUT LOGIN:", font=custom_font)
        label_timeOutLogin.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        entry_timeOutLogin = ttk.Entry(frame3, width=cell_width)
        entry_timeOutLogin.configure(font=custom_font)
        entry_timeOutLogin.insert(0, str(TimeOutLogin))
        entry_timeOutLogin.grid(row=4, column=1, padx=5, pady=5)

        # TimeOut While
        label_timeOutDK = ttk.Label(frame3, text="TIMEOUT RUN:", font=custom_font)
        label_timeOutDK.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        entry_timeOutDK = ttk.Entry(frame3, width=cell_width)
        entry_timeOutDK.configure(font=custom_font)
        entry_timeOutDK.insert(0, str(TimeOutDK))
        entry_timeOutDK.grid(row=5, column=1, padx=5, pady=5)

        # USERNAME
        label_username = ttk.Label(frame3, text="Mã SV:", font=custom_font, foreground="red")
        label_username.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        entry_username = ttk.Entry(frame3, width=cell_width)
        entry_username.configure(font=custom_font)
        entry_username.grid(row=6, column=1, padx=5, pady=5)

        # PASSWORD
        label_password = ttk.Label(frame3, text="Mật khẩu:", font=custom_font, foreground="red")
        label_password.grid(row=7, column=0, padx=5, pady=5, sticky="w")
        entry_password = ttk.Entry(frame3, show="*", width=cell_width)
        entry_password.configure(font=custom_font)
        entry_password.grid(row=7, column=1, padx=5, pady=5)

        # FILE DATA
        label_file_path = ttk.Label(frame3, text="File mã môn học (*.txt):", font=custom_font, foreground="red")
        label_file_path.grid(row=8, column=0, padx=5, pady=5, sticky="w")
        entry_file_path = ttk.Entry(frame3, width=20)
        entry_file_path.configure(font=custom_font)
        entry_file_path.grid(row=8, column=1, padx=5, pady=5, sticky="w")
        button_choose_file = ttk.Button(frame3, text="Chọn file", command=choose_file)
        button_choose_file.grid(row=8, column=1, padx=5, pady=5, sticky="e")

        # ------------ BUTTON ------------
        farm_button = ttk.Frame(frame3)
        farm_button.grid(row=9, column=1, columnspan=2, rowspan=1, sticky="we")
        farm_button.grid_rowconfigure(0, weight=10)
        farm_button.grid_columnconfigure(0, weight=1)
        farm_button.config(width=200)
        farm_button.config(height=50)
        farm_button.grid_propagate(True)

        # START
        submit_button = tk.Button(farm_button, text="RUN AUTO", command=runDK, state=tk.NORMAL,
                                  background="#00d4b7", foreground="#2e3152", font=("Inconsolata", 10, "bold"),
                                  width=10)
        submit_button.grid(row=0, column=0, pady=10, padx=10, stick="ew")

        # STOP
        stop_button = tk.Button(farm_button, text="STOP", command=stop_xu_ly, background="#bd3500", foreground="white",
                                font=("Inconsolata", 10, "bold"))
        stop_button.grid(row=0, column=1, pady=10, padx=10, stick="ew")

        # CONSOLE
        console_text = tk.Text(frame3, height=20, width=50, wrap=tk.WORD, state=tk.DISABLED, foreground="white",
                               background="#2e3152")
        console_text.grid(row=0, column=3, rowspan=9, padx=10, pady=10)

        show_entry()

        return app, console_text, submit_button, stop_button, entry_file_path, entry_username, entry_password, entry_timeOutDK, entry_timeOutLogin, entry_name, entry_cmtPath, entry_loginPath, entry_ip, entry_mdk, selected_option

    # Run the main program
    app, console_text, submit_button, stop_button, entry_file_path, entry_username, entry_password, entry_timeOutDK, entry_timeOutLogin, entry_name, entry_cmtPath, entry_loginPath, entry_ip, entry_mdk, selected_option = Main_display()
    # Center the window
    app.update_idletasks()
    width = app.winfo_width()
    height = app.winfo_height()
    center_window(app, width, height)

    app.protocol("WM_DELETE_WINDOW", app.destroy)
    app.mainloop()

if __name__ == "__main__":
    main()
