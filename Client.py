from tkinter import messagebox
from tkinter import *
from tkinter import font
import sqlite3
from threading import *
import socket
import matplotlib.pyplot as plt


class Login(Frame):

    def __init__(self):
        Frame.__init__(self)
        self.pack()
        self.master.title("Login")


        self.frame1 = Frame(self)
        self.frame1.pack(padx=5, pady=5)

        self.emailLbl = Label(self.frame1, text="E-mail:")
        self.emailLbl.pack(side=LEFT, padx=5, pady=5)

        self.emailEntry = Entry(self.frame1, name="email")
        self.emailEntry.pack(padx=5, pady=5)

        self.frame2 = Frame(self)
        self.frame2.pack(padx=5, pady=5)

        self.passwordLbl = Label(self.frame2, text="Password")
        self.passwordLbl.pack(side=LEFT, padx=5, pady=5)

        self.passwordEntry = Entry(self.frame2, name="password", show="*")
        self.passwordEntry.pack(padx=5, pady=5)

        self.frame3 = Frame(self)
        self.frame3.pack(padx=5, pady=5)

        self.roleLbl = Label(self.frame3, text="Roles: ")
        self.roleLbl.pack(side=LEFT, padx=5, pady=5)

        self.userRoles = ["user", "shop", "admin"]
        self.role = StringVar()
        self.role.set(self.userRoles[0])

        for role in self.userRoles:
            self.roleSelection = Radiobutton(self.frame3, text=role, value=role, variable=self.role)
            self.roleSelection.pack(side=LEFT, padx=5, pady=5)

        self.frame4 = Frame(self)
        self.frame4.pack(padx=5, pady=5)

        self.loginBtn = Button(self.frame4, text="Login", command=self.buttonPressed)
        self.loginBtn.pack(padx=5, pady=5)

    def buttonPressed(self):
        email = self.emailEntry.get()
        password = self.passwordEntry.get()
        role = self.role.get()
        clientMsg = "login;" + email + ";" + password + ";" + role
        msg = ("CLIENT>>> " + clientMsg).encode()
        clientSocket.send(msg)

        serverMsg = clientSocket.recv(1024).decode()
        print(serverMsg)
        serverMsg = serverMsg.split(";")  # after getting server message, I splitted it
        if serverMsg[0] != "SERVER>>> loginsuccess":
            messagebox.showerror("Error", "Invalid login!")

        else:
            self.master.destroy()
            if serverMsg[2] == "user":
                window = CarOwner()
                window.mainloop()
            elif serverMsg[2] == "shop":
                window = Repairshop()
                window.mainloop()
            elif serverMsg[2] == "admin":
                window = SystemAdmin()
                window.mainloop()
            else:
                exit(1)

