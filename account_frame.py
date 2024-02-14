import tkinter as tk
from PIL import ImageTk, Image
from tkinter.font import Font
from tooltip import create_tool_tip


class AccountFrame(tk.Frame):

    default_account_logo_path = "./icons/default_logo.png"
    unknowm_attribute_logo_path = "./icons/unknown_attribute.png"
    password_logo_path = "./icons/password.png"

    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = controller
        self.configure()

        self.account_logo = ImageTk.PhotoImage(Image.open(AccountFrame.default_account_logo_path))
        self.unknowm_attribute_logo = ImageTk.PhotoImage(Image.open(AccountFrame.unknowm_attribute_logo_path))

        """UPPER LEVEL FRAMES"""

        self.image_frame = tk.Frame(self, bg=self.cget("bg"))
        self.image_frame.pack(side="left", fill="y", padx=5, pady=5)

        self.info_frame = tk.Frame(self, bg=self.cget("bg"))
        self.info_frame.pack(side="left", fill="both", expand=True, pady=5)

        self.expand_frame = tk.Frame(self, bg="light grey", width=50)
        self.expand_frame.pack(side="left", fill="y", padx=5, pady=5)

        """IMAGE FRAME"""

        self.image_label = tk.Label(self.image_frame, image=self.account_logo, bg=self.image_frame.cget("bg"))
        self.image_label.pack()

        """INFO FRAME"""

        self.title_label = tk.Label(self.info_frame, text="Example Account", bg=self.info_frame.cget("bg"),
                                    font=Font(size=11), anchor="w")
        self.title_label.pack(fill="x")

        self.data_frame = tk.Frame(self.info_frame, bg=self.info_frame.cget("bg"))
        self.data_frame.pack(fill="x")

        self.add_attribute("email", "examplemail@lol.com")
        self.add_attribute("password", "asdp12apsdja2")
        self.add_attribute("name", "test name")


    def add_attribute(self, attribute, value):
        frame_bg = self.data_frame.cget("bg")
        new_attribute_frame = tk.Frame(self.data_frame, bg=frame_bg)

        if attribute in self.controller.attribute_imgs.keys():
            attribute_logo = self.controller.attribute_imgs[attribute]
        else:
            attribute_logo = self.unknowm_attribute_logo

        attribute_logo = tk.Label(new_attribute_frame, image=attribute_logo, bg=frame_bg)
        attribute_logo.pack(side="left")
        create_tool_tip(attribute_logo, attribute)

        attribute_value = tk.Label(new_attribute_frame, text=value, bg=frame_bg, font=Font(size=10))
        attribute_value.pack(side="left")

        copy_button = tk.Button(new_attribute_frame, text="COPY", command=lambda: print(value), bd=0)
        copy_button.pack(side="left")

        new_attribute_frame.pack(fill="x")

