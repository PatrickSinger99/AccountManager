import tkinter as tk
from PIL import ImageTk, Image
from win32api import GetMonitorInfo, MonitorFromPoint


class CornerSnappingHandler:

    window_snap_logo_paths = {
        "empty": "./icons/snap_empty.png",
        "filled": "./icons/snap_filled.png"
    }

    def __init__(self, parent_frame, controller):

        self.snap_window_frame = parent_frame
        self.controller = controller

        self.window_snap_imgs = {}

        for attribute, img_path in CornerSnappingHandler.window_snap_logo_paths.items():
            self.window_snap_imgs[f"top_left_{attribute}"] = (
                ImageTk.PhotoImage(Image.open(img_path)))
            self.window_snap_imgs[f"top_right_{attribute}"] = (
                ImageTk.PhotoImage(Image.open(img_path).transpose(Image.FLIP_LEFT_RIGHT)))
            self.window_snap_imgs[f"bottom_left_{attribute}"] = (
                ImageTk.PhotoImage(Image.open(img_path).transpose(Image.FLIP_TOP_BOTTOM)))
            self.window_snap_imgs[f"bottom_right_{attribute}"] = (
                ImageTk.PhotoImage(Image.open(img_path).transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)))

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

    def move_window(self, y_loc="bottom", x_loc="right"):
        monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
        work_area = monitor_info.get("Work")

        x_coord = work_area[2]-self.controller.winfo_width() if x_loc == "right" else 0
        y_coord = work_area[3]-self.controller.winfo_height() if y_loc == "bottom" else 0

        self.controller.geometry(f'{self.controller.winfo_width()}x{self.controller.winfo_height()}+{x_coord}+{y_coord}')

        return "break"  # Disable buttons click "animation" of shifting slightly down-right
