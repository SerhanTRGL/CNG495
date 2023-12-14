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

class CarOwner(Frame):

    def __init__(self):
        Frame.__init__(self)
        self.pack()
        self.master.title("Car Owner Menu")

        self.frame1 = Frame(self)
        self.frame1.pack(padx=15, pady=25, expand=YES, fill=BOTH)

        bold_font = font.Font(weight="bold")
        self.mainTitle = Label(self.frame1, text="QUERIES & BUTTONS", font=bold_font)
        self.mainTitle.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.frame2 = Frame(self)
        self.frame2.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.showPastLbl = Label(self.frame2, text="Show My Past Transactions",anchor="w")
        self.showPastLbl.pack(side=LEFT, padx=5, pady=5, expand=YES, fill=BOTH)

        self.showPastBtn = Button(self.frame2, text="Show", command=self.buttonPressedShowPast)
        self.showPastBtn.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.frame3 = Frame(self)
        self.frame3.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.newAppointmentLbl = Label(self.frame3, text="Add New Appointment",anchor="w")
        self.newAppointmentLbl.pack(side=LEFT, padx=5, pady=5, expand=YES, fill=BOTH)

        self.newAppointmentBtn = Button(self.frame3, text="Add", command=self.buttonPressedNewAppointment)
        self.newAppointmentBtn.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.frame4 = Frame(self)
        self.frame4.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.newCarLbl = Label(self.frame4, text="Add New Car", anchor="w")
        self.newCarLbl.pack(side=LEFT, padx=5, pady=5, expand=YES, fill=BOTH)

        self.newCarBtn = Button(self.frame4, text="Add", command=self.buttonPressedAddCar)
        self.newCarBtn.pack(padx=5, pady=5, expand=YES, fill=BOTH)


        self.frame5 = Frame(self)
        self.frame5.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.carStatusLbl = Label(self.frame5, text="Show My Car Status", anchor="w")
        self.carStatusLbl.pack(side=LEFT, padx=5, pady=5, expand=YES, fill=BOTH)

        self.carStatusBtn = Button(self.frame5, text="Show", command=self.buttonPressedShowStatus)
        self.carStatusBtn.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.frame6 = Frame(self)
        self.frame6.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.closeBtn = Button(self.frame6, text="Close", command=self.buttonPressedClose)
        self.closeBtn.pack(padx=5, pady=5, expand=YES, fill=BOTH)


    def buttonPressedShowPast(self):
        messagebox.showinfo("Message", "Your past transactions are: ")
    def buttonPressedNewAppointment(self):
        self.master.destroy()
        appointmentWindow = NewAppointment()
        appointmentWindow.mainloop()



    def buttonPressedAddCar(self):
        self.master.destroy()
        addCarWindow = CarOwnerAddCar()
        addCarWindow.mainloop()

    def buttonPressedShowStatus(self):
        # self.master.destroy()
        # showStatusWindow = ShowCarStatus()
        # showStatusWindow.mainloop()
        messagebox.showinfo("Message", "Your car status is: ")

    def buttonPressedClose(self):
        self.master.destroy()

class ShowCarStatus(Frame):
    pass

