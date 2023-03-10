# This is example of Python program.
# it stores user and their task and show it using ktinter

import tkinter as tk
from datetime import datetime
from random import randrange
from tkinter import messagebox, ttk

from tkcalendar import DateEntry


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set the window size and background color
        self.geometry("700x500")
        self.title("Task Manager")
        self.resizable(0, 0)
        self['background'] = '#EBEBEB'

        # Create a dictionary to store all the registered users and set the current user to None
        self.all_users = {}
        self.logged_in_user = None

        # Call the function to get the list of all registered users from user.txt file
        self.get_users_list()

        # Create a login page object and place it in the window
        LoginPage().place(height=500, width=700)

    def get_users_list(self):
        # Open the user.txt file and read its contents
        with open('user.txt', "r") as file:
            data = file.readlines()
            # Iterate over each line in the file and add the user to the dictionary
            for line in data:
                accounts = line.strip("\n", ).strip("").split(",")
                self.all_users[accounts[0].strip()] = accounts[1].strip()


class MainPage(tk.Frame):
    def __init__(self):
        super(MainPage, self).__init__()

        # Set background color
        self.background = self.master["background"]

        # Create main frame
        self.main_frame = tk.LabelFrame(self, bg=self.background)
        self.main_frame.place(x=10, y=10)

        # Create user frame and display user name
        self.user_frame = tk.LabelFrame(self.main_frame, bg=self.background)
        self.user_name_label = tk.Label(self.main_frame, text=f"Welcome {str(self.master.logged_in_user).title()} !",
                                        bg=self.background, font=('Helvetica', 20, "bold"))
        # Create log out button
        self.log_out_btn = tk.Button(self.main_frame, text="Log out", command=lambda: self.show_frame(LoginPage),
                                     bg=self.background)
        # Place user name label and log out button
        self.user_name_label.place(x=260, y=10, width=170, height=20)
        self.log_out_btn.place(x=550, y=10, width=100, height=20)
        self.main_frame.place(height=50, width=680)

        # Create second frame and buttons
        self.scd_frame = tk.LabelFrame(self, text="MENU:", bg=self.background)
        self.scd_frame.place(x=10, y=60, width=680, height=430)
        tk.Button(self.scd_frame, text="Register new user", command=lambda: self.show_frame(AddUserForm)).place(x=225,
                                                                                                                y=0,
                                                                                                                width=250,
                                                                                                                height=50)
        tk.Button(self.scd_frame, text="Add new task", command=lambda: self.show_frame(Add_Task, )).place(x=225, y=60,
                                                                                                          width=250,
                                                                                                          height=50)
        tk.Button(self.scd_frame, text="View all tasks", command=lambda: self.show_frame(View_Tasks)).place(x=225,
                                                                                                            y=120,
                                                                                                            width=250,
                                                                                                            height=50)
        tk.Button(self.scd_frame, text="View my tasks", command=lambda: self.show_frame(View_My_Tasks)).place(x=225,
                                                                                                              y=180,
                                                                                                              width=250,
                                                                                                              height=50)

        # Create statistic button if user is an admin
        if str(self.master.logged_in_user).lower() == "admin":
            tk.Button(self.scd_frame, text="Display statistic", command=lambda: self.show_frame(StatisticPage)).place(
                x=225, y=300, width=250, height=50)

        # Create exit button
        tk.Button(self.scd_frame, text="Exit", command=self.master.destroy).place(x=225, y=360,
                                                                                  width=250,
                                                                                  height=50)

    def show_frame(self, page_name):
        # Check if user has permission to access the page
        if str(page_name) == "<class '__main__.AddUserForm'>" and str(self.master.logged_in_user).lower() != 'admin':
            # Display error message and ring bell
            messagebox.showerror(title="Error", message="You don't have right to do this !")
            self.bell()
        else:
            # Destroy current page and display new page
            self.destroy()
            page_name().place(height=500, width=700)


