import tkinter as tk
from account_frame import AccountFrame
from PIL import ImageTk, Image


class AccountManager(tk.Tk):

    attribute_logo_paths = {
        "password": "./icons/password.png",
        "email": "./icons/email.png"
    }

    def __init__(self):
        super().__init__()

        self.title("Account Manager")
        self.configure(bg="white")

        self.attribute_imgs = {}
        for attribute, img_path in AccountManager.attribute_logo_paths.items():
            self.attribute_imgs[attribute] = ImageTk.PhotoImage(Image.open(img_path))


        self.test_frame = AccountFrame(self, bg="#ace3d4")
        self.test_frame.pack(padx=5, pady=5, fill="x")


if __name__ == '__main__':
    am = AccountManager()
    am.mainloop()
