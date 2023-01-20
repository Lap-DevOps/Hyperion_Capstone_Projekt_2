# This is example of Python program.
# it stores user and their task and show it using ktinter

import tkinter as tk
from tkinter import messagebox


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("700x500")

        self.title("Task Manager")
        self.resizable(0, 0)
        self['background'] = '#EBEBEB'

        self.all_users = {}
        self.logged_in_user = None

        self.get_users_list()
        MainPage().place(height=500, width=700)


    def get_users_list(self):
        with open('user.txt', "r") as file:
            data = file.readlines()
            for line in data:
                accounts = line.strip("\n", ).strip("").split(",")
                self.all_users[accounts[0].strip()] = accounts[1].strip()



class MainPage(tk.Frame):
    def __init__(self):
        super(MainPage, self).__init__()
        self.background = self.master["background"]


        self.main_frame = tk.LabelFrame(self, bg=self.background)
        self.main_frame.place(x=10, y=10)
        self.user_frame = tk.LabelFrame(self.main_frame, bg=self.background, )
        self.user_name_label = tk.Label(self.main_frame, text=f"Welcome {str(self.master.logged_in_user).title()} !",
                                        bg=self.background, font=('Helvetica', 20, "bold"))
        self.log_out_btn = tk.Button(self.main_frame, text="Log out", command=lambda: self.show_frame(LoginPage),
                                     bg=self.background, )
        self.user_name_label.place(x=260, y=10, width=170, height=20)
        self.log_out_btn.place(x=550, y=10, width=100, height=20)
        self.main_frame.place(height=50, width=680, )

        self.scd_frame = tk.LabelFrame(self, text="MENU:", bg=self.background)
        self.scd_frame.place(x=10, y=60, width=680, height=430)
        tk.Button(self.scd_frame, text="Register new user").place(x=225, y=0, width=250, height=50)
        tk.Button(self.scd_frame, text="Add new task").place(x=225, y=60, width=250,
                                                             height=50)
        tk.Button(self.scd_frame, text="View all tasks").place(x=225, y=120, width=250,
                                                               height=50)
        tk.Button(self.scd_frame, text="View my tasks").place(x=225, y=180, width=250,
                                                              height=50)
        tk.Button(self.scd_frame, text="Generate reports").place(x=225, y=240, width=250,
                                                                 height=50)
        if str(self.master.logged_in_user).lower() == "admin":
            tk.Button(self.scd_frame, text="Display statistic").place(x=225, y=300, width=250,
                                                                      height=50)
        tk.Button(self.scd_frame, text="Exit", command=self.master.destroy).place(x=225, y=360,
                                                                                  width=250,
                                                                                  height=50, )


    def show_frame(self, page_name):
        self.destroy()
        page_name().pack()


class LoginPage(tk.Frame):
    def __init__(self, ):
        super(LoginPage, self).__init__()
        self.background = self.master["background"]
        self.font = ('Helvetica', 16)
        self.all_users = self.master.all_users
        self.center_frame = tk.LabelFrame(self, bg=self.background)
        self.login_label = tk.Label(self.center_frame, text="Login", background=self.background,
                                    font=('Helvetica', 30))
        self.username_label = tk.Label(self.center_frame, text="Username", background=self.background,
                                       font=self.font)
        self.username_entry = tk.Entry(self.center_frame, font=self.font)
        self.password_entry = tk.Entry(self.center_frame, show="*", font=self.font)
        self.password_label = tk.Label(self.center_frame, text="Password", background=self.background,
                                       font=self.font)
        self.login_button = tk.Button(self.center_frame, text="Login", background="#303841",
                                      font=('Helvetica', 20), command=lambda: self.log_in_user())
        self.login_label.grid(row=0, column=0, columnspan=2, pady=40)
        self.username_label.grid(row=1, column=0, )
        self.username_entry.grid(row=1, column=1, pady=20, padx=20)
        self.password_label.grid(row=2, column=0, )
        self.password_entry.grid(row=2, column=1, )
        self.login_button.grid(row=3, column=0, columnspan=2, pady=30)
        self.center_frame.pack(side='bottom')

    def show_frame(self, page_name):
        self.destroy()

        page_name().place(height=500, width=700)

    def log_in_user(self):
        try:
            if self.username_entry.get().lower() in self.all_users and \
                    self.password_entry.get() == self.all_users[self.username_entry.get().lower()]:
                self.master.logged_in_user = self.username_entry.get()
                self.show_frame(MainPage)
            else:
                self.bell()
                messagebox.showerror(title="Error", message="Username or Password incorrect !")

        except KeyError:
            pass


class StatisticPage(tk.Frame):
    def __init__(self):
        super(StatisticPage, self).__init__()
        self.background = self.master["background"]
        self.lablel1 = tk.Label(self, text="Statistic page", bg=self.background)
        self.lablel1.pack(pady=20)
        self.button = tk.Button(self, text="G0 to main", bg=self.background, command=lambda: self.show_frame(MainPage))
        self.button.pack()
        self.button = tk.Button(self, text="G0 to login", bg=self.background,
                                command=lambda: self.show_frame(LoginPage))
        self.button.pack()

    def show_frame(self, page_name):
        self.destroy()
        page_name().pack()


if __name__ == '__main__':
    app = App()
    app.mainloop()