class LoginPage(tk.Frame):
    def __init__(self):
        super(LoginPage, self).__init__()
        self.background = self.master["background"]
        self.font = ('Helvetica', 16)
        self.all_users = self.master.all_users

        # create login form widgets
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

        # place login form widgets
        self.login_label.grid(row=0, column=0, columnspan=2, pady=40, padx=100)
        self.username_label.grid(row=1, column=0, padx=100)
        self.username_entry.grid(row=1, column=1, pady=20, padx=100)
        self.password_label.grid(row=2, column=0, padx=100)
        self.password_entry.grid(row=2, column=1, padx=100)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=30, padx=100)
        self.center_frame.place(x=0, y=0, height=500, width=700)

    def show_frame(self, page_name):
        # destroy current frame and show new frame
        self.destroy()
        page_name().place(height=500, width=700)

    def log_in_user(self):
        try:
            if self.username_entry.get().lower() in self.all_users and \
                    self.password_entry.get() == self.all_users[self.username_entry.get().lower()]:
                # set logged in user and show main page
                self.master.logged_in_user = self.username_entry.get()
                self.show_frame(MainPage)
            else:
                # show error message and bell if login fails
                self.bell()
                messagebox.showerror(title="Error", message="Username or Password incorrect !")

        except KeyError:
            # do nothing if KeyError occurs
            pass


