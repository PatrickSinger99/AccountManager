import tkinter as tk
from PIL import ImageTk, Image
from tkinter.font import Font
from tooltip import create_tool_tip
import subprocess
from utils import change_icon_color
from account_edit_window import EditAccountWindow
from account_delete_window import DeleteAccountWindow


class AccountFrame(tk.Frame):

    default_account_logo_path = "./data/gui_icons/default_logo.png"
    hidden_details = ("group_id", "account_name", "account_id")

    def __init__(self, controller, account_details: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = controller
        self.configure()

        self.account_logo = ImageTk.PhotoImage(change_icon_color(Image.open(AccountFrame.default_account_logo_path),
                                                                 target_color=self.controller.colors["account_icons"],
                                                                 tk_controller=self.controller))
        self.account_details = account_details

        """UPPER LEVEL FRAMES"""

        self.image_frame = tk.Frame(self, bg=self.cget("bg"))
        self.image_frame.pack(side="left", fill="y", padx=5, pady=5)

        self.info_frame = tk.Frame(self, bg=self.cget("bg"))
        self.info_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        """IMAGE FRAME"""

        self.image_label = tk.Label(self.image_frame, image=self.account_logo, bg=self.image_frame.cget("bg"))
        self.image_label.pack()

        """INFO FRAME"""

        self.title_frame = tk.Frame(self.info_frame, bg=self.info_frame.cget("bg"))
        self.title_frame.pack(fill="x")

        self.title_label = tk.Label(self.title_frame, text=self.account_details["account_name"], bg=self.info_frame.cget("bg"),
                                    font=Font(size=11, weight="bold"), anchor="w", fg=self.controller.colors["account_text"])
        self.title_label.pack(side="left")

        self.delete_button = tk.Button(self.title_frame, text="del", bd=0, relief="flat", cursor="hand2",
                                       bg=self.title_frame.cget("bg"), activebackground=self.title_frame.cget("bg"),
                                       command=self.on_delete_button_click)

        self.edit_button = tk.Button(self.title_frame, text="edit", bd=0, relief="flat", bg=self.title_frame.cget("bg"),
                                     activebackground=self.title_frame.cget("bg"), cursor="hand2",
                                     command=self.on_edit_button_click)

        self.data_frame = tk.Frame(self.info_frame, bg=self.info_frame.cget("bg"))
        self.data_frame.pack(fill="x")

        """HOVER BEHAVIOUR"""

        self.bind("<Enter>", lambda e: self.on_hover_enter())
        self.bind("<Leave>", lambda e: self.on_hover_leave())

        """INIT CALLS"""
        self.draw()

    def draw(self):
        for key, value in self.account_details.items():
            if key not in AccountFrame.hidden_details:
                self.add_detail(key, value)

    def add_detail(self, detail, value):
        frame_bg = self.data_frame.cget("bg")
        new_detail_frame = tk.Frame(self.data_frame, bg=frame_bg)

        if detail in self.controller.acc_detail_display.keys():
            detail_tk_img = self.controller.acc_detail_display[detail]["img"]
        else:
            detail_tk_img = self.controller.acc_detail_display["unknown_detail"]["img"]

        detail_logo = tk.Label(new_detail_frame, image=detail_tk_img, bg=frame_bg)
        detail_logo.pack(side="left", anchor="n")

        try:
            create_tool_tip(detail_logo, self.controller.acc_detail_display[detail]["display_name"])
        except KeyError:
            create_tool_tip(detail_logo, self.controller.acc_detail_display["unknown_detail"]["display_name"] + ": " + detail)

        detail_value = tk.Label(new_detail_frame, text=value, bg=frame_bg, font=Font(size=10), cursor="hand2",
                                fg=self.controller.colors["account_text"])
        detail_value.bind("<Button-1>", lambda e: self.copy_to_clipboard(value))
        detail_value.bind("<Enter>", lambda e: self.on_detail_enter(detail_value))
        detail_value.bind("<Leave>", lambda e: self.on_detail_leave(detail_value))
        detail_value.pack(side="left")
        # create_tool_tip(detail_value, "Click to copy")

        new_detail_frame.pack(fill="x")

    def on_detail_enter(self, detail_obj):
        detail_obj.configure(fg=self.controller.colors["account_text_hover"])

    def on_detail_leave(self, detail_obj):
        detail_obj.configure(fg=self.controller.colors["account_text"])

    def copy_to_clipboard(self, value):
        # Copy text to clipboard
        cmd = 'echo ' + str(value).strip() + '|clip'
        subprocess.check_call(cmd, shell=True)

        print(f"Copied \"{value}\" to clipboard")

        # Play notification bar
        self.controller.display_notification("Copied to Clipboard")

    def on_hover_enter(self):
        self.delete_button.pack(side="right")
        self.edit_button.pack(side="right")

    def on_hover_leave(self):
        self.delete_button.pack_forget()
        self.edit_button.pack_forget()

    def on_edit_button_click(self):
        edit_window = EditAccountWindow(self.account_details, self.controller)  # Toplevel type

    def on_delete_button_click(self):
        delete_window = DeleteAccountWindow(self.account_details, self.controller, self)  # Toplevel type


