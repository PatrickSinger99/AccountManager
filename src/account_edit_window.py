import tkinter as tk


class EditAccountWindow(tk.Toplevel):
    def __init__(self, account_details, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = controller
        self.account_details = account_details

        """TITLE"""

        self.title_label = tk.Label(self, text=f"Edit account {account_details['account_name']}")
        self.title_label.pack()

        """EDIT SECTION"""

        self.edit_frame = tk.Frame(self)
        self.edit_frame.pack()

        for i, (detail_name, detail_info) in enumerate(self.account_details.items()):
            self.add_detail_edit(detail_name, detail_info, row=i)

        """USER BUTTONS"""

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack()

        self.save_button = tk.Button(self.buttons_frame, text="Save", command=self.on_save)
        self.save_button.pack(side="right")

        self.cancel_button = tk.Button(self.buttons_frame, text="Cancel", command=self.on_cancel)
        self.cancel_button.pack(side="left")

        # Place window in center of main gui window
        self.wait_visibility()
        x = self.controller.winfo_x() + self.controller.winfo_width() // 2 - self.winfo_width() // 2
        y = self.controller.winfo_y() + self.controller.winfo_height() // 2 - self.winfo_height() // 2
        self.geometry(f"+{x}+{y}")

    def on_save(self):
        # TODO
        self.destroy()

    def on_cancel(self):
        self.destroy()

    def add_detail_edit(self, detail_name, detail_info, row):
        detail_name_label = tk.Label(self.edit_frame, text=detail_name)
        detail_name_label.grid(row=row, column=0)

        detail_info_label = tk.Label(self.edit_frame, text=detail_info)
        detail_info_label.grid(row=row, column=1)

        detail_delete_button = tk.Button(self.edit_frame, text="delete")
        detail_delete_button.grid(row=row, column=2)