class StatisticPage(tk.Frame):
    def __init__(self):
        super(StatisticPage, self).__init__()
        # Store the background color of the parent widget
        self.background = self.master["background"]
        # Initialize the number of tasks to 0
        self.tasks_amount = 0

        # Create a main frame and place it at the top-left corner of the window
        self.main_frame = tk.LabelFrame(self, bg=self.background)
        self.main_frame.place(x=10, y=10)

        # Create a user frame inside the main frame and set its background color
        self.user_frame = tk.LabelFrame(self.main_frame, bg=self.background)

        # Create a label for the user name and set its text, font, and background color
        self.user_name_label = tk.Label(self.main_frame, text=f"Statistic of Users:", bg=self.background,
                                        font=('Helvetica', 20, "bold"))

        # Create a logout button and set its text, command, and background color
        self.log_out_btn = tk.Button(self.main_frame, text="Log out", command=lambda: self.show_frame(LoginPage),
                                     bg=self.background)

        # Create a main menu button and set its text, command, and background color
        self.main_meny_btn = tk.Button(self.main_frame, text="Main page", command=lambda: self.show_frame(MainPage),
                                       bg=self.background)

        # Place the user name label, logout button, and main menu button
        self.user_name_label.place(x=220, y=10, width=250, height=20)
        self.log_out_btn.place(x=550, y=2, width=100, height=20)
        self.main_meny_btn.place(x=550, y=25, width=100, height=20)

        # Set the size of the main frame
        self.main_frame.place(height=50, width=680)

        # Create a second frame for the statistics and set its background color
        self.scd_frame = tk.LabelFrame(self, text="Statistic:", bg=self.background)

        # Place the second frame below the main frame
        self.scd_frame.place(x=10, y=60, width=680, height=430)

        # Create a fourth frame and set its background color
        self.forth_frame = tk.LabelFrame(self, bg=self.background)

        # Place the fourth frame below the user frame
        self.forth_frame.place(x=10, y=115, width=680, height=350)

        # Create a canvas and set its background color
        self.canvas = tk.Canvas(self.forth_frame, background=self.background)

        # Create a scrollbar and set its orientation and command
        self.scroll_bar = ttk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)

        # Create a scrollable frame and bind it to the canvas
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Create a window inside the canvas for the scrollable frame
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Set the scrollbar command to the canvas yview
        self.canvas.configure(yscrollcommand=self.scroll_bar.set)

        # Open the 'tasks.txt' file in read mode and store its contents in 'self.data'
        with open("tasks.txt", "r") as file:
            self.data = file.readlines()

            # Initialize an empty dictionary to store statistics
            self.statistic = {}

            # Loop through each line in 'self.data'
            for x in self.data:
                # Split each line by comma and store the result in 'task'
                task = x.split(",")

                # Increment 'self.tasks_amount' by 1
                self.tasks_amount += 1

                # If the task's category is not already in the 'self.statistic' dictionary:
                if task[1] not in self.statistic:
                    # Add the category to the dictionary with a list of counts for tasks, completed tasks, incomplete tasks, and overdue tasks
                    self.statistic[task[1]] = [1, 0, 0, 0]

                    # If the task is marked as completed:
                    if task[6].strip().lower() == 'yes':
                        # Increment the count of completed tasks for the category
                        self.statistic[task[1]][1] += 1
                    else:
                        # Otherwise, increment the count of incomplete tasks for the category
                        self.statistic[task[1]][2] += 1

                        # If the task is overdue, increment the count of overdue tasks for the category
                        if datetime.now().strftime("%d %b %Y") > task[5]:
                            self.statistic[task[1]][3] += 1

                # If the task's category is already in the 'self.statistic' dictionary:
                else:
                    # Increment the count of tasks for the category
                    self.statistic[task[1]][0] += 1

                    # If the task is marked as completed:
                    if task[6].strip().lower() == 'yes':
                        # Increment the count of completed tasks for the category
                        self.statistic[task[1]][1] += 1
                    else:
                        # Otherwise, increment the count of incomplete tasks for the category
                        self.statistic[task[1]][2] += 1

            # Loop through each category and its statistics in the 'self.statistic' dictionary
            for user, stat in self.statistic.items():
                frame = StatisticFrame(self.scrollable_frame, stat=stat, user=user, total=self.tasks_amount)
                frame.pack()
        self.tasks_amount_lbl = tk.Label(self.scd_frame, text=f"Total tasks: {self.tasks_amount}")
        self.tasks_amount_lbl.place(x=20, y=5)
        self.report_btb = tk.Button(self.scd_frame, text="Generate reports", command=lambda: self.gen_reports())
        self.report_btb.place(y=5, x=500)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_bar.pack(side="right", fill="y")

    def gen_reports(self):
        StatisticPage()
        with open("user_overview.txt", "w") as file:
            print("Users statistic overview !", file=file)
            print(file=file)
            for user in self.statistic.items():
                print(f"Statistic for user:                     {str(user[0]).title()}.  ", file=file)
                print(f"Total number of tasks:                  {user[1][0]}", file=file)
                print(f"Finished tasks:                         {user[1][1]}", file=file)
                print(f"Not finished tasks:                     {user[1][2]}", file=file)
                print(
                    f"Percentage of total tasks:              {round((user[1][0] / int(self.tasks_amount) * 100), 2)} %",
                    file=file)
                print(f"Percentage of completed tasks:          {round((user[1][1] / user[1][0] * 100), 2)} %",
                      file=file)
                print(f"Percentage of not completed tasks:      {round((user[1][2] / user[1][0] * 100), 2)} %",
                      file=file)
                print(f"Percentage of overdue tasks:            {round((user[1][3] / user[1][0] * 100), 2)} %",
                      file=file)
                print("", file=file)
                print("----------------------------------------------------------------", file=file)
                print("", file=file)

        with open("task_overview.txt", "w") as file:
            print("Tasks statistic overview !", file=file)
            print(file=file)
            print('----------------------------------------------------', file=file)
            print(f"The total number of  tasks:                          {self.tasks_amount}", file=file)
            print(
                f"The total number of completed tasks:                 {(sum(x[1] for x in list(self.statistic.values())))}",
                file=file)
            print(
                f"The total number of uncompleted tasks                {(sum(x[2] for x in list(self.statistic.values())))}",
                file=file)
            print(
                f"The total number of overdue tasks                    {(sum(x[3] for x in list(self.statistic.values())))}",
                file=file)
            print(
                f"The percentage of tasks that are incomplete          {round(((sum(x[2] for x in list(self.statistic.values()))) / (sum(x[0] for x in list(self.statistic.values()))) * 100), 2)} %",
                file=file)
            print(
                f"The percentage of tasks that are overdue.            {round(((sum(x[3] for x in list(self.statistic.values()))) / (sum(x[0] for x in list(self.statistic.values()))) * 100), 2)} %",
                file=file)
            print()
            print('----------------------------------------------------', file=file)

    def show_frame(self, page_name):
        self.destroy()
        page_name().place(height=500, width=700)


