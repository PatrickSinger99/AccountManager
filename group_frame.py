import tkinter as tk
from PIL import ImageTk, Image, ImageOps
from tkinter.font import Font
from tooltip import create_tool_tip
from typing import Union
import re


class GroupFrame(tk.Frame):

    title_size = 12
    title_color = "white"
    divider_color = "white"

    default_collapse_down_icon_path = "./icons/collapse_down.png"
    default_collapse_up_icon_path = "./icons/collapse_up.png"

    def __init__(self, controller, title: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = controller
        self.configure(bg=self.master.cget("bg"))

        self.collapsed_state = False
        self.child_accounts = []

        """ICONS"""

        self.collapse_down_icon = ImageTk.PhotoImage(Image.open(GroupFrame.default_collapse_down_icon_path))
        self.collapse_up_icon = ImageTk.PhotoImage(Image.open(GroupFrame.default_collapse_up_icon_path))

        """CONTENT"""

        self.header_frame = tk.Frame(self, bg=self.cget("bg"))
        self.header_frame.pack(side="top", fill="x")

        self.title_label = tk.Label(self.header_frame, text=title, font=Font(size=GroupFrame.title_size),
                                    fg=GroupFrame.title_color, bg=self.header_frame.cget("bg"))
        self.title_label.pack(side="left")

        self.collapse_button = tk.Button(self.header_frame, command=self.on_collapse_button_press, cursor="hand2",
                                         image=self.collapse_down_icon if self.collapsed_state else self.collapse_up_icon,
                                         relief="flat", highlightthickness=0, bd=0, bg=self.header_frame.cget("bg"),
                                         activebackground=self.header_frame.cget("bg"))
        self.collapse_button.pack(side="right", padx=5)

        self.content_frame = tk.Frame(self, bg=self.cget("bg"))
        self.content_frame.pack(side="bottom", fill="x")

        self.divider_element = tk.Frame(self, bg=GroupFrame.divider_color)
        self.divider_element.pack(side="top", fill="x")

        # This placeholder is needed to dynamically adjust the pack size of the content frame when collapsing accounts
        self.update_placeholder = tk.Frame(self.content_frame)
        self.update_placeholder.pack()

    def add_accounts(self, account_frames):

        if type(account_frames) not in (list, tuple):
            account_frames = [account_frames]

        for account_frame in account_frames:
            self.child_accounts.append(account_frame)

        self.draw_accounts()

    def draw_accounts(self, regex_filter=None):
        for account in self.child_accounts:
            if regex_filter is None or re.search(regex_filter, "test"):
                account.pack(pady=(5, 0), fill="x")

    def on_collapse_button_press(self):
        if self.collapsed_state:
            self.collapsed_state = False

            self.draw_accounts()
            self.collapse_button.configure(image=self.collapse_up_icon)

        else:
            self.collapsed_state = True
            for child in self.child_accounts:
                child.pack_forget()
            self.update_placeholder.pack()  # Pack placeholder frame to update pack size
            self.collapse_button.configure(image=self.collapse_down_icon)
