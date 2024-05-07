import os.path
import tkinter as tk
from account_frame import AccountFrame
from group_frame import GroupFrame
from PIL import ImageTk, Image
from tkinter.font import Font
from tkinter.ttk import Style
from data_handler import DataHandler
from corner_snap_button import CornerSnappingHandler
from utils import change_icon_color


class AccountManager(tk.Tk):

    version = 0.2

    default_color_palette = {
        "primary": "#1EC4D0",
        "secondary": "#1A324F",
        "tertiary": "#A9C2CE",
        "group_title": "#A9C2CE",
        "account_icons": "#1A324F",
        "account_text": "#1A324F",
        "account_text_hover": "white",
        "gui_icons": "#1A324F"
    }

    gui_icons = {
        "settings": "data/gui_icons/settings.png",
        "settings_hover": "data/gui_icons/settings_hover.png"
    }

    def __init__(self):
        super().__init__()

        """WINDOW ATTRIBUTES"""

        self.title("Account Manager")
        self.configure(bg="white")
        self.iconbitmap("./data/gui_icons/app_icon.ico")
        self.minsize(300, 300)
        self.maxsize(600, 1200)

        """COLORS"""
        self.colors = AccountManager.default_color_palette

        """DATA"""
        self.data_handler = DataHandler(save_file_location="data")
        self.data_handler.dev_only_create_dummy_data()  # ONLY FOR DEVELOPMENT

        """IMAGES"""

        # Load every account details name and icon (as Tk Image) into a dictionary
        self.acc_detail_display = {}
        for img_id, img_data in self.data_handler.data["settings"]["detail_icons"].items():
            # Create full path of img source
            img_path = os.path.join(self.data_handler.data["settings"]["detail_icon_location"], img_data["img"])

            # Create img object and ajust color
            img_obj = ImageTk.PhotoImage(change_icon_color(Image.open(img_path), tk_controller=self,
                                                           target_color=self.colors["account_icons"]))

            # Add to dictionary
            self.acc_detail_display[img_id] = {"img": img_obj, "display_name": img_data["display_name"]}

        # Load every gui icon as Tk Image into a dict
        self.gui_icons = {}
        for img_id, img_path in AccountManager.gui_icons.items():
            self.gui_icons[img_id] = ImageTk.PhotoImage(change_icon_color(Image.open(img_path), tk_controller=self,
                                                        target_color=self.colors["gui_icons"]))

        """HEADER"""

        self.header_frame = tk.Frame(self, bg=self.colors["primary"], width=300, height=50)
        self.header_frame.pack(side="top", fill="x")

        self.header_info_frame = tk.Frame(self.header_frame, bg=self.header_frame.cget("bg"))
        self.header_info_frame.pack(side="top", fill="x", padx=8, pady=(8, 0))

        self.header_title = tk.Label(self.header_info_frame, text="Account Manager", font=Font(size=13, weight="bold"),
                                     bg=self.header_info_frame.cget("bg"), fg=self.colors["secondary"])
        self.header_title.pack(side="left", anchor="sw")

        self.header_version = tk.Label(self.header_info_frame, text=f"v.{AccountManager.version}", font=Font(size=10),
                                       bg=self.header_info_frame.cget("bg"), fg=self.colors["secondary"])
        self.header_version.pack(side="left", anchor="s")

        self.on_settings_hover = tk.BooleanVar(value=False)
        self.settings_button = tk.Button(self.header_info_frame, image=self.gui_icons["settings"], relief="flat", bd=0,
                                         bg=self.header_info_frame.cget("bg"), cursor="hand2", highlightthickness=0,
                                         activebackground=self.header_info_frame.cget("bg"))
        self.settings_button.bind("<Enter>", lambda e: self.on_settings_hover.set(True))
        self.settings_button.bind("<Leave>", lambda e: self.on_settings_hover.set(False))

        self.settings_button.pack(side="right")


        """
        self.snap_window_frame = tk.Frame(self.header_info_frame, bg=self.header_info_frame.cget("bg"))
        self.snap_window_frame.pack(side="right")

        # Handler initialized corner buttons and its actions
        self.corner_snapping_handler = CornerSnappingHandler(parent_frame=self.snap_window_frame, root=self)
        """

        self.header_search_frame = tk.Frame(self.header_frame, bg=self.header_frame.cget("bg"))
        self.header_search_frame.pack(side="bottom", fill="x", padx=8, pady=8)

        self.search_string_var = tk.StringVar()
        self.search_entry = tk.Entry(self.header_search_frame, relief="flat", textvariable=self.search_string_var,
                                     bg=self.colors["tertiary"])
        self.search_entry.pack(side="bottom", fill="x", ipady=2)
        self.search_string_var.trace_add("write", lambda name, index, mode, sv=self.search_string_var: self.on_search_update())

        """BODY"""

        # FRAME:
        self.body_frame = tk.Frame(self, width=300, height=500, bg=self.colors["secondary"])
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

        """NOTIFICATION BAR"""

        self.update()  # Update base tk window before to get current height for frame placement
        self.notification_frame = tk.Frame(self.body_frame, height=30, bg="green")
        self.notification_frame.pack_propagate(False)  # Prevent resizing through child elements
        # Notification frame only gets places when notification appears

        self.notification_text = tk.Label(self.notification_frame, text="", bg=self.notification_frame.cget("bg"), fg="white")
        self.notification_text.pack(fill="both", expand=True)

        self.extend_notification_bar = False

        """INIT CALLS"""
        self.draw()  # Display all accounts and groups
        self.animate_settings_icon()

    def draw(self):
        group_objects = {}

        # Create group frame objects for all groups
        for group_id, group_params in self.data_handler.data["groups"].items():
            group_objects[group_id] = GroupFrame(master=self.content_frame, controller=self, title=group_params["name"])

        # Create account frame objects for every account, add to group if assigned to one
        for account_id, account_params in self.data_handler.data["accounts"].items():
            # CASE: Account has group
            if account_params["group_id"] in group_objects.keys():
                group_objects[account_params["group_id"]].add_accounts(
                    AccountFrame(master=group_objects[account_params["group_id"]].content_frame, controller=self,
                                 bg=self.colors["tertiary"], account_details=account_params))

            # CASE: No group associated with account
            else:
                pass
                # TODO

        # Draw all Elements
        for group in group_objects.values():
            group.pack(padx=5, fill="x")

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

    def on_search_update(self):

        search_text = self.search_string_var.get()

        for group in self.content_frame.winfo_children():
            group.draw_accounts(regex_filter=search_text)

    def animate_settings_icon(self):
        if self.on_settings_hover.get():
            self.settings_button.configure(image=self.gui_icons["settings_hover"])
            self.after(200, lambda: self.settings_button.configure(image=self.gui_icons["settings"]))

        self.after(400, lambda: self.animate_settings_icon())


if __name__ == '__main__':
    am = AccountManager()
    am.mainloop()