class StatisticFrame(tk.Frame):
    def __init__(self, parent, stat=None, user=None, total=None):
        tk.Frame.__init__(self, parent, )
        self.user = user
        self.stat = stat
        self.tasks_amount = total
        self.stat_frame = tk.LabelFrame(self, text=f"User: {str(self.user).title()} ", width=650, height=250)
        self.stat_frame.pack()
        self.user_lbl = tk.Label(self.stat_frame, text="User name:", width=21, anchor="w", background="#EBEBEB")
        self.user_lbl.place(x=150, y=10)
        self.user_all_tasks = tk.Label(self.stat_frame, text="Total number of tasks:", width=21, anchor="w",
                                       background="#EBEBEB")
        self.user_all_tasks.place(x=150, y=35)
        self.user_fin_tasks = tk.Label(self.stat_frame, text="Finished tasks:", width=21, anchor="w",
                                       background="#EBEBEB")
        self.user_fin_tasks.place(x=150, y=60)
        self.user_n_fin_tasks = tk.Label(self.stat_frame, text="Not finished tasks:", width=21, anchor="w",
                                         background="#EBEBEB")
        self.user_n_fin_tasks.place(x=150, y=85)
        self.percentage_lbl = tk.Label(self.stat_frame, text="Percentage of total tasks:", width=21, anchor="w",
                                       background="#EBEBEB")
        self.percentage_lbl.place(x=150, y=110)
        self.percentage_lbl = tk.Label(self.stat_frame, text="Percentage of completed tasks:", width=21, anchor="w",
                                       background="#EBEBEB")
        self.percentage_lbl.place(x=150, y=135)
        self.percentage_lbl = tk.Label(self.stat_frame, text="% of not completed tasks:", width=21, anchor="w",
                                       background="#EBEBEB")
        self.percentage_lbl.place(x=150, y=160)
        self.percentage_lbl = tk.Label(self.stat_frame, text="Percentage of overdue tasks:", width=21, anchor="w",
                                       background="#EBEBEB")
        self.percentage_lbl.place(x=150, y=185)

        self.user_lbl2 = tk.Label(self.stat_frame, text=f"{str(self.user).title()}", width=10, anchor="center",
                                  background="#EBEBEB")
        self.user_lbl2.place(x=450, y=10)
        self.user_all2_tasks = tk.Label(self.stat_frame, text=f"{self.stat[0]}", width=10, anchor="center",
                                        background="#EBEBEB")
        self.user_all2_tasks.place(x=450, y=35)
        self.user_fin2_tasks = tk.Label(self.stat_frame, text=f"{self.stat[1]}", width=10, anchor="center",
                                        background="#EBEBEB")
        self.user_fin2_tasks.place(x=450, y=60)
        self.user_n_fin2_tasks = tk.Label(self.stat_frame, text=f"{self.stat[2]}", width=10, anchor="center",
                                          background="#EBEBEB")
        self.user_n_fin2_tasks.place(x=450, y=85)
        self.percentage_lbl1 = tk.Label(self.stat_frame,
                                        text=f"{round(int(self.stat[0]) / int(self.tasks_amount) * 100, 2)} %",
                                        width=10, anchor="center",
                                        background="#EBEBEB")
        self.percentage_lbl1.place(x=450, y=110)
        self.percentage_lbl1 = tk.Label(self.stat_frame,
                                        text=f"{round(int(self.stat[1]) / int(self.stat[0]) * 100, 2)} %", width=10,
                                        anchor="center",
                                        background="#EBEBEB")
        self.percentage_lbl1.place(x=450, y=135)
        self.percentage_lbl1 = tk.Label(self.stat_frame,
                                        text=f"{round(int(self.stat[2]) / int(self.stat[0]) * 100, 2)} %", width=10,
                                        anchor="center",
                                        background="#EBEBEB")
        self.percentage_lbl1.place(x=450, y=160)
        self.percentage_lbl1 = tk.Label(self.stat_frame,
                                        text=f"{round(int(self.stat[3]) / int(self.stat[0]) * 100, 2)} %", width=10,
                                        anchor="center",
                                        background="#EBEBEB")
        self.percentage_lbl1.place(x=450, y=185)


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
        self.main_meny_btn = tk.Button(self.main_frame, text="Main page", command=lambda: self.show_frame(MainPage),
                                       bg=self.background, )
        self.user_name_label.place(x=220, y=10, width=250, height=20)
        self.log_out_btn.place(x=550, y=2, width=100, height=20)
        self.main_meny_btn.place(x=550, y=25, width=100, height=20)
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
        self.logged_in_user = self.master.logged_in_user

        self.main_frame = tk.LabelFrame(self, bg=self.background)
        self.main_frame.place(x=10, y=10)
        self.user_frame = tk.LabelFrame(self.main_frame, bg=self.background, )

        self.user_name_label = tk.Label(self.main_frame, text=f"View all Users tasks:",
                                        bg=self.background, font=('Helvetica', 20, "bold"))
        self.log_out_btn = tk.Button(self.main_frame, text="Log out", command=lambda: self.show_frame(LoginPage),
                                     bg=self.background, )
        self.main_meny_btn = tk.Button(self.main_frame, text="Main page", command=lambda: self.show_frame(MainPage),
                                       bg=self.background, )
        self.user_name_label.place(x=220, y=10, width=250, height=20)
        self.log_out_btn.place(x=550, y=2, width=100, height=20)
        self.main_meny_btn.place(x=550, y=25, width=100, height=20)
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
                frame = Task_Frame(self.scrollable_frame, task=task, user=self.logged_in_user)
                frame.pack()

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_bar.pack(side="right", fill="y")

    def show_frame(self, page_name):
        self.destroy()
        page_name().place(height=500, width=700)


