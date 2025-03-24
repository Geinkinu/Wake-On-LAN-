import imaplib
import email
from email.header import decode_header
from wakeonlan import send_magic_packet
import time
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import threading

# Configuration
IMAP_SERVER = 'imap.gmail.com'
EMAIL_ACCOUNT = 'example@gmail.com' # Use the gmail account that you will be receiving your email on.
EMAIL_PASSWORD = 'test test test test'  # Use the app-specific password here
WOL_MAC_ADDRESS = '' # Input your MAC Address
CHECK_INTERVAL = 1  # Check every 1 second
LABEL_NAME = 'TurnOnPC'  # Label name to filter emails
CHECK_LOG_INTERVAL = 10  # Interval for logging 'Checking..'

def create_image():
    # Create an image with a transparent background
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # Draw a simple icon (a blue circle)
    draw.ellipse((16, 16, 48, 48), fill='blue')
    
    return image

def get_label_id(mail, label_name):
    # Fetch the list of labels
    status, labels = mail.list()
    if status != 'OK':
        return None

    # Find the label ID
    for label in labels:
        # Decode and compare the label
        label = label.decode().split(' "/" ')[-1].strip('"')
        if label == label_name:
            return label
    return None

def check_email():
    try:
        # Connect to the server
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail.select('inbox')

        # Get the label ID
        label_id = get_label_id(mail, LABEL_NAME)
        if not label_id:
            return

        # Search for emails with the specific label
        status, messages = mail.search(None, f'(UNSEEN X-GM-LABELS "{LABEL_NAME}")')
        if status != 'OK':
            return
        
        email_ids = messages[0].split()

        for email_id in email_ids:
            status, msg_data = mail.fetch(email_id, '(RFC822)')
            if status != 'OK':
                continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = decode_header(msg["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()
                    
                    if 'Turn on PC' in subject:
                        print(f"Triggering action for email with subject: {subject}")
                        send_magic_packet(WOL_MAC_ADDRESS)
                        print("Magic packet sent!")
                        
                        # Mark the email for deletion
                        mail.store(email_id, '+FLAGS', '\\Deleted')
                        print(f"Email with ID {email_id} marked for deletion")
        
        # Permanently remove emails marked for deletion
        mail.expunge()
        
        # Logout and close the connection
        mail.logout()
    except Exception as e:
        print(f"Error checking email: {e}")

def email_checker():
    last_log_time = time.time()  # Initialize the last log time
    while True:
        check_email()
        
        current_time = time.time()
        if current_time - last_log_time >= CHECK_LOG_INTERVAL:
            print('Checking..')
            last_log_time = current_time
        
        time.sleep(CHECK_INTERVAL)

def on_quit(icon, item):
    icon.stop()

def main():
    # Create the system tray icon
    icon = Icon("WOL Script", create_image(), menu=Menu(
        MenuItem('Quit', on_quit)
    ))

    # Start email checker in a separate thread
    checker_thread = threading.Thread(target=email_checker)
    checker_thread.daemon = True
    checker_thread.start()

    # Run the icon in the system tray
    icon.run()

if __name__ == "__main__":
    main()
