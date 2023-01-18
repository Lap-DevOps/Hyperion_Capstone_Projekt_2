# This is example of Python program.
# it stores user and their task and show it using ktinter

import tkinter as tk
from tkinter import font as tkfont


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.users = {}
        self.title("Task Manager")
        self.geometry("700x500")
        self.resizable(0, 0)
        self.title_font = tkfont.Font(family='Helvetica', size=33, weight="bold", slant="italic")
        self.get_users_list()
        self.create_widgets()

    def create_widgets(self):
        """ store frames(windows)  """
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, LogIn_Page, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LogIn_Page")

    def show_frame(self, page_name):
        """ Show a frame for the given page name """
        frame = self.frames[page_name]
        frame.tkraise()

    def get_users_list(self):
        with open('user.txt', "r") as file:
            data = file.readlines()
            for line in data:
                a = line.strip("\n")
                accounts = line.strip("\n", ).strip("").split(",")
                self.users[accounts[0].strip()] = accounts[1].strip()
            print(self.users)


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=100)

        button1 = tk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("LogIn_Page"))
        button2 = tk.Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame("PageTwo"))
        button1.pack()
        button2.pack()


class LogIn_Page(tk.Frame):

    def __init__(self, parent, controller):
        self.login_user = None
        tk.Frame.__init__(self, parent),
        self.controller = controller
        self.configure(bg="#303841")
        self.users = self.controller.users
        self.center_frame = tk.Frame(self, bg="#303841")
        self.login_label = tk.Label(self.center_frame, text="Login", background="#303841", fg="#f3a556",
                                    font=controller.title_font)
        self.username_label = tk.Label(self.center_frame, text="Username", background="#303841", fg="#FFFFFF",
                                       font=('Helvetica', 16))
        self.username_entry = tk.Entry(self.center_frame, font=('Helvetica', 16))
        self.password_entry = tk.Entry(self.center_frame, show="*", font=('Helvetica', 16))
        self.password_label = tk.Label(self.center_frame, text="Password", background="#303841", fg="#FFFFFF",
                                       font=('Helvetica', 16))
        self.login_button = tk.Button(self.center_frame, text="Login", background="#303841",
                                      font=('Helvetica', 20), command=self.log_in_user)
        self.login_label.grid(row=0, column=0, columnspan=2, pady=40)
        self.username_label.grid(row=1, column=0, sticky="news")
        self.username_entry.grid(row=1, column=1, pady=20, padx=20)
        self.password_label.grid(row=2, column=0, )
        self.password_entry.grid(row=2, column=1, )
        self.login_button.grid(row=3, column=0, columnspan=2, pady=30)
        self.center_frame.pack()

    def log_in_user(self):
        try:
            if self.username_entry.get().lower() in self.users and \
                    self.password_entry.get() == self.users[self.username_entry.get().lower()]:
                login_state = "Login successful !"
                self.login_user = self.username_entry.get()
                win = Top_Level_Window(self, login_state, controller=self.controller)
                win.grab_set()
            else:
                self.bell()
                login_state = "Login incorrect !"
                win = Top_Level_Window(self, login_state, controller=self.controller)
                win.grab_set()
        except KeyError:
            print("User dont exist.")
            pass


class Top_Level_Window(tk.Toplevel):
    def __init__(self, parent, login_state, controller, ):
        super(Top_Level_Window, self).__init__(parent)
        self.controller = controller
        self.login_state = login_state
        self.configure(bg="#303841")
        self.geometry("200x150")
        self.resizable(0, 0)
        self.title(login_state)
        if login_state == "Login successful !":
            label = tk.Label(self, text="You successfully login", background="#303841", fg="#FFFFFF",
                             font=('Helvetica', 16))
            label2 = tk.Label(self, text=" into system !", background="#303841", fg="#FFFFFF",
                              font=('Helvetica', 16))
            button = tk.Button(self, text="OK", font=('Helvetica', 16), command=self.destroy)
            label.pack(pady=10)
            label2.pack(pady=0)
            button.pack(pady=20)
            controller.show_frame("PageTwo")
        elif login_state == 'Login incorrect !':
            label = tk.Label(self, text="Username or", background="#303841", fg="#e63d09",
                             font=('Helvetica', 16))
            label2 = tk.Label(self, text=" Password incorrect !", background="#303841", fg="#e63d09",
                              font=('Helvetica', 16))
            button = tk.Button(self, text="Close", font=('Helvetica', 16), command=self.destroy)
            label.pack(pady=10)
            label2.pack(pady=0, padx=20)
            button.pack(pady=20)
            # button.after(3000, self.destroy())


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == '__main__':
    app = App()
    app.mainloop()
