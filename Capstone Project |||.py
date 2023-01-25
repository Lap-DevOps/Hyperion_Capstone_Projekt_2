# This is example of Python program.
# it stores user and their task and show it using ktinter

import tkinter as tk
from tkinter import messagebox, ttk


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
        View_Tasks().place(height=500, width=700)

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
        tk.Button(self.scd_frame, text="Register new user", command=lambda: self.show_frame(AddUserForm)).place(x=225,
                                                                                                                y=0,
                                                                                                                width=250,
                                                                                                                height=50)
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
        if str(page_name) == "<class '__main__.AddUserForm'>" and str(self.master.logged_in_user).lower() != 'admin':
            messagebox.showerror(title="Error", message="You don't have right to do this !")
            self.bell()
        else:
            self.destroy()
            page_name().place(height=500, width=700)


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
        self.login_label.grid(row=0, column=0, columnspan=2, pady=40, padx=100)
        self.username_label.grid(row=1, column=0, padx=100)
        self.username_entry.grid(row=1, column=1, pady=20, padx=100)
        self.password_label.grid(row=2, column=0, padx=100)
        self.password_entry.grid(row=2, column=1, padx=100)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=30, padx=100)
        self.center_frame.place(x=0, y=0, height=500, width=700)

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


class AddUserForm(tk.Frame):
    def __init__(self):
        super(AddUserForm, self).__init__()
        self.background = self.master["background"]
        self.font = ('Helvetica', 16)

        self.main_frame = tk.LabelFrame(self, bg=self.background)
        self.main_frame.place(x=10, y=10)
        self.user_frame = tk.LabelFrame(self.main_frame, bg=self.background, )
        self.user_name_label = tk.Label(self.main_frame, text=f"Register new User:",
                                        bg=self.background, font=('Helvetica', 20, "bold"))
        self.log_out_btn = tk.Button(self.main_frame, text="Log out", command=lambda: self.show_frame(LoginPage),
                                     bg=self.background, )
        self.user_name_label.place(x=220, y=10, width=250, height=20)
        self.log_out_btn.place(x=550, y=10, width=100, height=20)
        self.main_frame.place(height=50, width=680, )
        self.scd_frame = tk.LabelFrame(self, text="Add user:", bg=self.background)
        self.scd_frame.place(x=10, y=60, width=680, height=430)

        self.username_label = tk.Label(self.scd_frame, text="Username", background=self.background,
                                       font=self.font)
        self.username_label.place(x=150, y=50)
        self.username_entry = tk.Entry(self.scd_frame, font=self.font)
        self.username_entry.place(x=300, y=50)
        self.password_entry = tk.Entry(self.scd_frame, font=self.font)
        self.password_entry.place(x=300, y=100)
        self.password_label = tk.Label(self.scd_frame, text="Password", background=self.background,
                                       font=self.font).place(x=150, y=100)
        self.password_label2 = tk.Label(self.scd_frame, text="Repeat Password", background=self.background,
                                        font=self.font).place(x=150, y=150)
        self.password_entry2 = tk.Entry(self.scd_frame, font=self.font)
        self.password_entry2.place(x=300, y=150)

        self.subit_button = tk.Button(self.scd_frame, text="Submit",
                                      font=('Helvetica', 20), command=self.reg_user).place(x=325, y=250)

    def reg_user(self):
        try:
            if self.username_entry.get().lower() in self.master.all_users:
                self.bell()
                messagebox.showerror(title="Error", message="Username exist !")
            elif self.username_entry.get() == "" or self.password_entry.get() == "" or self.password_entry2.get() == "":
                self.bell()
                messagebox.showerror(title="Error", message="Username or Password can't be empty!")
            elif self.password_entry.get() != self.password_entry2.get():
                self.bell()
                messagebox.showerror(title="Error", message="Incorrect Password !")
            else:
                with open("user.txt", "a") as file:
                    new_user = (self.username_entry.get().lower() + "," + self.password_entry.get().lower() + "\n")
                    file.write(new_user)
                    messagebox.showerror(title="Susses", message="User added !")
                    self.show_frame(MainPage)

        except KeyError:
            pass

    def show_frame(self, page_name):
        self.destroy()
        page_name().place(height=500, width=700)


