import copy
import threading
from threading import *
import socket
from datetime import datetime
import sqlite3


def createDatabase(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS USER("
              "userId INTEGER PRIMARY KEY,"
              "name TEXT,"
              "email TEXT,"
              "password TEXT,"
              "phoneNumber TEXT)")

    c.execute("CREATE TABLE IF NOT EXISTS VEHICLE("
              "vehicleId INTEGER PRIMARY KEY,"
              "miles INTEGER,"
              "type TEXT,"
              "model TEXT,"
              "year INTEGER)")

    c.execute("CREATE TABLE IF NOT EXISTS MAINTENANCE("
              "maintenanceId INTEGER PRIMARY KEY,"
              "cost INTEGER,"
              "name TEXT,"
              "date TEXT,"
              "description TEXT,"
              "shopId INTEGER,"
              "FOREIGN KEY(shopId) REFERENCES REPAIR_SHOP(shopId))")

    c.execute("CREATE TABLE IF NOT EXISTS APPOINTMENT("
              "appointmentId INTEGER PRIMARY KEY,"
              "date TEXT,"
              "userId INTEGER,"
              "vehicleId INTEGER,"
              "shopId INTEGER,"
              "FOREIGN KEY(userId) REFERENCES USER(userId),"
              "FOREIGN KEY(vehicleId) REFERENCES VEHICLE(vehicleId),"
              "FOREIGN KEY(shopId) REFERENCES REPAIR_SHOP(shopId))")

    c.execute("CREATE TABLE IF NOT EXISTS REPAIR_SHOP("
              "shopId INTEGER PRIMARY KEY,"
              "email TEXT,"
              "phoneNumber TEXT,"
              "address TEXT,"
              "status TEXT,"
              "password TEXT)")

    c.execute("CREATE TABLE IF NOT EXISTS SCHEDULE("
              "scheduleId INTEGER PRIMARY KEY,"
              "startTime TEXT,"
              "endTime TEXT)")

    c.execute("CREATE TABLE IF NOT EXISTS USER_VEHICLE("
              "userId INTEGER,"
              "vehicleId INTEGER,"
              "FOREIGN KEY(userId) REFERENCES USER(userId),"
              "FOREIGN KEY(vehicleId) REFERENCES VEHICLE(vehicleId),"
              "PRIMARY KEY(userId, vehicleId))")

    c.execute("CREATE TABLE IF NOT EXISTS VEHICLE_MAINTENANCE("
              "vehicleId INTEGER,"
              "maintenanceId INTEGER,"
              "FOREIGN KEY(vehicleId) REFERENCES VEHICLE(vehicleId),"
              "FOREIGN KEY(maintenanceId) REFERENCES MAINTENANCE(maintenanceId),"
              "PRIMARY KEY(vehicleId, maintenanceId))")

    c.execute("CREATE TABLE IF NOT EXISTS SHOP_APPOINTMENT("
              "shopId INTEGER,"
              "appointmentId INTEGER,"
              "FOREIGN KEY(shopId) REFERENCES REPAIR_SHOP(shopId),"
              "FOREIGN KEY(appointmentId) REFERENCES APPOINTMENT(appointmentId),"
              "PRIMARY KEY(shopId, appointmentId))")

    c.execute("CREATE TABLE IF NOT EXISTS APPOINTMENT_SCHEDULE("
              "appointmentId INTEGER,"
              "scheduleId INTEGER,"
              "FOREIGN KEY(appointmentId) REFERENCES APPOINTMENT(appointmentId),"
              "FOREIGN KEY(scheduleId) REFERENCES SCHEDULE(scheduleId),"
              "PRIMARY KEY(appointmentId, scheduleId))")

    c.execute("CREATE TABLE IF NOT EXISTS ADMIN("
              "adminId INTEGER PRIMARY KEY,"
              "name TEXT,"
              "email TEXT,"
              "password TEXT)")

    conn.commit()
    conn.close()

def insertRecords(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    users = [
        (1, 'John Doe', 'john.doe@example.com', 'password123', '555-1234'),
        (2, 'Jane Smith', 'jane.smith@example.com', 'password456', '555-5678'),
        (3, 'Alice Johnson', 'alice.johnson@example.com', 'password789', '555-9012'),
        (4, 'Eren Yarar', 'eren.yarar@metu.edu.tr', '1234', '555-668-73-70')
    ]
    c.executemany("INSERT INTO USER VALUES(?, ?, ?, ?, ?)", users)

    vehicles = [
        (1, 120000, 'Sedan', 'Model S', 2020),
        (2, 23000, 'SUV', 'Model X', 2019),
        (3, 5000, 'Compact', 'Model 3', 2021)
    ]
    c.executemany("INSERT INTO VEHICLE VALUES(?, ?, ?, ?, ?)", vehicles)

    maintenance_records = [
        (1, 1200, 'Oil Change', '2023-01-15', 'Regular oil change', 1),
        (2, 500, 'Tire Replacement', '2023-02-20', 'Replaced all tires', 2),
        (3, 300, 'Brake Service', '2023-03-10', 'Brake pads replaced', 1)
    ]
    c.executemany("INSERT INTO MAINTENANCE VALUES(?, ?, ?, ?, ?, ?)", maintenance_records)

    appointments = [
        (1, '2023-04-15', 1, 1, 1),  # Assuming userId 1, vehicleId 1, shopId 1
        (2, '2023-04-20', 2, 2, 2),  # Assuming userId 2, vehicleId 2, shopId 2
        (3, '2023-04-25', 3, 3, 1)  # Assuming userId 3, vehicleId 3, shopId 1
    ]
    c.executemany("INSERT INTO APPOINTMENT (appointmentId, date, userId, vehicleId, shopId) VALUES (?, ?, ?, ?, ?)",
                  appointments)

    repair_shops = [
        (1, 'shop1@example.com', '555-0202', '1234 Main St', 'Open', 'shop1pass'),
        (2, 'shop2@example.com', '555-0303', '5678 Second St', 'Closed', 'shop2pass')
    ]
    c.executemany("INSERT INTO REPAIR_SHOP VALUES(?, ?, ?, ?, ?, ?)", repair_shops)

    schedules = [
        (1, '08:00', '12:00'),
        (2, '13:00', '17:00')
    ]
    c.executemany("INSERT INTO SCHEDULE VALUES(?, ?, ?)", schedules)

    user_vehicles = [
        (1, 1),
        (2, 2),
        (3, 3)
    ]
    c.executemany("INSERT INTO USER_VEHICLE VALUES(?, ?)", user_vehicles)

    vehicle_maintenance = [
        (1, 1),
        (2, 2),
        (3, 3)
    ]
    c.executemany("INSERT INTO VEHICLE_MAINTENANCE VALUES(?, ?)", vehicle_maintenance)

    shop_appointments = [
        (1, 1),
        (2, 2)
    ]
    c.executemany("INSERT INTO SHOP_APPOINTMENT VALUES(?, ?)", shop_appointments)

    appointment_schedules = [
        (1, 1),
        (2, 2),
        (3, 1)
    ]
    c.executemany("INSERT INTO APPOINTMENT_SCHEDULE VALUES(?, ?)", appointment_schedules)

    admin = [
        ('Admin Name', 'admin@example.com', 'adminpassword')
    ]

    c.executemany("INSERT INTO ADMIN (name, email, password) VALUES (?, ?, ?)", admin)

    conn.commit()
    conn.close()

class ClientThread(Thread):

    # clientSocket represents connection
    def __init__(self, clientSocket, clientAddress):
        Thread.__init__(self)
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress

    def run(self):

        dbname = "car.db"
        # createDatabase(dbname)
        # insertRecords(dbname)



        msg = "SERVER>>> connectionsuccess".encode()
        self.clientSocket.send(msg)
        clientMsg = self.clientSocket.recv(1024).decode()
        originalMessage = copy.deepcopy(clientMsg)
        clientMsg = clientMsg.split(";")

        while clientMsg[0] != "CLIENT>>> TERMINATE":
            if clientMsg[0] == "CLIENT>>> login":
                conn = sqlite3.connect(dbname)
                c = conn.cursor()
                print(originalMessage)
                if clientMsg[3] == 'user':
                    c.execute("SELECT userId FROM USER WHERE email=? AND password=?", (clientMsg[1], clientMsg[2]))
                    user = c.fetchone()
                    if user:
                        msg = ("SERVER>>> loginsuccess" + ";" + clientMsg[1] + ";" + clientMsg[3]).encode()
                    else:
                        msg = "SERVER>>> loginfailure".encode()

                elif clientMsg[3] == 'shop':
                    c.execute("SELECT shopId FROM REPAIR_SHOP WHERE email=? AND password=?", (clientMsg[1], clientMsg[2]))
                    shop = c.fetchone()
                    if shop:
                        msg = ("SERVER>>> loginsuccess" + ";" + clientMsg[1] + ";" + clientMsg[3]).encode()
                    else:
                        msg = "SERVER>>> loginfailure".encode()

                elif clientMsg[3] == 'admin':
                    c.execute("SELECT adminId FROM ADMIN WHERE email=? AND password=?", (clientMsg[1], clientMsg[2]))
                    admin = c.fetchone()
                    if admin:
                        msg = ("SERVER>>> loginsuccess" + ";" + clientMsg[1] + ";" + clientMsg[3]).encode()
                    else:
                        msg = "SERVER>>> loginfailure".encode()
                self.clientSocket.send(msg)
                conn.close()

            elif clientMsg[0] == "CLIENT>>> showRepairshopAnalytics":
                conn = sqlite3.connect(dbname)
                c = conn.cursor()
                print(originalMessage)
                c.execute("""
                            SELECT RS.shopId, RS.email, SUM(M.cost) AS total_income
                            FROM REPAIR_SHOP RS
                            JOIN MAINTENANCE M ON RS.shopId = M.shopId
                            GROUP BY RS.shopId
                """)
                stats = c.fetchall()
                print(stats)
                statList = ""
                for stat in stats:
                    statList += str(stat[0]) + "," + str(stat[2]) + ";"


                msg = ("SERVER>>> showAnalyticsSuccess;" + statList).encode()
                self.clientSocket.send(msg)
                conn.close()

            elif clientMsg[0] == "CLIENT>>> addRepairshop":
                print(originalMessage)
                conn = sqlite3.connect(dbname)
                c = conn.cursor()
                c.execute(
                    "INSERT INTO REPAIR_SHOP (email, phoneNumber, address, status, password) VALUES (?, ?, ?, ?, ?)",
                    (clientMsg[1], clientMsg[2], clientMsg[3], clientMsg[4], clientMsg[5]))
                conn.commit()

                msg = "SERVER>>> addRepairshopSuccess".encode()
                self.clientSocket.send(msg)

                conn.close()

            clientMsg = self.clientSocket.recv(1024).decode()
            originalMessage = copy.deepcopy(clientMsg)
            clientMsg = clientMsg.split(";")


        msg = "SERVER>>> TERMINATE".encode()
        self.clientSocket.send(msg)
        print("Connection terminated - ", self.clientAddress)
        self.clientSocket.close()
