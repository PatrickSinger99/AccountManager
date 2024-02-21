import tkinter as tk
from PIL import ImageTk, Image
from tkinter.font import Font
from tooltip import create_tool_tip
import subprocess


class AccountFrame(tk.Frame):

    default_account_logo_path = "./icons/default_logo.png"

    colors = {
        "detail_default": "black",
        "detail_hover": "grey",
        "detail_click": "white"
    }

    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = controller
        self.configure()

        self.account_logo = ImageTk.PhotoImage(Image.open(AccountFrame.default_account_logo_path))

        """UPPER LEVEL FRAMES"""

        self.image_frame = tk.Frame(self, bg=self.cget("bg"))
        self.image_frame.pack(side="left", fill="y", padx=5, pady=5)

        self.info_frame = tk.Frame(self, bg=self.cget("bg"))
        self.info_frame.pack(side="left", fill="both", expand=True, pady=5)

        self.options_frame = tk.Frame(self, bg="light grey", width=50)
        self.options_frame.pack(side="left", fill="y", padx=5, pady=5)

        """IMAGE FRAME"""

        self.image_label = tk.Label(self.image_frame, image=self.account_logo, bg=self.image_frame.cget("bg"))
        self.image_label.pack()

        """INFO FRAME"""

        self.title_label = tk.Label(self.info_frame, text="Example Account", bg=self.info_frame.cget("bg"),
                                    font=Font(size=11), anchor="w")
        self.title_label.pack(fill="x")

        self.data_frame = tk.Frame(self.info_frame, bg=self.info_frame.cget("bg"))
        self.data_frame.pack(fill="x")

        self.add_detail("email", "examplemail@lol.com")
        self.add_detail("password", "asdp12apsdja2")
        self.add_detail("name", "test name")

    def add_detail(self, detail, value):
        frame_bg = self.data_frame.cget("bg")
        new_detail_frame = tk.Frame(self.data_frame, bg=frame_bg)

        if detail in self.controller.acc_detail_imgs.keys():
            detail_logo = self.controller.acc_detail_imgs[detail]
        else:
            detail_logo = self.controller.acc_detail_imgs["unknown_detail"]

        detail_logo = tk.Label(new_detail_frame, image=detail_logo, bg=frame_bg)
        detail_logo.pack(side="left")
        create_tool_tip(detail_logo, detail.capitalize())

        detail_value = tk.Label(new_detail_frame, text=value, bg=frame_bg, font=Font(size=10), cursor="hand2",
                                fg=AccountFrame.colors["detail_default"],
                                activeforeground=AccountFrame.colors["detail_click"])
        detail_value.bind("<Button-1>", lambda e: self.copy_to_clipboard(value))
        detail_value.bind("<Enter>", lambda e: self.on_detail_enter(detail_value))
        detail_value.bind("<Leave>", lambda e: self.on_detail_leave(detail_value))
        detail_value.pack(side="left")

        new_detail_frame.pack(fill="x")

    @staticmethod
    def on_detail_enter(detail_obj):
        detail_obj.configure(fg=AccountFrame.colors["detail_hover"])

    @staticmethod
    def on_detail_leave(detail_obj):
        detail_obj.configure(fg=AccountFrame.colors["detail_default"])

    def copy_to_clipboard(self, value):
        # Copy text to clipboard
        cmd = 'echo ' + str(value).strip() + '|clip'
        subprocess.check_call(cmd, shell=True)

        print(f"Copied \"{value}\" to clipboard")

        # Play notification bar
        self.controller.display_notification("Copied to Clipboard")
