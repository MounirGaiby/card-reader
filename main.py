import time
import tkinter as tk
from py122u import nfc, error
from smartcard.Exceptions import CardConnectionException

class BadgeReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Badge Reader")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        self.status_label = tk.Label(self.root, text="Please scan card", font=("Arial", 12), fg="black", bg="#f0f0f0")
        self.status_label.pack(pady=10)

        # All UID labels
        self.labels = {}
        formats = [
            "Full Big endian", "Full Little endian",
            "3-byte First Big", "3-byte First Little", "3-byte Last Big", "3-byte Last Little",
            "4-byte First Big", "4-byte First Little", "4-byte Last Big", "4-byte Last Little"
        ]
        for fmt in formats:
            frame = tk.Frame(self.root, bg="#f0f0f0")
            frame.pack(pady=5, fill='x', padx=20)
            lbl = tk.Label(frame, text=f"{fmt}:", font=("Arial", 12), bg="#f0f0f0")
            lbl.pack(side=tk.LEFT)
            btn = tk.Button(frame, text="Copy", font=("Arial", 10), command=lambda f=fmt: self.copy_to_clipboard(f))
            btn.pack(side=tk.RIGHT)
            self.labels[fmt] = lbl

        self.copy_label = tk.Label(self.root, text="", font=("Arial", 10), fg="green", bg="#f0f0f0")
        self.copy_label.pack(pady=10)

        self.reader = None
        self.start_reader_check()

    def copy_to_clipboard(self, fmt):
        text = self.labels[fmt].cget("text").split(':')[1].strip()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.copy_label.config(text="Copied to clipboard!")
            self.root.after(500, lambda: self.copy_label.config(text=""))

    def start_reader_check(self):
        try:
            if self.reader is None:
                self.reader = nfc.Reader()
                self.reader.connect()
                self.status_label.config(text="Please scan card")

            try:
                uid = self.reader.get_uid()
                if uid:
                    hex_uid = [hex(byte)[2:].zfill(2) for byte in uid]
                    n = len(hex_uid)

                    # Full UID
                    full_big = int(''.join(hex_uid), 16)
                    full_little = int(''.join(reversed(hex_uid)), 16)

                    # 3-byte UID
                    if n >= 3:
                        first3 = hex_uid[:3]
                        last3 = hex_uid[-3:]
                        three_first_big = int(''.join(first3), 16)
                        three_first_little = int(''.join(reversed(first3)), 16)
                        three_last_big = int(''.join(last3), 16)
                        three_last_little = int(''.join(reversed(last3)), 16)
                    else:
                        three_first_big = three_first_little = three_last_big = three_last_little = 0

                    # 4-byte UID
                    if n >= 4:
                        first4 = hex_uid[:4]
                        last4 = hex_uid[-4:]
                        four_first_big = int(''.join(first4), 16)
                        four_first_little = int(''.join(reversed(first4)), 16)
                        four_last_big = int(''.join(last4), 16)
                        four_last_little = int(''.join(reversed(last4)), 16)
                    else:
                        four_first_big = four_first_little = four_last_big = four_last_little = 0

                    # Update labels
                    self.labels["Full Big endian"].config(text=f"Full Big endian: {full_big}")
                    self.labels["Full Little endian"].config(text=f"Full Little endian: {full_little}")
                    self.labels["3-byte First Big"].config(text=f"3-byte First Big: {three_first_big}")
                    self.labels["3-byte First Little"].config(text=f"3-byte First Little: {three_first_little}")
                    self.labels["3-byte Last Big"].config(text=f"3-byte Last Big: {three_last_big}")
                    self.labels["3-byte Last Little"].config(text=f"3-byte Last Little: {three_last_little}")
                    self.labels["4-byte First Big"].config(text=f"4-byte First Big: {four_first_big}")
                    self.labels["4-byte First Little"].config(text=f"4-byte First Little: {four_first_little}")
                    self.labels["4-byte Last Big"].config(text=f"4-byte Last Big: {four_last_big}")
                    self.labels["4-byte Last Little"].config(text=f"4-byte Last Little: {four_last_little}")

                    self.status_label.config(text="Card detected")
                else:
                    self.reset_labels()

            except CardConnectionException:
                self.reader = None
                self.reset_labels()

        except (error.NoReader, error.NoCommunication):
            self.reader = None
            self.reset_labels()

        except Exception:
            self.reader = None

        self.root.after(500, self.start_reader_check)

    def reset_labels(self):
        for key in self.labels:
            self.labels[key].config(text=f"{key}:")
        self.status_label.config(text="Please scan card")

def main():
    root = tk.Tk()
    app = BadgeReaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