class NewAppointment(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.pack()
        self.master.title("Make Appointment")


        self.frame1 = Frame(self)
        self.frame1.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.rapairshopIDLbl = Label(self.frame1, text="Repairshop ID:")
        self.rapairshopIDLbl.pack(side=LEFT, padx=5, pady=5, expand=YES, fill=BOTH, anchor="w")

        self.rapairshopIDEntry = Entry(self.frame1, name="repairshop ID")
        self.rapairshopIDEntry.pack(padx=5, pady=5, expand=YES, fill=BOTH)






        self.frame2 = Frame(self)
        self.frame2.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.carIDLbl = Label(self.frame2, text="Car ID:")
        self.carIDLbl.pack(side=LEFT, padx=5, pady=5, expand=YES, fill=BOTH, anchor="w")

        self.carIDEntry = Entry(self.frame2, name="carid")
        self.carIDEntry.pack(padx=5, pady=5, expand=YES, fill=BOTH)





        self.frame3 = Frame(self)
        self.frame3.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.appointmentDateLbl = Label(self.frame3, text="Appointment Date:")
        self.appointmentDateLbl.pack(side=LEFT, padx=5, pady=5, expand=YES, fill=BOTH, anchor="w")

        self.appointmentDateEntry = Entry(self.frame3, name="appointmentdate")
        self.appointmentDateEntry.pack(padx=5, pady=5, expand=YES, fill=BOTH)


        self.frame4 = Frame(self)
        self.frame4.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.makeAppointmentBtn = Button(self.frame4, text="Add", command=self.buttonPressedMakeAppointment)
        self.makeAppointmentBtn.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.frame5 = Frame(self)
        self.frame5.pack(padx=5, pady=5 ,expand=YES, fill=BOTH)

        self.closeBtn = Button(self.frame5, text="Close", command=self.buttonPressedClose)
        self.closeBtn.pack(padx=5, pady=5, expand=YES, fill=BOTH)

    def buttonPressedMakeAppointment(self):
        messagebox.showinfo("Message","Appointment is added!")

    def buttonPressedClose(self):
        self.master.destroy()

class CarOwnerAddCar(Frame):

    def __init__(self):
        Frame.__init__(self)
        self.pack()
        self.master.title("Add Car")


        self.frame1 = Frame(self)
        self.frame1.pack(padx=5, pady=5)

        self.carModelLbl = Label(self.frame1, text="Car Model:")
        self.carModelLbl.pack(side=LEFT, padx=5, pady=5)

        self.carModelEntry = Entry(self.frame1, name="carmodel")
        self.carModelEntry.pack(padx=5, pady=5)

        self.frame2 = Frame(self)
        self.frame2.pack(padx=5, pady=5)

        self.carMilesLbl = Label(self.frame2, text="Car Miles:")
        self.carMilesLbl.pack(side=LEFT, padx=5, pady=5)

        self.carMilesEntry = Entry(self.frame2, name="carmiles")
        self.carMilesEntry.pack(padx=5, pady=5)

        self.frame3 = Frame(self)
        self.frame3.pack(padx=5, pady=5)

        self.carTypeLbl = Label(self.frame3, text="Car Type:")
        self.carTypeLbl.pack(side=LEFT, padx=5, pady=5)

        self.carTypeEntry = Entry(self.frame3, name="cartype")
        self.carTypeEntry.pack(padx=5, pady=5)

        self.frame4 = Frame(self)
        self.frame4.pack(padx=5, pady=5)

        self.carYearLbl = Label(self.frame4, text="Car Year:")
        self.carYearLbl.pack(side=LEFT, padx=5, pady=5)

        self.carYearEntry = Entry(self.frame4, name="caryear")
        self.carYearEntry.pack(padx=5, pady=5)

        self.frame5 = Frame(self)
        self.frame5.pack(padx=5, pady=5)

        self.addCarBtn = Button(self.frame5, text="Add", command=self.buttonPressedAddCar)
        self.addCarBtn.pack(padx=5, pady=5)

        self.frame6 = Frame(self)
        self.frame6.pack(padx=5, pady=5)

        self.closeBtn = Button(self.frame6, text="Close", command=self.buttonPressedClose)
        self.closeBtn.pack(padx=5, pady=5)

    def buttonPressedAddCar(self):
        messagebox.showinfo("Message","Car is added!")

    def buttonPressedClose(self):
        self.master.destroy()

class Repairshop(Frame):

    def __init__(self):
        Frame.__init__(self)
        self.pack()
        self.master.title("RepairShop Menu")

        self.frame1 = Frame(self)
        self.frame1.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.showCarOwnerLbl = Label(self.frame1, text="Show All Car OwnerS", anchor="w")
        self.showCarOwnerLbl.pack(side=LEFT, padx=5, pady=5, expand=YES, fill=BOTH)

        self.showCarOwnerBtn = Button(self.frame1, text="Show", command=self.buttonPressedShowCarOwner)
        self.showCarOwnerBtn.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.frame5 = Frame(self)
        self.frame5.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.showAppointmentLbl = Label(self.frame5, text="Show All Appointments", anchor="w")
        self.showAppointmentLbl.pack(side=LEFT, padx=5, pady=5, expand=YES, fill=BOTH)

        self.showAppointmentBtn = Button(self.frame5, text="Show", command=self.buttonPressedShowAppointments)
        self.showAppointmentBtn.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.frame2 = Frame(self)
        self.frame2.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.addMaintananceLbl = Label(self.frame2, text="Add New Maintanance", anchor="w")
        self.addMaintananceLbl.pack(side=LEFT, padx=5, pady=5, expand=YES, fill=BOTH)

        self.addMaintananceBtn = Button(self.frame2, text="Add", command=self.buttonPressedAddMaintanance)
        self.addMaintananceBtn.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.frame3 = Frame(self)
        self.frame3.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.updateMaintananceLbl = Label(self.frame3, text="Update Maintanance Date", anchor="w")
        self.updateMaintananceLbl.pack(side=LEFT, padx=5, pady=5, expand=YES, fill=BOTH)

        self.updateMaintananceBtn = Button(self.frame3, text="Update", command=self.buttonPressedUpdateMaintanance)
        self.updateMaintananceBtn.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.frame4= Frame(self)
        self.frame4.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.closeBtn = Button(self.frame4, text="Close", command=self.buttonPressedClose)
        self.closeBtn.pack(padx=5, pady=5, expand=YES, fill=BOTH)

    def buttonPressedShowCarOwner(self):
        messagebox.showinfo("Message", "Your Car OwnerS are: ")

    def buttonPressedShowAppointments(self):
        messagebox.showinfo("Message", "Your Appointments are: ")

    def buttonPressedUpdateMaintanance(self):
        self.master.destroy()
        updateMaintananceWindow = UpdateMaintanance()
        updateMaintananceWindow.mainloop()
    def buttonPressedAddMaintanance(self):
        self.master.destroy()
        addMaintananceWindow = AddMaintanance()
        addMaintananceWindow.mainloop()

    def buttonPressedClose(self):
        self.master.destroy()

class AddMaintanance(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.pack()
        self.master.title("Add Maintanance")

        self.frame1 = Frame(self)
        self.frame1.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.carIDLbl = Label(self.frame1, text="Car ID:")
        self.carIDLbl.pack(side=LEFT, padx=5, pady=5, expand=YES, fill=BOTH, anchor="w")

        self.carIDEntry = Entry(self.frame1, name="id")
        self.carIDEntry.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.frame2 = Frame(self)
        self.frame2.pack(padx=5, pady=5)

        self.carMaintananceCostLbl = Label(self.frame2, text="Maintanance Cost:")
        self.carMaintananceCostLbl.pack(side=LEFT, padx=5, pady=5, anchor="w")

        self.carMaintananceCostEntry = Entry(self.frame2, name="cost")
        self.carMaintananceCostEntry.pack(padx=5, pady=5)

        self.frame3 = Frame(self)
        self.frame3.pack(padx=5, pady=5)

        self.maintananceTypeLbl = Label(self.frame3, text="Maintanance Type:")
        self.maintananceTypeLbl.pack(side=LEFT, padx=5, pady=5, anchor="w")

        self.maintananceTypeEntry = Entry(self.frame3, name="type")
        self.maintananceTypeEntry.pack(padx=5, pady=5)

        self.frame4 = Frame(self)
        self.frame4.pack(padx=5, pady=5)

        self.maintananceEndDateLbl = Label(self.frame4, text="Maintanance End Date:")
        self.maintananceEndDateLbl.pack(side=LEFT, padx=5, pady=5, anchor="w")

        self.maintananceEndDateEntry = Entry(self.frame4, name="enddate")
        self.maintananceEndDateEntry.pack(padx=5, pady=5)

        self.frame5 = Frame(self)
        self.frame5.pack(padx=5, pady=5)

        self.maintananceDescriptionLbl = Label(self.frame5, text="Maintanance Description:")
        self.maintananceDescriptionLbl.pack(side=LEFT, padx=5, pady=5, anchor="w")

        self.maintananceDescriptionEntry = Entry(self.frame5, name="description")
        self.maintananceDescriptionEntry.pack(padx=5, pady=5)

        self.frame6 = Frame(self)
        self.frame6.pack(padx=5, pady=5)

        self.addMaintananceBtn = Button(self.frame6, text="Add", command=self.buttonPressedAddMaintanance)
        self.addMaintananceBtn.pack(padx=5, pady=5)

        self.frame7 = Frame(self)
        self.frame7.pack(padx=5, pady=5)

        self.closeBtn = Button(self.frame7, text="Close", command=self.buttonPressedClose)
        self.closeBtn.pack(padx=5, pady=5)


    def buttonPressedAddMaintanance(self):
        messagebox.showinfo("Message","Maintanace is added!")

    def buttonPressedClose(self):
        self.master.destroy()

class UpdateMaintanance(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.pack()
        self.master.title("Update Maintanance")

        self.frame1 = Frame(self)
        self.frame1.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.carIDLbl = Label(self.frame1, text="Car ID:")
        self.carIDLbl.pack(side=LEFT, padx=5, pady=5, expand=YES, fill=BOTH, anchor="w")

        self.carIDEntry = Entry(self.frame1, name="id")
        self.carIDEntry.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.frame2 = Frame(self)
        self.frame2.pack(padx=5, pady=5)

        self.carMaintananceCostLbl = Label(self.frame2, text="Maintanance Cost:")
        self.carMaintananceCostLbl.pack(side=LEFT, padx=5, pady=5, anchor="w")

        self.carMaintananceCostEntry = Entry(self.frame2, name="cost")
        self.carMaintananceCostEntry.pack(padx=5, pady=5)

        self.frame3 = Frame(self)
        self.frame3.pack(padx=5, pady=5)

        self.maintananceTypeLbl = Label(self.frame3, text="Maintanance Type:")
        self.maintananceTypeLbl.pack(side=LEFT, padx=5, pady=5, anchor="w")

        self.maintananceTypeEntry = Entry(self.frame3, name="type")
        self.maintananceTypeEntry.pack(padx=5, pady=5)

        self.frame4 = Frame(self)
        self.frame4.pack(padx=5, pady=5)

        self.updateEndDateLbl = Label(self.frame4, text="New Maintanance End Date:")
        self.updateEndDateLbl.pack(side=LEFT, padx=5, pady=5, anchor="w")

        self.updateEndDateEntry = Entry(self.frame4, name="newenddate")
        self.updateEndDateEntry.pack(padx=5, pady=5)

        self.frame5 = Frame(self)
        self.frame5.pack(padx=5, pady=5)

        self.maintananceDescriptionLbl = Label(self.frame5, text="Maintanance Description:")
        self.maintananceDescriptionLbl.pack(side=LEFT, padx=5, pady=5, anchor="w")

        self.maintananceDescriptionEntry = Entry(self.frame5, name="description")
        self.maintananceDescriptionEntry.pack(padx=5, pady=5)

        self.frame6 = Frame(self)
        self.frame6.pack(padx=5, pady=5)

        self.updateMaintananceBtn = Button(self.frame6, text="Update", command=self.buttonPressedUpdateMaintanance)
        self.updateMaintananceBtn.pack(padx=5, pady=5)

        self.frame7 = Frame(self)
        self.frame7.pack(padx=5, pady=5)

        self.closeBtn = Button(self.frame7, text="Close", command=self.buttonPressedClose)
        self.closeBtn.pack(padx=5, pady=5)


    def buttonPressedUpdateMaintanance(self):
        messagebox.showinfo("Message","Maintanace date is updated!")

    def buttonPressedClose(self):
        self.master.destroy()

class SystemAdmin(Frame):

    def __init__(self):
        Frame.__init__(self)
        self.pack()
        self.master.title("System Admin Menu")

        self.frame1 = Frame(self)
        self.frame1.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.showRepairshopDataLbl = Label(self.frame1, text="Show Repairshop Analytics", anchor="w")
        self.showRepairshopDataLbl.pack(side=LEFT, padx=5, pady=5, expand=YES, fill=BOTH)

        self.showRepairshopDataBtn = Button(self.frame1, text="Show", command=self.buttonPressedShowAnalytics)
        self.showRepairshopDataBtn.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.frame2 = Frame(self)
        self.frame2.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.addRepairshopLbl = Label(self.frame2, text="Add New Repairshop", anchor="w")
        self.addRepairshopLbl.pack(side=LEFT, padx=5, pady=5, expand=YES, fill=BOTH)

        self.addRepairshopBtn = Button(self.frame2, text="Add", command=self.buttonPressedAddRepairshop)
        self.addRepairshopBtn.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.frame3 = Frame(self)
        self.frame3.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.closeBtn = Button(self.frame3, text="Close", command=self.buttonPressedClose)
        self.closeBtn.pack(padx=5, pady=5, expand=YES, fill=BOTH)

    def buttonPressedShowAnalytics(self):
        clientMsg = "showRepairshopAnalytics"
        msg = ("CLIENT>>> " + clientMsg).encode()
        clientSocket.send(msg)

        serverMsg = clientSocket.recv(1024).decode()
        print(serverMsg)
        serverMsg = serverMsg.split(";")  # after getting server message, I splitted it
        serverMsgLength = len(serverMsg)
        repairShopData = serverMsg[1:serverMsgLength-1]

        repairShopIDs = []
        repairShopIncome = []


        for data in repairShopData:
            data = data.split(",")
            repairShopIDs.append("RepairShop" + (data[0]))
            repairShopIncome.append(int(data[1]))


        # bar chart visualisation
        plt.bar(repairShopIDs, repairShopIncome)
        plt.xlabel('Repair Shop IDS')
        plt.ylabel('Repair Shop Income')
        plt.title("Total Income of each RepairShop")
        plt.show()





    def buttonPressedAddRepairshop(self):
        self.master.destroy()
        addRepairshopWindow = AddRepairshop()
        addRepairshopWindow.mainloop()



    def buttonPressedClose(self):
        self.master.destroy()
