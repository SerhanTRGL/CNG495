from tkinter import messagebox
from tkinter import *
from tkinter import font
import sqlite3
from threading import *
import socket
import matplotlib.pyplot as plt
import ast


class Home(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.pack()
        self.master.title("Home")

        self.frame1 = Frame(self)
        self.frame1.pack(padx=15, pady=15)

        self.nameLbl = Label(self.frame1, text="WELCOME TO OUR SYSTEM")
        self.nameLbl.pack(side=TOP, padx=5, pady=5)


        self.frame2 = Frame(self)
        self.frame2.pack(padx=5, pady=5)

        self.loginBtn = Button(self.frame2, text="Register", command=self.buttonPressedRegister)
        self.loginBtn.pack(padx=5, pady=5)

        self.frame3 = Frame(self)
        self.frame3.pack(padx=5, pady=5)

        self.loginBtn = Button(self.frame3, text="Login", command=self.buttonPressedLogin)
        self.loginBtn.pack(padx=5, pady=5)


    def  buttonPressedRegister(self):
        self.master.destroy()
        window = Registration()
        window.mainloop()

    def  buttonPressedLogin(self):
        self.master.destroy()
        window = Login()
        window.mainloop()



class Registration(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.pack()
        self.master.title("Login")

        self.frame1 = Frame(self)
        self.frame1.pack(padx=5, pady=5)

        self.nameLbl = Label(self.frame1, text="Name: ")
        self.nameLbl.pack(side=LEFT, padx=5, pady=5)

        self.nameEntry = Entry(self.frame1, name="name")
        self.nameEntry.pack(padx=5, pady=5)

        self.frame2 = Frame(self)
        self.frame2.pack(padx=5, pady=5)

        self.emailLbl = Label(self.frame2, text="E-mail:")
        self.emailLbl.pack(side=LEFT, padx=5, pady=5)

        self.emailEntry = Entry(self.frame2, name="email")
        self.emailEntry.pack(padx=5, pady=5)

        self.frame3 = Frame(self)
        self.frame3.pack(padx=5, pady=5)

        self.passwordLbl = Label(self.frame3, text="Password")
        self.passwordLbl.pack(side=LEFT, padx=5, pady=5)

        self.passwordEntry = Entry(self.frame3, name="password", show="*")
        self.passwordEntry.pack(padx=5, pady=5)

        self.frame4 = Frame(self)
        self.frame4.pack(padx=5, pady=5)

        self.phonenoLbl = Label(self.frame4, text="phoneNumber:")
        self.phonenoLbl.pack(side=LEFT, padx=5, pady=5)

        self.phonenoEntry = Entry(self.frame4, name="phoneno")
        self.phonenoEntry.pack(padx=5, pady=5)

        self.frame5 = Frame(self)
        self.frame5.pack(padx=5, pady=5)

        self.loginBtn = Button(self.frame5, text="Register", command=self.buttonPressed)
        self.loginBtn.pack(padx=5, pady=5)

    def buttonPressed(self):
        name = self.nameEntry.get()
        email = self.emailEntry.get()
        password = self.passwordEntry.get()
        phoneno = self.phonenoEntry.get()
        clientMsg = "register;" + name + ";" + email + ";" + password+ ";" + phoneno
        msg = ("CLIENT>>> " + clientMsg).encode()
        clientSocket.send(msg)

        serverMsg = clientSocket.recv(1024).decode()
        print(serverMsg)
        serverMsg = serverMsg.split(";")  # after getting server message, I splitted it
        if serverMsg[0] != "SERVER>>> registersuccess":
            messagebox.showerror("Error", "Invalid register!")

        else:
            self.master.destroy()
            window = Login()
            window.mainloop()








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
                window = CarOwner(email, password)
                window.mainloop()
            elif serverMsg[2] == "shop":
                window = Repairshop(email, password)
                window.mainloop()
            elif serverMsg[2] == "admin":
                window = SystemAdmin()
                window.mainloop()
            else:
                exit(1)






class CarOwner(Frame):

    def __init__(self, userMail, userPassword):
        Frame.__init__(self)
        self.userMail = userMail
        self.userPassword = userPassword
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

        self.carStatusLbl = Label(self.frame5, text="Show My Cars", anchor="w")
        self.carStatusLbl.pack(side=LEFT, padx=5, pady=5, expand=YES, fill=BOTH)

        self.carStatusBtn = Button(self.frame5, text="Show", command=self.buttonPressedShowCars)
        self.carStatusBtn.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.frame6 = Frame(self)
        self.frame6.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.closeBtn = Button(self.frame6, text="Close", command=self.buttonPressedClose)
        self.closeBtn.pack(padx=5, pady=5, expand=YES, fill=BOTH)


    def buttonPressedShowPast(self):
        clientMsg = "showPastTransactions;" + self.userMail + ";" + self.userPassword
        msg = ("CLIENT>>> " + clientMsg).encode()
        clientSocket.send(msg)

        serverMsg = clientSocket.recv(1024).decode()
        print(serverMsg) #M.maintenanceId, M.name, M.date, M.description, V.model
        serverMsg = serverMsg.split(";")
        if serverMsg[0] == "SERVER>>> pasttransactionssuccess":
        # make the string back again a tuple to get each element
            parsed_tuple = ast.literal_eval(serverMsg[1])
            messagebox.showinfo(f"Message", "Your past transactions are: "
                                        f"Maintanance ID:{parsed_tuple[0]}\n"
                                        f"Maintanance Name: {parsed_tuple[1]}\n"
                                        f"Maintanance Date: {parsed_tuple[2]}\n"
                                        f"Maintanace Description: {parsed_tuple[3]}\n"
                                        f"Vehicle Model: {parsed_tuple[4]}")
        else:
            messagebox.showerror("Error", "You dont have any past transaction record!")

    def buttonPressedNewAppointment(self):
        self.master.destroy()
        appointmentWindow = NewAppointment(self.userMail, self.userPassword)
        appointmentWindow.mainloop()



    def buttonPressedAddCar(self):
        self.master.destroy()
        addCarWindow = CarOwnerAddCar(self.userMail, self.userPassword)
        addCarWindow.mainloop()

    def buttonPressedShowCars(self):
        clientMsg = "showMyCars;" + self.userMail + ";" + self.userPassword
        msg = ("CLIENT>>> " + clientMsg).encode()
        clientSocket.send(msg)

        serverMsg = clientSocket.recv(1024).decode()
        print(serverMsg)
        parts = serverMsg.split(";")
        if len(parts) > 1 and parts[0] == "SERVER>>> showallcarsuccess":
            data = ";".join(parts[1:])
            tuple_strings = data.split(';')
            tuples_list = [eval(f"({tuple_str})") for tuple_str in tuple_strings]
            message = "Your cars are as follows:\n"
            counter = 1
            for car_info in tuples_list:
                message += f"\nCar {counter}:\n"
                message += f"Car ID: {car_info[0]}\nPrice: {car_info[1]}\nType: {car_info[2]}\nModel: {car_info[3]}\nYear: {car_info[4]}\n"
                counter += 1
            messagebox.showinfo("Car Information", message)
        else:
            messagebox.showerror("Error", "You don't have any car in the system!")

    def buttonPressedClose(self):
        self.master.destroy()





class NewAppointment(Frame):
    def __init__(self, userMail, userPassword):
        Frame.__init__(self)
        self.userMail = userMail
        self.userPassword = userPassword
        self.pack()
        self.master.title("Make Appointment")

        self.frame1 = Frame(self)
        self.frame1.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.carIDLbl = Label(self.frame1, text="Car ID:")
        self.carIDLbl.pack(side=LEFT, padx=5, pady=5, expand=YES, fill=BOTH, anchor="w")

        self.carIDEntry = Entry(self.frame1, name="carid")
        self.carIDEntry.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.frame2 = Frame(self)
        self.frame2.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.rapairshopIDLbl = Label(self.frame2, text="Repairshop ID:")
        self.rapairshopIDLbl.pack(side=LEFT, padx=5, pady=5, expand=YES, fill=BOTH, anchor="w")

        self.rapairshopIDEntry = Entry(self.frame2, name="repairshop ID")
        self.rapairshopIDEntry.pack(padx=5, pady=5, expand=YES, fill=BOTH)


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
        carid = self.carIDEntry.get()
        repairshopid = self.rapairshopIDEntry.get()
        appointmentdate = self.appointmentDateEntry.get()

        clientMsg = "addnewappointment;" + self.userMail + ";" + self.userPassword + ";" + carid + ";" + repairshopid + ";" + appointmentdate
        msg = ("CLIENT>>> " + clientMsg).encode()
        clientSocket.send(msg)

        serverMsg = clientSocket.recv(1024).decode()
        print(serverMsg)
        serverMsg = serverMsg.split(";")
        if serverMsg[0] == "SERVER>>> addnewappointmentsuccess":
            messagebox.showinfo("Success", "You have added a new appointment successfully")
        else:
            messagebox.showerror("Error", "Your appointment could not be added to the system!")

    def buttonPressedClose(self):
        self.master.destroy()


class CarOwnerAddCar(Frame):

    def __init__(self, userMail, userPassword):
        Frame.__init__(self)
        self.userMail = userMail
        self.userPassword = userPassword
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
        model = self.carModelEntry.get()
        miles = self.carMilesEntry.get()
        type = self.carTypeEntry.get()
        year = self.carYearEntry.get()
        clientMsg = "addnewcar;" + self.userMail + ";" + self.userPassword + ";" + model + ";" + miles + ";" + type + ";" + year
        msg = ("CLIENT>>> " + clientMsg).encode()
        clientSocket.send(msg)

        serverMsg = clientSocket.recv(1024).decode()
        print(serverMsg)
        serverMsg = serverMsg.split(";")
        if serverMsg[0] == "SERVER>>> addNewCarSuccess":
            messagebox.showinfo("Success", "You have added a car successfully")
        else:
            messagebox.showerror("Error", "Your car could not be added to the system!")
    def buttonPressedClose(self):
        self.master.destroy()



class Repairshop(Frame):

    def __init__(self, repairshopMail, repairshopPassword):
        Frame.__init__(self)
        self.repairshopMail = repairshopMail
        self.repairshopPassword = repairshopPassword
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
        clientMsg = "showcarowners;" + self.repairshopMail + ";" + self.repairshopPassword
        msg = ("CLIENT>>> " + clientMsg).encode()
        clientSocket.send(msg)

        serverMsg = clientSocket.recv(1024).decode()
        print(serverMsg)
        parts = serverMsg.split(";")
        if len(parts) > 1 and parts[0] == "SERVER>>> showownersuccess":
            data = ";".join(parts[1:])
            tuple_strings = data.split(';')
            tuples_list = [eval(f"({tuple_str})") for tuple_str in tuple_strings]
            message = "Your Car Owners are as follows:\n"
            counter = 1
            for appointment_info in tuples_list:
                message += f"\nOwner {counter}:\n"
                message += f"ID: {appointment_info[0]}\nName: {appointment_info[1]}\nEmail: {appointment_info[2]}\nPhone Number: {appointment_info[3]}\n"
                counter += 1
            messagebox.showinfo("Car Owner Information", message)
        else:
            messagebox.showerror("Error", "You don't have any car owner in the system!")

    def buttonPressedShowAppointments(self):
        clientMsg = "showappointments;" + self.repairshopMail + ";" + self.repairshopPassword
        msg = ("CLIENT>>> " + clientMsg).encode()
        clientSocket.send(msg)

        serverMsg = clientSocket.recv(1024).decode()
        print(serverMsg)
        parts = serverMsg.split(";")  #A.appointmentId, A.date, U.name, V.model
        if len(parts) > 1 and parts[0] == "SERVER>>> showappointmentsuccess":
            data = ";".join(parts[1:])
            tuple_strings = data.split(';')
            tuples_list = [eval(f"({tuple_str})") for tuple_str in tuple_strings]
            message = "Your appointments are as follows:\n"
            counter = 1
            for appointment_info in tuples_list:
                message += f"\nAppointment {counter}:\n"
                message += f"ID: {appointment_info[0]}\nDate: {appointment_info[1]}\nCar Owner Name: {appointment_info[2]}\nVehicle Model: {appointment_info[3]}\n"
                counter += 1
            messagebox.showinfo("Appointment Information", message)
        else:
            messagebox.showerror("Error", "You don't have any appointment in the system!")


    def buttonPressedAddMaintanance(self):
        self.master.destroy()
        addMaintananceWindow = AddMaintanance(self.repairshopMail, self.repairshopPassword)
        addMaintananceWindow.mainloop()

    def buttonPressedUpdateMaintanance(self):
        self.master.destroy()
        updateMaintananceWindow = UpdateMaintanance(self.repairshopMail, self.repairshopPassword)
        updateMaintananceWindow.mainloop()


    def buttonPressedClose(self):
        self.master.destroy()



class AddMaintanance(Frame):
    def __init__(self, repairshopMail, repairshopPassword):
        Frame.__init__(self)
        self.repairshopMail = repairshopMail
        self.repairshopPassword = repairshopPassword
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
        carId = self.carIDEntry.get()
        cost = self.carMaintananceCostEntry.get()
        type = self.maintananceTypeEntry.get()
        enddate = self.maintananceEndDateEntry.get()
        description = self.maintananceDescriptionEntry.get()
        clientMsg = "addnewmaintanance;" + self.repairshopMail + ";" + self.repairshopPassword + ";" + carId + ";" + cost + ";" + type + ";" + enddate + ";" + description
        msg = ("CLIENT>>> " + clientMsg).encode()
        clientSocket.send(msg)

        serverMsg = clientSocket.recv(1024).decode()
        print(serverMsg)
        serverMsg = serverMsg.split(";")
        if serverMsg[0] == "SERVER>>> addnewmaintanancesuccess":
            messagebox.showinfo("Success", "You have added a maintanance successfully")
        else:
            messagebox.showerror("Error", "Your maintanance could not be added to the system!")

    def buttonPressedClose(self):
        self.master.destroy()


class UpdateMaintanance(Frame):
    def __init__(self,repairshopMail, repairshopPassword):
        Frame.__init__(self)
        self.repairshopMail = repairshopMail
        self.repairshopPassword = repairshopPassword
        self.pack()
        self.master.title("Update Maintanance")

        self.frame1 = Frame(self)
        self.frame1.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.maintananceIDLbl = Label(self.frame1, text="Maintanance ID:")
        self.maintananceIDLbl.pack(side=LEFT, padx=5, pady=5, expand=YES, fill=BOTH, anchor="w")

        self.maintananceIDEntry = Entry(self.frame1, name="id")
        self.maintananceIDEntry.pack(padx=5, pady=5, expand=YES, fill=BOTH)

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
        maintananceId = self.maintananceIDEntry.get()
        cost = self.carMaintananceCostEntry.get()
        type = self.maintananceTypeEntry.get()
        newenddate = self.updateEndDateEntry.get()
        description = self.maintananceDescriptionEntry.get()
        clientMsg = "updatemaintanance;" + self.repairshopMail + ";" + self.repairshopPassword + ";" + maintananceId + ";" + cost + ";" + type + ";" + newenddate + ";" + description
        msg = ("CLIENT>>> " + clientMsg).encode()
        clientSocket.send(msg)

        serverMsg = clientSocket.recv(1024).decode()
        print(serverMsg)
        serverMsg = serverMsg.split(";")
        if serverMsg[0] == "SERVER>>> updatemaintanancesuccess":
            messagebox.showinfo("Success", "You have updated a maintanance enddate successfully")
        else:
            messagebox.showerror("Error", "Your maintanance enddate could not be updated!")

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


class AddRepairshop(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.pack()
        self.master.title("Add Repair Shop")

        self.frame1 = Frame(self)
        self.frame1.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.repairshopEmailLbl = Label(self.frame1, text="Repair Shop Email:")
        self.repairshopEmailLbl.pack(side=LEFT, padx=5, pady=5, expand=YES, fill=BOTH, anchor="w")

        self.repairshopEmailEntry = Entry(self.frame1, name="repairshopemail")
        self.repairshopEmailEntry.pack(padx=5, pady=5, expand=YES, fill=BOTH)

        self.frame2 = Frame(self)
        self.frame2.pack(padx=5, pady=5)

        self.repairshopPhoneNoLbl = Label(self.frame2, text="Repair Shop Phone Number:")
        self.repairshopPhoneNoLbl.pack(side=LEFT, padx=5, pady=5, anchor="w")

        self.repairshopPhoneNoEntry = Entry(self.frame2, name="repairshopphoneno")
        self.repairshopPhoneNoEntry.pack(padx=5, pady=5)

        self.frame3 = Frame(self)
        self.frame3.pack(padx=5, pady=5)

        self.repairshopAddressLbl = Label(self.frame3, text="Repair Shop Address:")
        self.repairshopAddressLbl.pack(side=LEFT, padx=5, pady=5, anchor="w")

        self.repairshopAddressEntry = Entry(self.frame3, name="repairshopaddress")
        self.repairshopAddressEntry.pack(padx=5, pady=5)

        self.frame4 = Frame(self)
        self.frame4.pack(padx=5, pady=5)

        self.repairshopStatusLbl = Label(self.frame4, text="Repair Shop Status:")
        self.repairshopStatusLbl.pack(side=LEFT, padx=5, pady=5, anchor="w")

        self.repairshopStatusEntry = Entry(self.frame4, name="repairshopstatus")
        self.repairshopStatusEntry.pack(padx=5, pady=5)

        self.frame5 = Frame(self)
        self.frame5.pack(padx=5, pady=5)

        self.repairshopPasswordLbl = Label(self.frame5, text="Repair Shop Password:")
        self.repairshopPasswordLbl.pack(side=LEFT, padx=5, pady=5, anchor="w")

        self.repairshopPasswordEntry = Entry(self.frame5, name="repairshoppassword")
        self.repairshopPasswordEntry.pack(padx=5, pady=5)

        self.frame6 = Frame(self)
        self.frame6.pack(padx=5, pady=5)

        self.addRepairShopBtn = Button(self.frame6, text="Add", command=self.buttonPressedAddRepairshop)
        self.addRepairShopBtn.pack(padx=5, pady=5)

        self.frame7 = Frame(self)
        self.frame7.pack(padx=5, pady=5)

        self.closeBtn = Button(self.frame7, text="Close", command=self.buttonPressedClose)
        self.closeBtn.pack(padx=5, pady=5)

    def buttonPressedAddRepairshop(self):
        email = self.repairshopEmailEntry.get()
        phoneNumber = self.repairshopPhoneNoEntry.get()
        address = self.repairshopAddressEntry.get()
        status = self.repairshopStatusEntry.get()
        password = self.repairshopPasswordEntry.get()

        clientMsg = "addRepairshop;" + email + ";" + phoneNumber + ";" + address + ";" + status + ";" + password
        print(clientMsg)
        msg = ("CLIENT>>> " + clientMsg).encode()
        clientSocket.send(msg)

        serverMsg = clientSocket.recv(1024).decode()
        print(serverMsg)
        serverMsg = serverMsg.split(";")  # after getting server message, I splitted it
        if serverMsg[0] == "SERVER>>> addRepairshopSuccess":
            messagebox.showinfo("Message", "Repairshop has been successfully added!")
        else:
            messagebox.showerror("Error", "Repairshop has NOT been successfully added!")

    def buttonPressedClose(self):
        self.master.destroy()




if __name__ == "__main__":
    HOST = "34.155.248.200"
    PORT = 3389
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        clientSocket.connect((HOST, PORT))
    except socket.error:
        print("Connection error!")

    serverMsg = clientSocket.recv(1024).decode()
    if serverMsg == "SERVER>>> connectionsuccess":
        print(serverMsg)
        window = Home()
        window.mainloop()

        # serverMsg = clientSocket.recv(1024).decode()

    else:
        msg = "CLIENT>>> TERMINATE".encode()
        clientSocket.send(msg)
        print("Connection terminated! ")
        clientSocket.close()
