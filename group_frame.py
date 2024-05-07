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

    no_results_found_message = "No matches"

    def __init__(self, controller, title: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = controller
        self.configure(bg=self.master.cget("bg"))

        self.collapsed_state = False
        self.current_filter = None  # Save last filter state to remember when toggling group collapse draws
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

        # No results found Notifier
        self.no_results_found_label = tk.Label(self.content_frame, bg=self.content_frame.cget("bg"),
                                               text=GroupFrame.no_results_found_message)

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
        # Save filter applied
        self.current_filter = regex_filter
        results_found = False  # Determines if "No results" message is shown

        # Remove all previously drawn account frames
        self.no_results_found_label.pack_forget()
        for child in self.child_accounts:
            child.pack_forget()

        # Only draw if group is not collapsed
        if not self.collapsed_state:

            for account in self.child_accounts:
                # Draw all accounts if no regex filter applied
                if regex_filter is None:
                    account.pack(pady=(5, 0), fill="x")

                # Only draw accounts if at least one detail matches if the regex filter applied
                else:
                    for detail_name, detail_content in account.account_details.items():
                        if re.search(regex_filter, str(detail_content)):
                            account.pack(pady=(5, 0), fill="x")
                            results_found = True

            # If no matches found, display message
            if regex_filter is not None and not results_found:
                self.no_results_found_label.pack(pady=(5, 0), fill="x")

    def on_collapse_button_press(self):
        if self.collapsed_state:
            self.collapsed_state = False

            self.draw_accounts(regex_filter=self.current_filter)
            self.collapse_button.configure(image=self.collapse_up_icon)

        else:
            self.collapsed_state = True
            for child in self.child_accounts:
                child.pack_forget()
            self.no_results_found_label.pack_forget()

            self.update_placeholder.pack()  # Pack placeholder frame to update pack size
            self.collapse_button.configure(image=self.collapse_down_icon)
