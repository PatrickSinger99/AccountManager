import tkinter as tk
import subprocess
from tkinter.font import Font


class AccountFrame(tk.Frame):
    label_fg = "black"
    label_hover_fg = "grey"
    label_copy_fg = "green"

    def __init__(self, master_root, account_title, account_infos, **kwargs):
        super().__init__(**kwargs)
        self.master_root = master_root
        self.account_title = account_title
        self.account_infos = account_infos

        """WIDGET APPEARANCE"""
        self.configure(bg="green")

        """HEADER"""

        # FRAME: Header
        self.header_frame = tk.Frame(self, bg="grey")
        self.header_frame.pack(fill="x", expand=True)

        # Account Title
        self.header_title = tk.Label(self.header_frame, text=self.account_title, bg=self.header_frame.cget("bg"))
        self.header_title.pack(side="left")

        # Account Delete Button
        self.delete_button = tk.Button(self.header_frame, text="delete")
        self.delete_button.pack(side="right")

        # Account Edit Button
        self.edit_button = tk.Button(self.header_frame, text="edit")
        self.edit_button.pack(side="right")

        """BODY"""

        self.body_frame = tk.Frame(self, bg="light grey")
        self.body_frame.pack(fill="both", expand=True)

        for i, (info_type, info_data) in enumerate(self.account_infos.items()):
            type_title = info_type.capitalize() + " :"
            tk.Label(self.body_frame, text=type_title, fg=AccountFrame.label_fg, bg=self.body_frame.cget("bg"),
                     font=Font(weight="bold", size=9)).grid(row=i, column=0, sticky="e")

            new_info_data = tk.Label(self.body_frame, text=info_data, bg=self.body_frame.cget("bg"), cursor="hand2",
                                     wraplength=150, justify="left")
            new_info_data.grid(row=i, column=1, sticky="w")
            new_info_data.bind("<Button-1>", lambda e, label=new_info_data, label_text=info_data: self.highlight_copy(e, label, label_text))

            new_info_data.bind("<Enter>", lambda e, label=new_info_data: self.on_label_enter(label))
            new_info_data.bind("<Leave>", lambda e, label=new_info_data: self.on_label_exit(label))

    def highlight_copy(self, event, label, label_text):
        initial_fg_color = label.cget("fg")

        # Change appearance of label to show it was copied to clipboard
        label.configure(text="Copied to Clipboard", fg=AccountFrame.label_copy_fg)

        # Copy text to clipboard
        cmd = 'echo ' + str(label_text).strip() + '|clip'
        subprocess.check_call(cmd, shell=True)

        # Change label back to initial state. Only if current state of label is not already set as copied
        if initial_fg_color != AccountFrame.label_copy_fg:
            self.after(1000, lambda: label.configure(text=label_text, fg=AccountFrame.label_fg))

    @staticmethod
    def on_label_enter(label):
        if label.cget("fg") != AccountFrame.label_copy_fg:
            label.config(fg=AccountFrame.label_hover_fg)

    @staticmethod
    def on_label_exit(label):
        if label.cget("fg") != AccountFrame.label_copy_fg:
            label.config(fg=AccountFrame.label_fg)


class App(tk.Tk):
    def __init__(self, account_data):
        super().__init__()
        self.account_data = account_data

        """APP SETTINGS"""

        self.title("Account Manager")
        self.resizable(False, False)

        """HEADER"""

        # FRAME: Header
        self.header_frame = tk.Frame(self, bg="blue", width=300, height=50)
        self.header_frame.pack_propagate(False)
        self.header_frame.pack(side="top")

        """BODY"""

        # FRAME:
        self.body_frame = tk.Frame(self, width=300, height=500)
        self.body_frame.pack_propagate(False)
        self.body_frame.pack(side="bottom")

        # Create canvas as wrapper for scroll widgets
        self.scrollable_canvas = tk.Canvas(self.body_frame, highlightthickness=0, relief='ridge', bg="red")

        # Frame inside canvas
        self.content_frame = tk.Frame(self.scrollable_canvas)
        self.content_frame.pack(side="left")
        self.content_frame.bind("<Configure>", lambda e: self.scrollable_canvas.configure(scrollregion=self.scrollable_canvas.bbox("all")))

        # Scrollbar for canvas
        self.content_scrollbar = tk.Scrollbar(self.scrollable_canvas, orient="vertical", command=self.scrollable_canvas.yview)
        self.content_scrollbar.pack(side="right", fill="y")

        # Add a window with the content frame inside canvas. Link scrollbar to canvas
        self.canvas_window = self.scrollable_canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        self.scrollable_canvas.configure(yscrollcommand=self.content_scrollbar.set)
        self.scrollable_canvas.pack(side="bottom", fill="both", expand=True)

        # Set window width inside canvas to canvas width
        self.scrollable_canvas.bind("<Configure>", self.set_canvas_window_width)

        # Bind scrollwheel to canvas to enable scrolling with mouse
        self.content_frame.bind("<Enter>", lambda x: self.bind_canvas_to_mousewheel(self.scrollable_canvas))
        self.content_frame.bind("<Leave>", lambda x: self.unbind_canvas_from_mousewheel(self.scrollable_canvas))

        """INITIAL CALLS"""

        self.display_accounts()

    def display_accounts(self):
        for i, (account_title, content) in enumerate(self.account_data.items()):
            new_account = AccountFrame(master=self.content_frame, master_root=self, account_title=account_title,
                                       account_infos=content)
            new_account.pack(fill="x", padx=3, pady=(3 if i == 0 else 0, 3))

    def set_canvas_window_width(self, event):
        new_width = event.width - 17  # 17 = width of scrollbar
        self.scrollable_canvas.itemconfig(self.canvas_window, width=new_width)

    def bind_canvas_to_mousewheel(self, canvas):
        # Bind mousewheel only if more elements are available than fit the screen
        if self.content_frame.winfo_height() > self.scrollable_canvas.winfo_height():
            canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    @staticmethod
    def unbind_canvas_from_mousewheel(canvas):
        canvas.unbind_all("<MouseWheel>")

    def on_mousewheel(self, event):
        self.scrollable_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


if __name__ == '__main__':
    data = {"Google": {"password": "pasjap3aüd2asd2", "phone": 201239432, "info": "Test info"},
            "Samsung": {"password": "sdfgdsf", "phone": 67435},
            "Amazon": {"password": "asasfdgd", "adress": "Street PLZ ..."},
            "Paypal": {"password": "203j43202c3", "security question": "answer", "info": "Test info", "date": "24.08.1888"},
            "Google1": {"password": "pasjap3aüd2asd2", "phone": 201239432, "info": "Test info"},
            "Samsung1": {"password": "sdfgdsf", "phone": 67435},
            "Amazon1": {"password": "asasfdgd", "adress": "Street PLZ ..."},
            "Paypal1": {"password": "203j43202c3", "security question": "answer", "info": "Test infoaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                       "date": "24.08.1888"}
            }
    app = App(data)
    app.mainloop()