class View_Tasks(tk.Frame):
    def __init__(self):
        super(View_Tasks, self).__init__()
        self.background = self.master["background"]
        self.font = ('Helvetica', 16)

        self.main_frame = tk.LabelFrame(self, bg=self.background)
        self.main_frame.place(x=10, y=10)
        self.user_frame = tk.LabelFrame(self.main_frame, bg=self.background, )

        self.user_name_label = tk.Label(self.main_frame, text=f"View all Users tasks:",
                                        bg=self.background, font=('Helvetica', 20, "bold"))
        self.log_out_btn = tk.Button(self.main_frame, text="Log out", command=lambda: self.show_frame(LoginPage),
                                     bg=self.background, )
        self.user_name_label.place(x=220, y=10, width=250, height=20)
        self.log_out_btn.place(x=550, y=10, width=100, height=20)
        self.main_frame.place(height=50, width=680, )

        self.scd_frame = tk.LabelFrame(self, text="Tasks:", bg=self.background)
        self.scd_frame.place(x=10, y=60, width=680, height=430)

        self.thrd_frame = tk.LabelFrame(self, bg=self.background, ).place(x=10, y=80, width=680, height=30)
        self.lbl_user = tk.Label(self.thrd_frame, text='User').place(x=17, y=85, width=47, height=20)
        self.lbl = tk.Label(self.thrd_frame, text='Task title').place(x=67, y=85, width=105, height=20)
        self.lbl3 = tk.Label(self.thrd_frame, text='Task description').place(x=175, y=85, width=205, height=20)
        self.lbl5 = tk.Label(self.thrd_frame, text='Start date').place(x=385, y=85, width=95, height=20)
        self.lbl6 = tk.Label(self.thrd_frame, text='End date').place(x=485, y=85, width=95, height=20)
        self.lbl7 = tk.Label(self.thrd_frame, text='Done ?').place(x=590, y=85, width=45, height=20)

        self.forth_frame = tk.LabelFrame(self, bg=self.background)
        self.forth_frame.place(x=10, y=115, width=680, height=350)

        self.canvas = tk.Canvas(self.forth_frame, background=self.background)
        self.scroll_bar = ttk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_bar.set)

        with open("tasks.txt", "r") as file:
            self.data = file.readlines()
            for x in self.data:
                task = x.split(",")
                frame = Task_Frame(self.scrollable_frame, task=task)
                frame.pack()

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_bar.pack(side="right", fill="y")
        # self.scrollable_frame.pack(side="left", fill="both", expand=True)

        # self.submit_button = tk.Button(self.main_frame, text="Submit",
        #                                font=('Helvetica', 20), ).place(x=25, y=350)

    def show_frame(self, page_name):
        self.destroy()
        page_name().place(height=500, width=700)


class Task_Frame(tk.Frame):
    def __init__(self, parent, task=None):
        tk.Frame.__init__(self, parent, )
        self.background = '#EBEBEB'
        self.task = task
        self.task_frame = tk.LabelFrame(self, text=f"Task #{task[0]} ", width=650, height=100)
        self.task_frame.pack()
        self.lbl_user = tk.Label(self.task_frame, text=f"{task[1]}", justify=tk.LEFT, bg=self.background,
                                 height=4)
        self.lbl_user.place(x=1, y=0)
        self.lbl_user = tk.Label(self.task_frame, text=f"{task[1]}", justify=tk.LEFT, bg=self.background,
                                 height=4)
        self.lbl_user.place(x=1, y=0)
        self.lbl_title = tk.Label(self.task_frame, text=f"{task[2]}", width=11,
                                  height=4, justify=tk.LEFT, wraplength=100, bg=self.background)
        self.lbl_title.place(x=50, y=0)
        self.lbl_task = tk.Label(self.task_frame, text=f"{task[3]}", width=22,
                                 height=4, justify=tk.LEFT, wraplength=200, bg=self.background)
        self.lbl_task.place(x=160, y=0)
        self.lbl_s_date = tk.Label(self.task_frame, text=f"{task[4]}", width=10,
                                   height=4, justify=tk.LEFT, wraplength=200, bg=self.background)
        self.lbl_s_date.place(x=368, y=0)
        self.lbl_end_date = tk.Label(self.task_frame, text=f"{task[5]}", width=10,
                                     height=4, justify=tk.LEFT, wraplength=200, bg=self.background)
        self.lbl_end_date.place(x=469, y=0)
        self.edit_button = tk.Button(self.task_frame, text="Edit", command=lambda: print(self.task[0]))
        self.edit_button.place(x=600, y=0)
        self.confirm_button = tk.Button(self.task_frame, text="Done", command=lambda: self.mark_task_done(task[0]))
        self.confirm_button.place(x=600, y=25)
        self.del_button = tk.Button(self.task_frame, text="Delt", command=lambda: print(self.task[0]))
        self.del_button.place(x=600, y=50)
        if str(task[6]).strip() == "Yes":
            self.fin_lbl = tk.Label(self.task_frame, text='+', background='green')
        else:
            self.fin_lbl = tk.Label(self.task_frame, text='-', background='red')
        self.fin_lbl.place(x=575, y=25)

        self.pack()

    def mark_task_done(self, task):
        # print(task)
        answer = messagebox.askokcancel(title="Confirm", message="Confirm task fulfilment ? !")
        if answer:
            with open("tasks.txt", "r") as file:
                lines = file.readlines()
                print(lines)
                print(type(lines[0]))
                # for x in lines:
                #     line = x.split(",")
                #     if line[6] == "Yes\n":
                #         line[6] = "Yes"
                #     elif line[6] == "No\n":
                #          line[6] = "No"
                #     elif line[0] == task[0]:
                #         # print(line)
                #         line[6] = "Yes\n"
                        # if line[6] == "Yes\n":
                        #     line[6] = "Yes"
                        # elif line[6] == "No\n":
                        #     line[6] = "No"
                        # print(line)
                #         text = ",".join(line)
                #         print(text)
                #         print(type(text))
                #     lines[int(task) - 1] = ",".join(line)
                # # lines[x] = ",".join(line)
                # print(lines)
                #         print(line)
                #
                #         zxzx = ",".join(line)
                #         print(zxzx)
                #         lines[int(task) - 1] = ",".join(line)
                #         print(lines)
                # str(lines).replace('\n','')
                # lines= "\n".join(str(lines))
                # print(lines)
                # print(type(lines))
                # file.write(str(lines).split("\n"))


if __name__ == '__main__':
    app = App()
    app.mainloop()
