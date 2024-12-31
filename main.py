import time
import tkinter as tk
from tkinter import messagebox
from py122u import nfc

class BadgeReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Badge Reader")
        self.root.geometry("300x200")  # Window size
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        # Label for Big Endian and Little Endian
        self.big_endian_label = tk.Label(self.root, text="UID 1: Big endian", font=("Arial", 14), bg="#f0f0f0")
        self.big_endian_label.pack(pady=20)

        self.little_endian_label = tk.Label(self.root, text="UID 2: Little endian", font=("Arial", 14), bg="#f0f0f0")
        self.little_endian_label.pack(pady=10)

        # Copy button
        self.copy_button = tk.Button(self.root, text="Copy", font=("Arial", 12), command=self.copy_to_clipboard)
        self.copy_button.pack(pady=20)

        self.reader = nfc.Reader()
        self.reader.connect()
        self.no_card_printed = False

    def copy_to_clipboard(self):
        # Copy the current displayed Big and Little Endian values to the clipboard
        badge_info = f"{self.big_endian_label.cget('text')}\n{self.little_endian_label.cget('text')}"
        self.root.clipboard_clear()
        self.root.clipboard_append(badge_info)
        messagebox.showinfo("Copied", "Badge information copied to clipboard!")

    def update_labels(self, badge_number_big, badge_number_little):
        # Update the labels with the new badge numbers
        self.big_endian_label.config(text=f"UID 1: Big endian {badge_number_big}")
        self.little_endian_label.config(text=f"UID 2: Little endian {badge_number_little}")

    def read_badge(self):
        try:
            while True:
                uid = self.reader.get_uid()
                if not uid:
                    if not self.no_card_printed:
                        self.no_card_printed = True
                    time.sleep(1)
                    continue

                self.no_card_printed = False
                hex_uid = [hex(byte) for byte in uid]
                badge_number_big = int(''.join(byte[2:] for byte in hex_uid), 16)
                badge_number_little = int(''.join(byte[2:] for byte in reversed(hex_uid)), 16)

                # Update the labels with new badge numbers
                self.update_labels(badge_number_big, badge_number_little)
                time.sleep(1)

        except Exception as e:
            print("Error reading card:", str(e))
            time.sleep(1)

def main():
    root = tk.Tk()
    app = BadgeReaderApp(root)
    root.after(100, app.read_badge)  # Start reading badge after the window is initialized
    root.mainloop()

if __name__ == "__main__":
    main()
