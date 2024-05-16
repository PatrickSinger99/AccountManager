import tkinter as tk


class EditAccountWindow(tk.Toplevel):
    def __init__(self, account_details, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = controller
        self.account_details = account_details
        self.detail_attributes = self.controller.data_handler.get_detail_attributes()

        """TITLE"""

        self.title_label = tk.Label(self, text=f"Edit account {account_details['account_name']}")
        self.title_label.pack()

        """EDIT SECTION"""

        self.edit_frame = tk.Frame(self)
        self.edit_frame.pack()

        for i, (detail_name, detail_info) in enumerate(self.account_details.items()):
            try:
                if not self.detail_attributes[detail_name]["hidden"]:
                    multi_line = self.detail_attributes[detail_name]["multi_line"]
                    self.add_detail_edit(detail_name, detail_info, row=i, multi_line_entry=multi_line)

            # Unknown detail case
            except KeyError:
                self.add_detail_edit(detail_name, detail_info, row=i, multi_line_entry=False)

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

    def add_detail_edit(self, detail_name, detail_info, row, multi_line_entry=False):
        try:
            display_text = self.controller.acc_detail_display[detail_name]["display_name"]
        except KeyError:
            display_text = detail_name

        detail_name_label = tk.Label(self.edit_frame, text=display_text)
        detail_name_label.grid(row=row, column=0)

        if not multi_line_entry:
            detail_info_entry = tk.Entry(self.edit_frame, width=20)
        else:
            detail_info_entry = tk.Text(self.edit_frame, width=30, height=3)

        detail_info_entry.insert(tk.END, detail_info)
        detail_info_entry.grid(row=row, column=1)

        detail_delete_button = tk.Button(self.edit_frame, text="delete")
        detail_delete_button.grid(row=row, column=2)