class View_My_Tasks(tk.Frame):
    def __init__(self):
        super(View_My_Tasks, self).__init__()
        self.background = self.master["background"]
        self.font = ('Helvetica', 16)
        self.logged_in_user = self.master.logged_in_user

        self.main_frame = tk.LabelFrame(self, bg=self.background)
        self.main_frame.place(x=10, y=10)
        self.user_frame = tk.LabelFrame(self.main_frame, bg=self.background, )

        self.user_name_label = tk.Label(self.main_frame, text=f"{str(self.logged_in_user).title()} tasks:",
                                        bg=self.background, font=('Helvetica', 20, "bold"))
        self.log_out_btn = tk.Button(self.main_frame, text="Log out", command=lambda: self.show_frame(LoginPage),
                                     bg=self.background, )
        self.main_meny_btn = tk.Button(self.main_frame, text="Main page", command=lambda: self.show_frame(MainPage),
                                       bg=self.background, )
        self.user_name_label.place(x=220, y=10, width=250, height=20)
        self.log_out_btn.place(x=550, y=2, width=100, height=20)
        self.main_meny_btn.place(x=550, y=25, width=100, height=20)
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
                if task[1].lower() == str(self.logged_in_user).lower():
                    frame = Task_Frame(self.scrollable_frame, task=task, user=self.logged_in_user)
                    frame.pack()

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_bar.pack(side="right", fill="y")

    def show_frame(self, page_name):
        self.destroy()
        page_name().place(height=500, width=700)


