import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")




class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("test")
        self.config(bg="black")

        self.theme = {"bg_main": "#1A1824", "bg_sec": "#0D0C13", "accent": "#6549BD", "accent_high": "#855DFF"}

        self.header_frm = ctk.CTkFrame(self, bg_color=self.theme["bg_main"], fg_color=self.theme["bg_main"])
        self.header_frm.pack(side="top", fill="x")

        self.content_frm = ctk.CTkFrame(self, bg_color=self.theme["bg_sec"], fg_color=self.theme["bg_sec"])
        self.content_frm.pack(side="top", fill="both", padx=4, expand=True)

        self.footer_frm = ctk.CTkFrame(self, bg_color=self.cget("bg"), height=40)
        self.footer_frm.pack(side="bottom", fill="x", padx=4, pady=4)

        self.test_btn = ctk.CTkButton(self.header_frm, text="test", cursor="hand2", fg_color=self.theme["accent"])
        self.test_btn.pack(padx=4, pady=4)


if __name__ == '__main__':
    app = App()
    app.mainloop()

