import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import tkinter as tk
from tkinter import filedialog
import subprocess
import paramiko
import os

# ------------------- Custom Dark Popup -------------------
def custom_popup(title, message, success=True):
    popup = tk.Toplevel(root)
    popup.title(title)
    popup.configure(bg="#1e1e1e")
    popup.geometry("420x160")
    popup.resizable(False, False)
    popup.grab_set()  # Focus lock

    icon = "✅" if success else "❌"
    color = "#00cc66" if success else "#ff4444"

    tk.Label(
        popup,
        text=f"{icon} {message}",
        font=("Segoe UI", 11, "bold"),
        bg="#1e1e1e",
        fg=color,
        wraplength=360,
        justify="center",
        padx=20,
        pady=20
    ).pack()

    tk.Button(
        popup,
        text="OK",
        command=popup.destroy,
        bg="#444444",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        padx=12,
        pady=4
    ).pack(pady=10)

# ------------------- File Select -------------------
def select_file():
    filepath = filedialog.askopenfilename()
    if filepath:
        file_path_var.set(filepath)

# ------------------- Remote Folder Select -------------------
def select_remote_folder():
    server_ip = server_ip_var.get()
    username = username_var.get()
    password = password_var.get()

    if not server_ip or not username or not password:
        custom_popup("Error", "Please fill Server IP, Username and Password first!", success=False)
        return

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server_ip, username=username, password=password)

        stdin, stdout, stderr = ssh.exec_command('find ~ -type d')
        folders = stdout.read().decode().splitlines()
        ssh.close()

        folder_window = tk.Toplevel(root, bg="#1e1e1e")
        folder_window.title("📁 Select Destination Folder")
        folder_window.geometry("650x450")

        tk.Label(folder_window, text="📂 Choose a destination folder:", bg="#1e1e1e", fg="white", font=("Segoe UI", 11, "bold")).pack(pady=8)

        list_frame = tk.Frame(folder_window, bg="#1e1e1e")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        folder_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=("Consolas", 11),
                                    height=15, width=80, bg="#2b2b2b", fg="white",
                                    selectbackground="#444444", selectforeground="white", bd=0)
        for folder in folders:
            folder_listbox.insert(tk.END, f"📁 {folder}")
        folder_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=folder_listbox.yview)

        button_frame = tk.Frame(folder_window, bg="#1e1e1e")
        button_frame.pack(pady=12)

        select_btn = tk.Button(button_frame, text="✅ Select Folder", state="disabled", bg="#0078d4", fg="white", font=("Segoe UI", 10, "bold"), padx=10)
        select_btn.pack()

        def on_select(event):
            select_btn.config(state="normal")

        def select_folder():
            selection = folder_listbox.curselection()
            if not selection:
                custom_popup("Warning", "Please select a folder before clicking Select.", success=False)
                return
            selected = folder_listbox.get(selection)
            selected_path = selected.replace("📁 ", "")
            remote_path_var.set(selected_path)
            folder_window.destroy()

        folder_listbox.bind("<<ListboxSelect>>", on_select)
        select_btn.config(command=select_folder)

    except Exception as e:
        custom_popup("Connection Error", str(e), success=False)

# ------------------- File Upload -------------------
def upload_file():
    filepath = file_path_var.get()
    server_ip = server_ip_var.get()
    username = username_var.get()
    password = password_var.get()
    remote_path = remote_path_var.get()

    if not filepath or not server_ip or not username or not password or not remote_path:
        custom_popup("Error", "Please fill all fields.", success=False)
        return

    filename = os.path.basename(filepath)
    remote_full_path = remote_path if remote_path.endswith('/') else remote_path + '/'

    try:
        scp_command = ['scp', filepath, f"{username}@{server_ip}:{remote_full_path}"]
        try:
            subprocess.run(['sshpass', '-V'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            scp_command = ['sshpass', '-p', password] + scp_command
            subprocess.run(scp_command, check=True)
            custom_popup("Success", f"File '{filename}' uploaded successfully!", success=True)
        except subprocess.CalledProcessError:
            custom_popup("Error", "sshpass not installed. Run:\n\nsudo apt install sshpass", success=False)
    except Exception as e:
        custom_popup("Upload Failed", f"{str(e)}", success=False)

# ------------------- Main Window -------------------
root = tk.Tk()
root.title("🚀 SCP File Uploader")
root.geometry("750x400")
root.configure(bg="#1e1e1e")

# Form variables
file_path_var = tk.StringVar()
server_ip_var = tk.StringVar(value="103.206.13.152")
username_var = tk.StringVar(value="devlop")
password_var = tk.StringVar()
remote_path_var = tk.StringVar()

# UI styling
label_font = ("Segoe UI", 10, "bold")
entry_style = {"bg": "#2b2b2b", "fg": "white", "insertbackground": "white", "bd": 1, "relief": "flat", "highlightthickness": 1}

# Layout
tk.Label(root, text="📂 Select Local File:", bg="#1e1e1e", fg="white", font=label_font).grid(row=0, column=0, padx=10, pady=10, sticky='w')
tk.Entry(root, textvariable=file_path_var, width=50, **entry_style).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_file, bg="#0078d4", fg="white").grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="🔗 Server IP:", bg="#1e1e1e", fg="white", font=label_font).grid(row=1, column=0, padx=10, pady=10, sticky='w')
tk.Entry(root, textvariable=server_ip_var, width=30, **entry_style).grid(row=1, column=1, padx=10, pady=10, sticky='w')

tk.Label(root, text="👤 Username:", bg="#1e1e1e", fg="white", font=label_font).grid(row=2, column=0, padx=10, pady=10, sticky='w')
tk.Entry(root, textvariable=username_var, width=30, **entry_style).grid(row=2, column=1, padx=10, pady=10, sticky='w')

tk.Label(root, text="🔐 Password:", bg="#1e1e1e", fg="white", font=label_font).grid(row=3, column=0, padx=10, pady=10, sticky='w')
tk.Entry(root, textvariable=password_var, width=30, show="*", **entry_style).grid(row=3, column=1, padx=10, pady=10, sticky='w')

tk.Label(root, text="📁 Remote Folder:", bg="#1e1e1e", fg="white", font=label_font).grid(row=4, column=0, padx=10, pady=10, sticky='w')
tk.Entry(root, textvariable=remote_path_var, width=50, **entry_style).grid(row=4, column=1, padx=10, pady=10)
tk.Button(root, text="Choose", command=select_remote_folder, bg="#444444", fg="white").grid(row=4, column=2, padx=10, pady=10)

tk.Button(root, text="🚀 Upload File", command=upload_file, bg="green", fg="white", font=("Segoe UI", 11, "bold"), width=20).grid(row=5, column=1, pady=25)

root.mainloop()

