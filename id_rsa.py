import tkinter as tk
from tkinter import filedialog
import paramiko
import os
from stat import S_ISDIR
from tkinter import ttk  # For progress bar

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
    filepath = filedialog.askopenfilename(title="Select File", filetypes=[("All Files", "*.*")])
    if filepath:
        file_path_var.set(filepath)

# ------------------- PEM Key Select -------------------
def select_pem_key():
    filepath = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    if filepath:
        pem_key_var.set(filepath)

# ------------------- File Upload with Progress -------------------
def upload_file():
    filepath = file_path_var.get()
    server_ip = server_ip_var.get()
    username = username_var.get()
    pem_path = pem_key_var.get()
    remote_path = remote_path_var.get()

    if not filepath or not server_ip or not username or not pem_path or not remote_path:
        custom_popup("Error", "Please fill all fields.", success=False)
        return

    # Disable the Upload File button to prevent multiple uploads
    upload_button.config(state="disabled")

    filename = os.path.basename(filepath)
    remote_full_path = remote_path.rstrip('/') + '/' + filename

    try:
        key = paramiko.RSAKey.from_private_key_file(pem_path)

        transport = paramiko.Transport((server_ip, 22))
        transport.connect(username=username, pkey=key)

        sftp = paramiko.SFTPClient.from_transport(transport)

        # Create a new popup window for the progress bar
        progress_popup = tk.Toplevel(root)
        progress_popup.title("Uploading File")
        progress_popup.geometry("400x200")
        progress_popup.configure(bg="#1e1e1e")

        tk.Label(progress_popup, text="Uploading file... Please wait.", font=("Segoe UI", 12, "bold"), fg="white", bg="#1e1e1e").pack(pady=10)

        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(progress_popup, length=300, mode='determinate', variable=progress_var)
        progress_bar.pack(pady=20)
        
        # Function to update progress
        def progress_callback(transferred, total):
            progress = (transferred / total) * 100
            progress_var.set(progress)
            progress_popup.update_idletasks()

        # Upload the file with progress tracking
        sftp.put(filepath, remote_full_path, callback=progress_callback)

        sftp.close()
        transport.close()

        # Hide progress popup and show success message
        progress_popup.destroy()
        custom_popup("Success", f"File '{filename}' uploaded successfully!", success=True)

    except Exception as e:
        custom_popup("Upload Failed", f"{str(e)}", success=False)
    finally:
        # Re-enable the Upload File button
        upload_button.config(state="normal")

# ------------------- Remote Folder Navigation -------------------
def browse_remote_folder(remote_path="/"):
    server_ip = server_ip_var.get()
    username = username_var.get()
    pem_path = pem_key_var.get()

    if not server_ip or not username or not pem_path:
        custom_popup("Error", "Please fill in the server connection details first.", success=False)
        return

    # Create the folder window dynamically when browsing (only once)
    if 'folder_window' not in globals():
        global folder_window
        folder_window = tk.Toplevel(root)
        folder_window.title("Select Remote Folder")
        folder_window.geometry("400x300")
        folder_window.configure(bg="#1e1e1e")

    try:
        key = paramiko.RSAKey.from_private_key_file(pem_path)

        transport = paramiko.Transport((server_ip, 22))
        transport.connect(username=username, pkey=key)

        sftp = paramiko.SFTPClient.from_transport(transport)

        remote_items = sftp.listdir_attr(remote_path)

        # Clear existing folder list before showing new one
        for widget in folder_window.winfo_children():
            widget.destroy()

        tk.Label(folder_window, text=f"Select Remote Folder\n({remote_path})", font=("Segoe UI", 12, "bold"), fg="white", bg="#1e1e1e").pack(pady=10)

        if not remote_items:
            tk.Label(folder_window, text="No folders found", font=("Segoe UI", 12), fg="white", bg="#1e1e1e").pack(pady=10)

        for item in remote_items:
            if S_ISDIR(item.st_mode):  # Only show directories
                button = tk.Button(folder_window, text=f"📂 {item.filename}", command=lambda item=item: update_path_and_browse(remote_path + '/' + item.filename))
                button.pack(fill='x', padx=20, pady=5)

        sftp.close()
        transport.close()

    except Exception as e:
        custom_popup("Error", f"Failed to connect or retrieve directories: {str(e)}", success=False)

# ------------------- Update Path and Browse -------------------
def update_path_and_browse(path):
    remote_path_var.set(path)
    browse_remote_folder(path)

# ------------------- Set Remote Path -------------------
def set_remote_path(path):
    remote_path_var.set(path)

# ------------------- Main Window -------------------
root = tk.Tk()
root.title("🚀 SCP File Uploader (Key-Based)")
root.geometry("750x400")
root.configure(bg="#1e1e1e")

# Form variables
file_path_var = tk.StringVar()
server_ip_var = tk.StringVar(value="64.227.134.57")  # Default IP address
username_var = tk.StringVar(value="root")  # Default username for root access
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

# Remote folder selection with a browse button
tk.Label(root, text="📁 Remote Folder Path:", bg="#1e1e1e", fg="white", font=label_font).grid(row=4, column=0, padx=10, pady=10, sticky='w')
tk.Entry(root, textvariable=remote_path_var, width=50, **entry_style).grid(row=4, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=lambda: browse_remote_folder(remote_path_var.get() or "/"), bg="#0078d4", fg="white").grid(row=4, column=2, padx=10, pady=10)

# Upload File button
upload_button = tk.Button(root, text="🚀 Upload File", command=upload_file, bg="green", fg="white", font=("Segoe UI", 11, "bold"), width=20)
upload_button.grid(row=5, column=1, pady=25)

root.mainloop()
