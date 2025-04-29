# `SCP File Uploader GUI`

![image](https://github.com/user-attachments/assets/a6208261-32fb-43dd-9e84-976bfe1ef6e1)

A modern, dark-themed SCP File Uploader GUI built with Python Tkinter and Paramiko. Transfer files easily to remote Linux servers with a stylish, easy-to-use interface.

---

**Complete Linux-compatible, dark-themed SCP File Uploader GUI**, including:

✅ Dark theme  
✅ Custom black-and-white popup (replacing `messagebox`)  
✅ Pre-filled username and server IP  
✅ Folder selector with icons  
✅ Fully self-contained GUI

---

## ✅ How to Run:

1. Save this as `main.py`
2. Ensure you have:
   ```bash
   pip install paramiko
   sudo apt install sshpass
   ```
3. Run it:
   ```bash
   python3 main.py
   ```

---

# 🎯 Steps to Turn Your Termux into a Server (LAN)


## ✅ 1. Install Termux (if not done)

If you don't have it yet, **install Termux** from:
- [F-Droid version (recommended)](https://f-droid.org/packages/com.termux/) (because Play Store version is outdated)

---

## ✅ 2. Update Termux Packages

First thing:
```bash
pkg update
pkg upgrade
```

Always **update** to avoid compatibility issues.

---

## ✅ 3. Install an SSH Server (or Other Servers)

Install **OpenSSH** server:
```bash
pkg install openssh
```

OpenSSH lets your Termux device **act as a small Linux server** inside your LAN.

---

## ✅ 4. Set a Password for Termux

If you don’t have a password set (Termux default is no password), run:

```bash
passwd
```

👉 This will set a password for your Termux user.

---

## ✅ 5. Start SSH Server

Now, start your SSH server:

```bash
sshd
```

This runs an **SSH server** on port `8022` by default (not 22, because Android blocks port 22).

---

## ✅ 6. Find Your Android's IP Address

Find out your **local IP address** (LAN IP):

```bash
ip addr show wlan0
```

Look for something like:
```
inet 192.168.1.50/24
```
✅ This `192.168.1.50` is your Termux server IP inside your Wi-Fi LAN.

---

## ✅ 7. Connect to Your Termux Server from Laptop or PC

From another device (Linux/Windows):
```bash
ssh -p 8022 username@192.168.1.50
```

(Username is usually `u0_a<number>` — you can check by typing `whoami` inside Termux.)

Or if you installed **file servers** (optional), you can access via:

- **SCP** for file transfers
- **SFTP** for file browsing
- **HTTP server** for web

---

# ⚡ Quick Recap of Commands:

```bash
pkg update
pkg upgrade
pkg install openssh
passwd
sshd
ip addr show wlan0
```
Then connect via:
```bash
ssh -p 8022 your_username@your_device_ip
```

---

# 🛠️ Pro Tip: (Optional)
You can also install:

| Server Type | Command |
|:---|:---|
| HTTP Server (simple web server) | `pkg install python` then `python3 -m http.server 8080` |
| FTP Server (for file transfer) | `pkg install ftpd` |
| PHP Server | `pkg install php` |

---

# 🚀 Important Things to Remember

| Topic | Important Note |
|---|---|
| Port | SSH on Termux is by default port `8022` (not 22) |
| Wi-Fi Only | Works inside the same Wi-Fi network (LAN) |
| Firewall | Android firewall must allow incoming LAN traffic |
| Mobile Data | Will not work over mobile data without port forwarding |

---

# 🧠 Why This Is Powerful

- You can use your Android like a **mini Linux server**!
- Host files, websites, transfer scripts, control your laptop from Android.
- Very lightweight, battery-friendly, and secure within Wi-Fi.

---

# ✅ Example Scenario:

👉 You install OpenSSH on Termux.  
👉 Your Android IP = `192.168.0.105` (found using `ip addr`).  
👉 Your laptop can SSH into Android with:
```bash
ssh -p 8022 u0_a123@192.168.0.105
```
👉 You can SCP upload/download files:
```bash
scp -P 8022 myfile.txt u0_a123@192.168.0.105:~
```

---

# 🌟 Final Simple Command Summary

| Action | Command |
|---|---|
| Install SSH | `pkg install openssh` |
| Start Server | `sshd` |
| Find IP | `ip addr show wlan0` |
| Connect from another device | `ssh -p 8022 username@IP` |

---

# 🔥 Would you like me to also show how you can:
- 📦 Turn your Termux into a **full file server** with **HTTP + upload**?
- 🎯 Setup **permanent SSH server** that auto-starts when Termux opens?
- 🌐 Expose it publicly using **Ngrok** (for outside LAN access)?

---

## 🚀 MIT License

When we say **"don't blame me"** under an **MIT License**,  
it’s mainly about **protecting yourself legally** from users who might face issues after using your code.

---

## 🧠 Imagine This Situation:

Suppose someone downloads your SCP Uploader, modifies it a little, and uses it to transfer important business files.

- If **your code had a small bug** (maybe a file wasn't uploaded correctly),
- **They lose important data**,
- They could **get angry** and say,  
  ➔ "**Because of your code, I lost my business files! I want to sue you for damages!**"

Even though you shared the code **for free**, they might **blame you** and **try to take legal action**.

---

## 🎯 What MIT License Says:

The **MIT License** includes a very important paragraph (standard legal text):

> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  
> IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY...

**In simple words:**  
- "You can use my code however you want."  
- "But if something goes wrong, it's **your own risk**."
- "**I (the original creator) am NOT responsible** for any problems, damages, or losses."

✅ **This protects you legally**.

---

## ✅ Quick Summary:

| Concept | Meaning |
|---|---|
| "Don't blame me" in MIT License | You are **NOT responsible** if their use of your code causes problems |
| Why needed? | To **protect you** from lawsuits or damage claims |
| Is it serious? | Not usually — but it's **important protection**, especially when your project becomes popular |

---

# ✨ In Simple One Line:

**The MIT License allows free use, but protects you from being blamed if something bad happens because of your code.**
