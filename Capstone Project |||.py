# This is example of Python program.
# it stores user and their task and show it using ktinter

import tkinter as tk
from tkinter import messagebox


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x500")
        self.title("Task Manager")
        self.resizable(0, 0)
        self['background'] = '#EBEBEB'

        self.all_users = {}
        self.logged_in_user = None

        self.get_users_list()
        LoginPage().pack()

    def get_users_list(self):
        with open('user.txt', "r") as file:
            data = file.readlines()
            for line in data:
                accounts = line.strip("\n", ).strip("").split(",")
                self.all_users[accounts[0].strip()] = accounts[1].strip()
            print(self.all_users)


class MainPage(tk.Frame):
    def __init__(self):
        super(MainPage, self).__init__()
        self.background = self.master["background"]
        self.label1 = tk.Label(self, text=f"Main page{self.master.logged_in_user}", bg=self.background)
        self.label1.pack(pady=20)
        self.button = tk.Button(self, text="G0 to 2", bg=self.background, command=lambda: self.show_frame(MainPage))
        self.button.pack()
        self.button = tk.Button(self, text="G0 to statistic", bg=self.background,
                                command=lambda: self.show_frame(StatisticPage))
        self.button.pack()

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
        page_name().pack()

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