class Add_Task(tk.Frame):
    def __init__(self):
        super(Add_Task, self).__init__()

        self.background = self.master["background"]
        self.font = ('Helvetica', 16)
        self.logged_in_user = self.master.logged_in_user
        self.users = list(self.master.all_users.keys())

        self.main_frame = tk.LabelFrame(self, bg=self.background)
        self.main_frame.place(x=10, y=10)
        self.user_frame = tk.LabelFrame(self.main_frame, bg=self.background, )

        self.user_name_label = tk.Label(self.main_frame, text=f"Add {str(self.logged_in_user).title()} tasks:",
                                        bg=self.background, font=('Helvetica', 20, "bold"))
        self.log_out_btn = tk.Button(self.main_frame, text="Log out", command=lambda: self.show_frame(LoginPage),
                                     bg=self.background, )
        self.main_meny_btn = tk.Button(self.main_frame, text="Main page", command=lambda: self.show_frame(MainPage),
                                       bg=self.background, )
        self.user_name_label.place(x=220, y=10, width=250, height=20)
        self.log_out_btn.place(x=550, y=2, width=100, height=20)
        self.main_meny_btn.place(x=550, y=25, width=100, height=20)
        self.main_frame.place(height=50, width=680, )

        self.scd_frame = tk.LabelFrame(self, text="Tasks:", bg=self.background)
        self.scd_frame.place(x=10, y=60, width=680, height=430)

        self.task_lbl = tk.Label(self.scd_frame, text='Task:', width=15)
        self.task_lbl.place(x=200, y=10)
        self.task_entry = tk.Entry(self.scd_frame, width=25)
        self.task_entry.place(x=350, y=10)

        self.task_id_lbl = tk.Label(self.scd_frame, text="Task ID", width=15)
        self.task_id_lbl.place(x=200, y=50)
        self.id = randrange(10000)
        self.task_id = tk.Label(self.scd_frame, text=self.id, width=15)
        self.task_id.place(x=350, y=50)
        self.user_lbl = tk.Label(self.scd_frame, text="Assigned to:", width=15)
        self.user_lbl.place(x=200, y=90)
        if str(self.logged_in_user).lower() != "admin":
            self.user_entry = tk.Label(self.scd_frame, text=f"{str(self.logged_in_user).title()}", width=15)
            self.user_entry.place(x=350, y=90)
        else:
            self.user_entry = ttk.Combobox(self.scd_frame, values=self.users, width=15)
            self.user_entry.place(x=350, y=90)

        self.date_assigned_lbl = tk.Label(self.scd_frame, text="Date assigned:", width=15)
        self.date_assigned_lbl.place(x=200, y=130)
        self.date_assigned = DateEntry(self.scd_frame, text="Today", width=10, date_pattern='dd/mm/YYYY')
        self.date_assigned.place(x=350, y=130)
        self.date_due_to_lbl = tk.Label(self.scd_frame, text="Due date: ", width=15)
        self.date_due_to_lbl.place(x=200, y=170)
        self.date_due_to = DateEntry(self.scd_frame, text=" date: ", width=10, date_pattern='dd/MM/YYYY')
        self.date_due_to.place(x=350, y=170)
        self.date_due_to._top_cal.overrideredirect(False)
        self.tsk_cmpl_lbl = tk.Label(self.scd_frame, text="Task complete ?", width=15)
        self.tsk_cmpl_lbl.place(x=200, y=210)
        self.tsk_cmpl = ttk.Combobox(self.scd_frame, values=("Yes", "No"), width=5)
        self.tsk_cmpl.current(1)
        self.tsk_cmpl.place(x=350, y=210)
        self.task_deskr_lbl = tk.Label(self.scd_frame, text="Task description:", width=15)
        self.task_deskr_lbl.place(x=200, y=250)
        self.task_deskr = tk.Text(self.scd_frame, width=35, height=7)
        self.task_deskr.place(x=350, y=250)

        self.sbm_btn = tk.Button(self.scd_frame, text="Submit", command=lambda: self.save_task())
        self.sbm_btn.place(x=300, y=350)

    def show_frame(self, page_name):
        self.destroy()
        page_name().place(height=500, width=700)

    def save_task(self):
        if str(self.logged_in_user).lower() == "admin":
            user = self.user_entry.get()
        else:
            user = self.logged_in_user
        task = str(self.id) + ',' + str(user) + ',' + str(self.task_entry.get()) + ',' + str(
            self.task_deskr.get("1.0", "end-1c")).replace('\n', " ") + ',' + str(
            datetime.strptime(self.date_assigned.get(), '%d/%m/%Y').strftime('%d %b %Y')) + "," + str(
            datetime.strptime(self.date_due_to.get(), '%d/%m/%Y').strftime('%d %b %Y')) + ',' + str(
            self.tsk_cmpl.get()) + '\n'

        with open("tasks.txt", "a") as file:
            file.write(task)
            messagebox.showerror(title="Susses", message="Task added !")
            self.show_frame(MainPage)


