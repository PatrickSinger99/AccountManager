import tkinter as tk
from account_frame import AccountFrame
from PIL import ImageTk, Image


class AccountManager(tk.Tk):

    acc_details_logo_paths = {
        "password": "./icons/password.png",
        "email": "./icons/email.png",
        "unknown_detail": "./icons/unknown_detail.png"
    }

    def __init__(self):
        super().__init__()

        """WINDOW ATTRIBUTES"""

        self.title("Account Manager")
        self.configure(bg="white")

        """IMAGES"""

        # Load every account detail icon as a Tk Image into a dictionary
        self.acc_detail_imgs = {}
        for attribute, img_path in AccountManager.acc_details_logo_paths.items():
            self.acc_detail_imgs[attribute] = ImageTk.PhotoImage(Image.open(img_path))

        """BODY"""

        # FRAME:
        self.body_frame = tk.Frame(self, width=300, height=500)
        self.body_frame.pack_propagate(False)
        self.body_frame.pack(side="bottom")

        # Create canvas as wrapper for scroll widgets
        self.scrollable_canvas = tk.Canvas(self.body_frame, highlightthickness=0, relief='ridge')

        # Frame inside canvas
        self.content_frame = tk.Frame(self.scrollable_canvas)
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
        for _ in range(10):
            test_frame = AccountFrame(master=self.content_frame, controller=self, bg="#ace3d4")
            test_frame.pack(padx=5, pady=5, fill="x")

        """NOTIFICATION BAR"""
        self.update()  # Update base tk window before to get current height for frame placement
        self.notification_frame = tk.Frame(self.body_frame, height=30, bg="green")
        self.notification_frame.pack_propagate(False)  # Prevent resizing through child elements
        # Notification frame only gets places when notification appears

        self.notification_text = tk.Label(self.notification_frame, text="", bg=self.notification_frame.cget("bg"), fg="white")
        self.notification_text.pack(fill="both", expand=True)

    def display_notification(self, message):
        self.notification_text.configure(text=message)

        # Check if a notification is currently displayed
        if not self.notification_frame.winfo_ismapped():
            self.slide_in_notification_bar()
            self.after(1000, self.slide_out_notification_bar)

    def update_notification_bar_placement(self, height):
        self.notification_frame.forget()
        self.notification_frame.place(x=0, y=self.body_frame.winfo_height() - height, relwidth=1)

    def slide_in_notification_bar(self):
        self.after(30, lambda: self.update_notification_bar_placement(10))
        self.after(60, lambda: self.update_notification_bar_placement(20))
        self.after(90, lambda: self.update_notification_bar_placement(30))

    def slide_out_notification_bar(self):
        self.after(30, lambda: self.update_notification_bar_placement(20))
        self.after(60, lambda: self.update_notification_bar_placement(10))
        self.after(90, self.notification_frame.place_forget)

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
    am = AccountManager()
    am.mainloop()
