import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # General
        self.title("Account Manager")

        """HEADER"""

        self.header_frame = tk.Frame(self)
        self.header_frame.grid(row=0, column=0)

        self.title_label = tk.Label(self.header_frame, text="Account Manager")
        self.title_label.grid(row=0, column=0, columnspan=2)

        self.search_box = tk.Entry(self.header_frame)
        self.search_box.grid(row=1, column=0)

        self.search_button = tk.Button(self.header_frame, text="search")
        self.search_button.grid(row=1, column=1)

        """CONTENT"""

        self.content_frame = tk.Frame(self)
        self.content_frame.grid(row=2, column=0)

        """FOOTER"""

        self.footer_frame = tk.Frame(self)
        self.footer_frame.grid(row=2, column=0)

        self.add_account_button = tk.Button(self.footer_frame, text="Add new Account")
        self.add_account_button.grid(row=0, column=0)


if __name__ == "__main__":
    app = App()
    app.mainloop()
