import tkinter as tk
from account_frame import AccountFrame
from group_frame import GroupFrame
from PIL import ImageTk, Image
from win32api import GetMonitorInfo, MonitorFromPoint
from tkinter.font import Font
from tkinter.ttk import Style


class AccountManager(tk.Tk):

    version = 0.2

    acc_details_logo_paths = {
        "password": "./icons/password.png",
        "email": "./icons/email.png",
        "unknown_detail": "./icons/unknown_detail.png"
    }

    window_snap_logo_paths = {
        "empty": "./icons/snap_empty.png",
        "filled": "./icons/snap_filled.png"
    }

    color_palette = {
        "primary": "#1EC4D0",
        "secondary": "#1A324F",
        "tertiary": "#A9C2CE"
    }

    def __init__(self):
        super().__init__()

        """WINDOW ATTRIBUTES"""

        self.title("Account Manager")
        self.configure(bg="white")
        self.iconbitmap("./icons/app_icon.ico")
        self.minsize(300, 300)
        self.maxsize(600, 1200)

        """IMAGES"""

        # Load every account detail icon as a Tk Image into a dictionary
        self.acc_detail_imgs = {}
        for attribute, img_path in AccountManager.acc_details_logo_paths.items():
            self.acc_detail_imgs[attribute] = ImageTk.PhotoImage(Image.open(img_path))

        self.window_snap_imgs = {}
        for attribute, img_path in AccountManager.window_snap_logo_paths.items():
            self.window_snap_imgs[f"top_left_{attribute}"] = ImageTk.PhotoImage(Image.open(img_path))
            self.window_snap_imgs[f"top_right_{attribute}"] = ImageTk.PhotoImage(Image.open(img_path).transpose(Image.FLIP_LEFT_RIGHT))
            self.window_snap_imgs[f"bottom_left_{attribute}"] = ImageTk.PhotoImage(Image.open(img_path).transpose(Image.FLIP_TOP_BOTTOM))
            self.window_snap_imgs[f"bottom_right_{attribute}"] = ImageTk.PhotoImage(Image.open(img_path).transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM))

        """HEADER"""

        self.header_frame = tk.Frame(self, bg=AccountManager.color_palette["primary"], width=300, height=50)
        self.header_frame.pack(side="top", fill="x")

        self.header_info_frame = tk.Frame(self.header_frame, bg=self.header_frame.cget("bg"))
        self.header_info_frame.pack(side="top", fill="x", padx=8, pady=(8, 0))

        self.header_title = tk.Label(self.header_info_frame, text="Account Manager", font=Font(size=13, weight="bold"),
                                     bg=self.header_info_frame.cget("bg"), fg=AccountManager.color_palette["secondary"])
        self.header_title.pack(side="left", anchor="sw")

        self.header_version = tk.Label(self.header_info_frame, text=f"v.{AccountManager.version}", font=Font(size=10),
                                       bg=self.header_info_frame.cget("bg"), fg=AccountManager.color_palette["secondary"])
        self.header_version.pack(side="left", anchor="s")

        self.snap_window_frame = tk.Frame(self.header_info_frame, bg=self.header_info_frame.cget("bg"))
        self.snap_window_frame.pack(side="right")

        # Snap Buttons
        self.move_top_left_button = tk.Button(self.snap_window_frame, image=self.window_snap_imgs["top_left_empty"], relief="flat",
                                              cursor="hand2", bd=0, bg=self.snap_window_frame.cget("bg"), activebackground=self.snap_window_frame.cget("bg"),
                                            highlightthickness=0)
        self.move_top_right_button = tk.Button(self.snap_window_frame, image=self.window_snap_imgs["top_right_empty"], relief="flat",
                                               cursor="hand2", bd=0, bg=self.snap_window_frame.cget("bg"), activebackground=self.snap_window_frame.cget("bg"),
                                               highlightthickness=0)
        self.move_bottom_left_button = tk.Button(self.snap_window_frame, image=self.window_snap_imgs["bottom_left_empty"], relief="flat",
                                                 cursor="hand2", bd=0, bg=self.snap_window_frame.cget("bg"), activebackground=self.snap_window_frame.cget("bg"),
                                                 highlightthickness=0)
        self.move_bottom_right_button = tk.Button(self.snap_window_frame, image=self.window_snap_imgs["bottom_right_empty"], relief="flat",
                                                  cursor="hand2", bd=0, bg=self.snap_window_frame.cget("bg"), activebackground=self.snap_window_frame.cget("bg"),
                                                   highlightthickness=0)

        self.move_top_left_button.bind("<Enter>", lambda e: self.move_top_left_button.configure(image=self.window_snap_imgs["top_left_filled"]))
        self.move_top_left_button.bind("<Leave>", lambda e: self.move_top_left_button.configure(image=self.window_snap_imgs["top_left_empty"]))
        self.move_top_right_button.bind("<Enter>", lambda e: self.move_top_right_button.configure(image=self.window_snap_imgs["top_right_filled"]))
        self.move_top_right_button.bind("<Leave>", lambda e: self.move_top_right_button.configure(image=self.window_snap_imgs["top_right_empty"]))
        self.move_bottom_left_button.bind("<Enter>", lambda e: self.move_bottom_left_button.configure(image=self.window_snap_imgs["bottom_left_filled"]))
        self.move_bottom_left_button.bind("<Leave>", lambda e: self.move_bottom_left_button.configure(image=self.window_snap_imgs["bottom_left_empty"]))
        self.move_bottom_right_button.bind("<Enter>", lambda e: self.move_bottom_right_button.configure(image=self.window_snap_imgs["bottom_right_filled"]))
        self.move_bottom_right_button.bind("<Leave>", lambda e: self.move_bottom_right_button.configure(image=self.window_snap_imgs["bottom_right_empty"]))

        # Commands need to be given as button binds to disable the buttons "animation" shifting slightly down-right
        self.move_top_left_button.bind("<Button-1>", lambda e: self.move_window("top", "left"))
        self.move_top_right_button.bind("<Button-1>", lambda e: self.move_window("top", "right"))
        self.move_bottom_left_button.bind("<Button-1>", lambda e: self.move_window("bottom", "left"))
        self.move_bottom_right_button.bind("<Button-1>", lambda e: self.move_window("bottom", "right"))

        self.move_top_left_button.grid(row=0, column=0)
        self.move_top_right_button.grid(row=0, column=1)
        self.move_bottom_left_button.grid(row=1, column=0)
        self.move_bottom_right_button.grid(row=1, column=1)

        self.header_search_frame = tk.Frame(self.header_frame, bg=self.header_frame.cget("bg"))
        self.header_search_frame.pack(side="bottom", fill="x", padx=8, pady=8)

        self.search_entry = tk.Entry(self.header_search_frame, relief="flat", bg=AccountManager.color_palette["tertiary"])
        self.search_entry.pack(side="bottom", fill="x", ipady=2)

        """BODY"""

        # FRAME:
        self.body_frame = tk.Frame(self, width=300, height=500, bg=AccountManager.color_palette["secondary"])
        self.body_frame.pack_propagate(False)
        self.body_frame.pack(side="bottom", fill="both", expand=True)

        # Create canvas as wrapper for scroll widgets
        self.scrollable_canvas = tk.Canvas(self.body_frame, highlightthickness=0, relief='ridge', bg=self.body_frame.cget("bg"))

        # Frame inside canvas
        self.content_frame = tk.Frame(self.scrollable_canvas, bg=self.scrollable_canvas.cget("bg"))
        self.content_frame.pack(side="left")
        self.content_frame.bind("<Configure>", lambda e: self.scrollable_canvas.configure(
            scrollregion=self.scrollable_canvas.bbox("all")))

        # Scrollbar for canvas
        self.content_scrollbar = tk.Scrollbar(self.scrollable_canvas, orient="vertical",
                                              command=self.scrollable_canvas.yview)
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

        # TEMP
        group_1 = GroupFrame(master=self.content_frame, controller=self, title="E-Mails")
        group_2 = GroupFrame(master=self.content_frame, controller=self, title="Shopping")

        group_1.add_accounts([AccountFrame(master=group_1.content_frame, controller=self, bg=AccountManager.color_palette["tertiary"]) for _ in range(4)])
        group_2.add_accounts([AccountFrame(master=group_2.content_frame, controller=self, bg=AccountManager.color_palette["tertiary"]) for _ in range(8)])

        group_1.pack(padx=5, fill="x")
        group_2.pack(padx=5, fill="x")

        """NOTIFICATION BAR"""

        self.update()  # Update base tk window before to get current height for frame placement
        self.notification_frame = tk.Frame(self.body_frame, height=30, bg="green")
        self.notification_frame.pack_propagate(False)  # Prevent resizing through child elements
        # Notification frame only gets places when notification appears

        self.notification_text = tk.Label(self.notification_frame, text="", bg=self.notification_frame.cget("bg"), fg="white")
        self.notification_text.pack(fill="both", expand=True)

        self.extend_notification_bar = False

    def display_notification(self, message):
        self.notification_text.configure(text=message)

        # Check if a notification is currently displayed
        if not self.notification_frame.winfo_ismapped():
            self.slide_in_notification_bar()
            self.after(1000, self.slide_out_notification_bar)
        else:
            self.extend_notification_bar = True
            self.after(1000, self.slide_out_notification_bar)

    def update_notification_bar_placement(self, height):
        self.notification_frame.forget()
        self.notification_frame.place(x=0, y=self.body_frame.winfo_height() - height, relwidth=1)

    def slide_in_notification_bar(self):
        self.after(30, lambda: self.update_notification_bar_placement(10))
        self.after(60, lambda: self.update_notification_bar_placement(20))
        self.after(90, lambda: self.update_notification_bar_placement(30))

    def slide_out_notification_bar(self):
        if not self.extend_notification_bar:
            self.after(30, lambda: self.update_notification_bar_placement(20))
            self.after(60, lambda: self.update_notification_bar_placement(10))
            self.after(90, self.notification_frame.place_forget)
        else:
            self.extend_notification_bar = False

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

    def move_window(self, y_loc="bottom", x_loc="right"):
        monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
        work_area = monitor_info.get("Work")

        x_coord = work_area[2]-self.winfo_width() if x_loc == "right" else 0
        y_coord = work_area[3]-self.winfo_height() if y_loc == "bottom" else 0

        self.geometry(f'{self.winfo_width()}x{self.winfo_height()}+{x_coord}+{y_coord}')

        return "break"  # Disable buttons click "animation" of shifting slightly down-right


if __name__ == '__main__':
    am = AccountManager()
    am.mainloop()
