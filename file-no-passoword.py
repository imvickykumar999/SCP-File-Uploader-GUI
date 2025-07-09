import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import tkinter as tk
from tkinter import filedialog
import paramiko
import os

# ------------------- Custom Dark Popup -------------------
def custom_popup(title, message, success=True):
    popup = tk.Toplevel(root)
    popup.title(title)
    popup.configure(bg="#1e1e1e")
    popup.geometry("420x160")
    popup.resizable(False, False)
    popup.grab_set()

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

# ------------------- PEM Key Select -------------------
def select_pem_key():
    filepath = filedialog.askopenfilename(filetypes=[("PEM Key", "*.pem")])
    if filepath:
        pem_key_var.set(filepath)

# ------------------- File Upload -------------------
def upload_file():
    filepath = file_path_var.get()
    server_ip = server_ip_var.get()
    username = username_var.get()
    pem_path = pem_key_var.get()
    remote_path = remote_path_var.get()

    if not filepath or not server_ip or not username or not pem_path or not remote_path:
        custom_popup("Error", "Please fill all fields.", success=False)
        return

    filename = os.path.basename(filepath)
    remote_full_path = remote_path.rstrip('/') + '/' + filename

    try:
        key = paramiko.RSAKey.from_private_key_file(pem_path)

        transport = paramiko.Transport((server_ip, 22))
        transport.connect(username=username, pkey=key)

        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(filepath, remote_full_path)
        sftp.close()
        transport.close()

        custom_popup("Success", f"File '{filename}' uploaded successfully!", success=True)

    except Exception as e:
        custom_popup("Upload Failed", f"{str(e)}", success=False)

# ------------------- Main Window -------------------
root = tk.Tk()
root.title("🚀 SCP File Uploader (Key-Based)")
root.geometry("750x400")
root.configure(bg="#1e1e1e")

# Form variables
file_path_var = tk.StringVar()
server_ip_var = tk.StringVar(value="34.139.46.232")
username_var = tk.StringVar(value="samadmin")
pem_key_var = tk.StringVar()
remote_path_var = tk.StringVar()

# UI styling
label_font = ("Segoe UI", 10, "bold")
entry_style = {
    "bg": "#2b2b2b",
    "fg": "white",
    "insertbackground": "white",
    "bd": 1,
    "relief": "flat",
    "highlightthickness": 1
}

# Layout
tk.Label(root, text="📂 Select Local File:", bg="#1e1e1e", fg="white", font=label_font).grid(row=0, column=0, padx=10, pady=10, sticky='w')
tk.Entry(root, textvariable=file_path_var, width=50, **entry_style).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_file, bg="#0078d4", fg="white").grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="🔗 Server IP:", bg="#1e1e1e", fg="white", font=label_font).grid(row=1, column=0, padx=10, pady=10, sticky='w')
tk.Entry(root, textvariable=server_ip_var, width=30, **entry_style).grid(row=1, column=1, padx=10, pady=10, sticky='w')

tk.Label(root, text="👤 Username:", bg="#1e1e1e", fg="white", font=label_font).grid(row=2, column=0, padx=10, pady=10, sticky='w')
tk.Entry(root, textvariable=username_var, width=30, **entry_style).grid(row=2, column=1, padx=10, pady=10, sticky='w')

tk.Label(root, text="🔑 PEM Key File:", bg="#1e1e1e", fg="white", font=label_font).grid(row=3, column=0, padx=10, pady=10, sticky='w')
tk.Entry(root, textvariable=pem_key_var, width=50, **entry_style).grid(row=3, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_pem_key, bg="#0078d4", fg="white").grid(row=3, column=2, padx=10, pady=10)

tk.Label(root, text="📁 Remote Folder Path:", bg="#1e1e1e", fg="white", font=label_font).grid(row=4, column=0, padx=10, pady=10, sticky='w')
tk.Entry(root, textvariable=remote_path_var, width=50, **entry_style).grid(row=4, column=1, padx=10, pady=10)

tk.Button(root, text="🚀 Upload File", command=upload_file, bg="green", fg="white", font=("Segoe UI", 11, "bold"), width=20).grid(row=5, column=1, pady=25)

root.mainloop()
