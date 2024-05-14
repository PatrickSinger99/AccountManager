import tkinter as tk


class DeleteAccountWindow(tk.Toplevel):
    def __init__(self, account_details, controller, account_frame, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = controller
        self.details = account_details
        self.account_frame = account_frame

        """TITLE"""

        self.title_label = tk.Label(self, text=f"Permanently delete account {account_details['account_name']}?")
        self.title_label.pack()

        """USER BUTTONS"""

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack()

        self.delete_confirm_button = tk.Button(self.buttons_frame, text="Delete", command=self.on_confirm)
        self.delete_confirm_button.pack(side="right")

        self.delete_cancel_button = tk.Button(self.buttons_frame, text="Cancel", command=self.on_cancel)
        self.delete_cancel_button.pack(side="left")

        # Place window in center of main gui window
        self.wait_visibility()
        x = self.controller.winfo_x() + self.controller.winfo_width() // 2 - self.winfo_width() // 2
        y = self.controller.winfo_y() + self.controller.winfo_height() // 2 - self.winfo_height() // 2
        self.geometry(f"+{x}+{y}")

    def on_cancel(self):
        self.destroy()

    def on_confirm(self):
        self.controller.data_handler.delete_account(account_id=self.details["account_id"])
        self.account_frame.destroy()
        self.destroy()
