import tkinter as tk
from tkinter.font import Font


class EditAccountWindow(tk.Toplevel):
    detail_font = {"family": "Segoe UI", "size": 9}

    def __init__(self, account_details, controller, account_frame, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = controller
        self.parent = account_frame
        self.account_details = account_details
        self.detail_attributes = self.controller.data_handler.get_detail_attributes()
        self.detail_font = Font(family=EditAccountWindow.detail_font["family"], size=EditAccountWindow.detail_font["size"])

        self.initial_detail_values = {}
        self.detail_entry_widgets = {}

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
                    new_widget = self.add_detail_edit(detail_name, detail_info, row=i, multi_line_entry=multi_line)
                    self.detail_entry_widgets[detail_name] = new_widget
                    self.initial_detail_values[detail_name] = str(detail_info)

            # Unknown detail case
            except KeyError:
                new_widget = self.add_detail_edit(detail_name, detail_info, row=i, multi_line_entry=False)
                self.detail_entry_widgets[detail_name] = new_widget
                self.initial_detail_values[detail_name] = str(detail_info)

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

        # Check for changes in the widget entry boxes
        changed_details = {}
        for detail_name, detail_widget in self.detail_entry_widgets.items():
            new_detail_value = self.get_widget_content(detail_widget)

            if new_detail_value != self.initial_detail_values[detail_name]:
                changed_details[detail_name] = new_detail_value

                # CASE: Delete
                if new_detail_value == "":
                    changed_details[detail_name] = None  # None = Signal for datahandler to delete

        self.controller.data_handler.update_account(account_id=self.account_details["account_id"],
                                                    updated_parameters=changed_details,
                                                    save_to_file=True)

        self.parent.update_draw()

        self.destroy()

    def on_cancel(self):
        self.destroy()

    @staticmethod
    def get_widget_content(widget):
        if isinstance(widget, tk.Entry):
            return widget.get()
        elif isinstance(widget, tk.Text):
            return widget.get("1.0", "end-1c")  # 'end-1c' excludes the last newline character
        else:
            raise ValueError("Unsupported widget type")

    def add_detail_edit(self, detail_name, detail_info, row, multi_line_entry=False):
        try:
            display_text = self.controller.acc_detail_display[detail_name]["display_name"]
        except KeyError:
            display_text = detail_name

        detail_name_label = tk.Label(self.edit_frame, text=display_text)
        detail_name_label.grid(row=row, column=0, sticky="e")

        if not multi_line_entry:
            detail_info_entry = tk.Entry(self.edit_frame, font=self.detail_font)
        else:

            num_of_lines = detail_info.count("\n") + 1
            detail_info_entry = tk.Text(self.edit_frame, width=30, height=num_of_lines, font=self.detail_font)

            def on_modify(e):
                """Gets called when text content changes and adjust widget size based on the currently written lines"""
                e.widget.after_idle(lambda: detail_info_entry.config(height=(detail_info_entry.get("1.0", "end-1c").count("\n") + 1)))

            detail_info_entry.bind('<Key>', on_modify)

        detail_info_entry.insert(tk.END, detail_info)
        detail_info_entry.grid(row=row, column=1, sticky="ew")

        detail_delete_button = tk.Button(self.edit_frame, text="delete")
        detail_delete_button.grid(row=row, column=2)

        return detail_info_entry

