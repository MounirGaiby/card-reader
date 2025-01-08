import time
import tkinter as tk
from py122u import nfc, error
from smartcard.Exceptions import CardConnectionException

class BadgeReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Badge Reader")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        # Status label
        self.status_label = tk.Label(
            self.root, 
            text="Please scan card", 
            font=("Arial", 12),
            fg="black",
            bg="#f0f0f0"
        )
        self.status_label.pack(pady=10)

        # Frame for big endian
        big_frame = tk.Frame(self.root, bg="#f0f0f0")
        big_frame.pack(pady=10, fill='x', padx=20)

        self.big_endian_label = tk.Label(
            big_frame, 
            text="UID 1: Big endian", 
            font=("Arial", 12), 
            bg="#f0f0f0"
        )
        self.big_endian_label.pack(side=tk.LEFT)

        self.copy_big_button = tk.Button(
            big_frame, 
            text="Copy", 
            font=("Arial", 10),
            command=lambda: self.copy_to_clipboard("big")
        )
        self.copy_big_button.pack(side=tk.RIGHT)

        # Frame for little endian
        little_frame = tk.Frame(self.root, bg="#f0f0f0")
        little_frame.pack(pady=10, fill='x', padx=20)

        self.little_endian_label = tk.Label(
            little_frame, 
            text="UID 2: Little endian", 
            font=("Arial", 12), 
            bg="#f0f0f0"
        )
        self.little_endian_label.pack(side=tk.LEFT)

        self.copy_little_button = tk.Button(
            little_frame, 
            text="Copy", 
            font=("Arial", 10),
            command=lambda: self.copy_to_clipboard("little")
        )
        self.copy_little_button.pack(side=tk.RIGHT)

        # Copy notification label
        self.copy_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 10),
            fg="green",
            bg="#f0f0f0"
        )
        self.copy_label.pack(pady=10)

        self.reader = None
        self.start_reader_check()

    def copy_to_clipboard(self, endian_type):
        if endian_type == "big":
            text = self.big_endian_label.cget("text").split("endian")[1].strip()
        else:
            text = self.little_endian_label.cget("text").split("endian")[1].strip()

        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.copy_label.config(text="Copied to clipboard!")
            self.root.after(500, lambda: self.copy_label.config(text=""))

    def start_reader_check(self):
        """Main loop to check for reader and card"""
        try:
            # Try to initialize reader if not present
            if self.reader is None:
                self.reader = nfc.Reader()
                self.reader.connect()
                self.status_label.config(text="Please scan card")

            # Try to read card
            try:
                uid = self.reader.get_uid()

                if uid:
                    hex_uid = [hex(byte) for byte in uid]
                    badge_number_big = int(''.join(byte[2:] for byte in hex_uid), 16)
                    badge_number_little = int(''.join(byte[2:] for byte in reversed(hex_uid)), 16)

                    self.big_endian_label.config(text=f"UID 1: Big endian {badge_number_big}")
                    self.little_endian_label.config(text=f"UID 2: Little endian {badge_number_little}")
                    self.status_label.config(text="Card detected")
                else:
                    self.big_endian_label.config(text="UID 1: Big endian")
                    self.little_endian_label.config(text="UID 2: Little endian")
                    self.status_label.config(text="Please scan card")

            except CardConnectionException as e:
                self.reader = None
                self.big_endian_label.config(text="UID 1: Big endian")
                self.little_endian_label.config(text="UID 2: Little endian")
                self.status_label.config(text="Please scan card")

        except (error.NoReader, error.NoCommunication) as e:
            self.reader = None
            self.big_endian_label.config(text="UID 1: Big endian")
            self.little_endian_label.config(text="UID 2: Little endian")
            self.status_label.config(text="Please scan card")

        except Exception as e:
            self.reader = None

        # Loop every 2 seconds
        self.root.after(500, self.start_reader_check)

def main():
    root = tk.Tk()
    app = BadgeReaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()