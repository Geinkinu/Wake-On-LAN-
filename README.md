# 🚀 Wake-On-LAN via Gmail & IFTTT

This Python script automates waking up a PC using **Wake-On-LAN (WOL)**, triggered by Gmail and IFTTT. The script continuously checks a Gmail inbox for incoming emails labeled with a specific keyword (**`TurnOnPC`**). Upon detecting such an email, it sends a magic packet to the specified MAC address, remotely powering on the target machine.

---

## 📌 Project Setup:

### ✉️ Gmail Filter:

- Create a filter in your Gmail account to label incoming emails containing the keyword **`TurnOnPC`**.

### ⚙️ IFTTT Configuration:

- Set up an [IFTTT](https://ifttt.com/) applet to send an email to your designated Gmail account when triggered (e.g., via voice command, app button, or other integrations).

### 🖥️ Server Execution:

- The script is designed to run indefinitely on a server or always-on device.

### 📦 Executable Setup:

- Convert the script into an `.exe` file using **[PyInstaller](https://www.pyinstaller.org/)** if you prefer running it as a startup program on Windows.

## 🛠️ Requirements:

- Python libraries:
    - `imaplib`
    - `email`
    - `wakeonlan`
    - `pystray`
    - `PIL` (Pillow)

- A Gmail account with **App-specific password enabled**.

## 🔑 Configuration Setup:

Edit your credentials within the script directly:

```python
IMAP_SERVER = 'imap.gmail.com'
EMAIL_ACCOUNT = 'your_email@gmail.com'