class Task_Frame(tk.Frame):
    def __init__(self, parent, task=None, user=None):
        tk.Frame.__init__(self, parent, )
        self.background = '#EBEBEB'
        self.task = task
        self.logged_in_user = user
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
        self.edit_button = tk.Button(self.task_frame, text="Edit", command=lambda: print(self.master.logged_in_user))
        self.edit_button.place(x=600, y=0)
        self.confirm_button = tk.Button(self.task_frame, text="Done", command=lambda: self.mark_task_done(task[0]))
        self.confirm_button.place(x=600, y=25)
        self.del_button = tk.Button(self.task_frame, text="Delt", command=lambda: self.delete_task(task[0]))
        self.del_button.place(x=600, y=50)
        if str(task[6]).strip() == "Yes":
            self.fin_lbl = tk.Label(self.task_frame, text='+', background='green')
        else:
            self.fin_lbl = tk.Label(self.task_frame, text='-', background='red')
        self.fin_lbl.place(x=575, y=25)

        self.pack()

    def mark_task_done(self, task):
        answer = messagebox.askokcancel(title="Confirm", message="Confirm task fulfilment ? !")
        new_file_text = list()
        if answer:
            with open("tasks.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    line = line.split(",")
                    if line[0] == task:
                        line[6] = "Yes\n"
                    new_file_text.append(','.join(line))
            with open("tasks.txt", "w") as file:
                file.write(''.join(new_file_text))
        self.destroy()
        if 'view_tasks' in str(self):
            View_Tasks().place(height=500, width=700)
        elif 'view_my_tasks' in str(self):
            View_My_Tasks().place(height=500, width=700)

    def delete_task(self, task):
        if str(self.logged_in_user).lower() == "admin":
            answer = messagebox.askokcancel(title="Delete ?", message="Confirm delete task! ")
            new_file_text = list()
            if answer:
                with open("tasks.txt", "r") as file:
                    lines = file.readlines()
                    for line in lines:
                        line = line.split(",")
                        if line[0] != task[0]:
                            new_file_text.append(','.join(line))
                with open("tasks.txt", "w") as file:
                    file.write(''.join(new_file_text))
                self.destroy()
                if 'view_tasks' in str(self):
                    View_Tasks().place(height=500, width=700)
                elif 'view_my_tasks' in str(self):
                    View_My_Tasks().place(height=500, width=700)
        else:
            messagebox.showerror(title="Error", message="You don't have right to do this !")
            self.bell()


if __name__ == '__main__':
    app = App()
    app.mainloop()
