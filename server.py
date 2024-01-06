import copy
import threading
from threading import *
import socket
from datetime import datetime
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

senderEmail = "carmanagementSystemMETUNCC@gmail.com"
password = "tsan uyja hvbg fydf"  # App specific password

def send_email(subject, message, from_email, to_email, password, smtp_server='smtp.gmail.com', smtp_port=587):
    # Create message container
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach message
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Establish a secure session with the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        # Login to the email server
        server.login(from_email, password)

        # Send the email
        server.sendmail(from_email, to_email, msg.as_string())

        # Close the SMTP server connection
        server.quit()

        print("Email sent successfully!")
    except Exception as e:
        print("Email could not be sent.")
        print(e)

class ClientThread(Thread):

    # clientSocket represents connection
    def __init__(self, clientSocket, clientAddress):
        Thread.__init__(self)
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress

    def run(self):
        msg = "SERVER>>> connectionsuccess".encode()
        self.clientSocket.send(msg)
        clientMsg = self.clientSocket.recv(1024).decode()
        originalMessage = copy.deepcopy(clientMsg)
        clientMsg = clientMsg.split(";")

        while clientMsg[0] != "CLIENT>>> TERMINATE":
            if clientMsg[0] == "CLIENT>>> register":
                conn = sqlite3.connect("car.db")
                c = conn.cursor()
                print(originalMessage)

                c.execute("SELECT * FROM USER WHERE email=?", (clientMsg[2], ))
                row = c.fetchone()
                #this means the user is already exist in our databse
                if row != None:
                    msg = "SERVER>>> registerfailure".encode()
                else:
                    c.execute("INSERT INTO USER(name,email,password,phoneNumber) VALUES(?,?,?,?)", (clientMsg[1], clientMsg[2], clientMsg[3], clientMsg[4]))
                    conn.commit()
                    msg = "SERVER>>> registersuccess".encode()

                self.clientSocket.send(msg)
                conn.close()

            elif clientMsg[0] == "CLIENT>>> login":
                conn = sqlite3.connect("car.db")
                c = conn.cursor()
                print(originalMessage)
                if clientMsg[3] == 'user':
                    c.execute("SELECT userId FROM USER WHERE email=? AND password=?", (clientMsg[1], clientMsg[2]))
                    user = c.fetchone()
                    if user:
                        msg = ("SERVER>>> loginsuccess" + ";" + clientMsg[1] + ";" + clientMsg[3] + ";" + clientMsg[2]).encode()
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

            elif clientMsg[0] == "CLIENT>>> showPastTransactions":
                conn = sqlite3.connect("car.db")
                c = conn.cursor()
                print(originalMessage)
                c.execute("SELECT userId FROM USER WHERE email=? AND password=?", (clientMsg[1], clientMsg[2]))
                user_id = c.fetchone()

                c.execute("""
                               SELECT M.maintenanceId, M.name, M.date, M.description, V.model
                               FROM MAINTENANCE M
                               JOIN VEHICLE_MAINTENANCE VM ON M.maintenanceId = VM.maintenanceId
                               JOIN USER_VEHICLE UV ON VM.vehicleId = UV.vehicleId
                               JOIN VEHICLE V ON UV.vehicleId = V.vehicleId
                               WHERE UV.userId = ?
                           """, user_id)

                maintenance_records = c.fetchall()

                seperatedRecords = ';'.join(str(item) for item in maintenance_records)

                if maintenance_records:
                    msg = ("SERVER>>> pasttransactionssuccess;" + seperatedRecords).encode()
                else:
                    msg = ("SERVER>>> notransaction").encode()

                self.clientSocket.send(msg)
                conn.close()


            elif clientMsg[0] == "CLIENT>>> addnewappointment":
                conn = sqlite3.connect("car.db")
                c = conn.cursor()
                print(originalMessage)

                #     get the user ID
                c.execute("SELECT userId FROM USER WHERE email=? AND password=?", (clientMsg[1], clientMsg[2]))
                user_id = c.fetchone()

                appointmentData = user_id + (int(clientMsg[3]), ) + (int(clientMsg[4]), )+ (clientMsg[5], )
                c.execute("INSERT INTO APPOINTMENT(userId,vehicleId,shopId,date) VALUES (?,?,?,?)", appointmentData)
                conn.commit()
                conn.close()
                subject = "Your appointment has been successfully made!"
                message = (f"{clientMsg[1]}, your car appointment has been successfully made. You may see the details below:\n"
                           f"Vehicle ID: {clientMsg[3]}\n"
                           f"Shop ID: {clientMsg[4]}\n"
                           f"Appointment date: {clientMsg[5]}\n"
                           f"Please do not miss your appointment.\n"
                           f"Regards,\n"
                           f"Car Repair Management System Administration...")
                send_email(subject, message, senderEmail, clientMsg[1],password);
                msg = "SERVER>>> addnewappointmentsuccess".encode()
                self.clientSocket.send(msg)


            elif clientMsg[0] == "CLIENT>>> addnewcar":
                conn = sqlite3.connect("car.db")
                c = conn.cursor()
                print(originalMessage)

                #     get the user ID
                c.execute("SELECT userId FROM USER WHERE email=? AND password=?", (clientMsg[1], clientMsg[2]))
                user_id = c.fetchone()


                c.execute("INSERT INTO VEHICLE (miles, type, model, year) VALUES (?, ?, ?, ?)",
                          (clientMsg[3], clientMsg[4], clientMsg[5], clientMsg[6]))
                conn.commit()

                vehicle_id = c.lastrowid
                data = user_id + (vehicle_id, )

                c.execute("INSERT INTO USER_VEHICLE (userId, vehicleId) VALUES (?, ?)", data)
                conn.commit()

                msg = "SERVER>>> addNewCarSuccess".encode()
                self.clientSocket.send(msg)
                conn.close()


            elif clientMsg[0] == "CLIENT>>> showMyCars":
                conn = sqlite3.connect("car.db")
                c = conn.cursor()
                print(originalMessage)
                c.execute("SELECT userId FROM USER WHERE email=? AND password=?", (clientMsg[1], clientMsg[2]))
                user_id = c.fetchone()

                c.execute("SELECT vehicleId FROM USER_VEHICLE WHERE userId=?", user_id)
                vehicle_ids = c.fetchall()
                allCarIds = []
                for id in vehicle_ids:
                    allCarIds.append(id[0])

                if len(allCarIds) > 1 and allCarIds:
                    c.execute("SELECT * FROM VEHICLE WHERE vehicleId IN {}".format(tuple(allCarIds)))
                elif allCarIds:
                    c.execute("SELECT * FROM VEHICLE WHERE vehicleId=?", vehicle_ids[0])

                records = c.fetchall()
                seperatedRecords = ';'.join(str(item) for item in records)

                if records:
                    msg = ("SERVER>>> showallcarsuccess;" + seperatedRecords).encode()
                else:
                    msg = ("SERVER>>> nocartoshow").encode()

                self.clientSocket.send(msg)
                conn.close()


            elif clientMsg[0] == "CLIENT>>> showcarowners":
                conn = sqlite3.connect("car.db")
                c = conn.cursor()
                print(originalMessage)
                c.execute("SELECT shopId FROM REPAIR_SHOP WHERE email=? AND password=?", (clientMsg[1], clientMsg[2]))
                shop_id = c.fetchone()

                # Show All User Information
                c.execute("""
                               SELECT U.userId, U.name, U.email, U.phoneNumber
                               FROM USER U
                               JOIN APPOINTMENT A ON U.userId = A.userId
                               JOIN SHOP_APPOINTMENT SA ON A.appointmentId = SA.appointmentId
                               WHERE SA.shopId = ?
                           """, shop_id)
                users = c.fetchall()

                seperatedRecords = ';'.join(str(item) for item in users)

                if users:
                    msg = ("SERVER>>> showownersuccess;" + seperatedRecords).encode()
                else:
                    msg = ("SERVER>>> nouser").encode()

                self.clientSocket.send(msg)
                conn.close()


            elif clientMsg[0] == "CLIENT>>> showappointments":
                conn = sqlite3.connect("car.db")
                c = conn.cursor()
                print(originalMessage)
                c.execute("SELECT shopId FROM REPAIR_SHOP WHERE email=? AND password=?", (clientMsg[1], clientMsg[2]))
                shop_id = c.fetchone()

                # View Appointments
                c.execute("""
                                        SELECT A.appointmentId, A.date, U.name, V.model
                                        FROM APPOINTMENT A
                                        JOIN USER U ON A.userId = U.userId
                                        JOIN VEHICLE V ON A.vehicleId = V.vehicleId
                                        WHERE A.shopId = ?
                                    """, shop_id)
                appointments = c.fetchall()
                print(appointments)

                seperatedRecords = ';'.join(str(item) for item in appointments)

                if appointments:
                    msg = ("SERVER>>> showappointmentsuccess;" + seperatedRecords).encode()
                else:
                    msg = ("SERVER>>> noappointment").encode()

                self.clientSocket.send(msg)
                conn.close()


            elif clientMsg[0] == "CLIENT>>> addnewmaintanance":
                conn = sqlite3.connect("car.db")
                c = conn.cursor()
                print(originalMessage)

                #     get the SHOP ID
                c.execute("SELECT shopId FROM REPAIR_SHOP WHERE email=? AND password=?", (clientMsg[1], clientMsg[2]))
                shop_id = c.fetchone()

                maintananceData = (int(clientMsg[4]), ) + (clientMsg[5], ) + (clientMsg[6], ) + (clientMsg[7], ) + shop_id


                c.execute("INSERT INTO MAINTENANCE (cost, name, date, description, shopId) VALUES (?, ?, ?, ?, ?)", maintananceData)

                maintenance_id = c.lastrowid
                vehicleMaintanance = (maintenance_id, ) + (int(clientMsg[4]), )
                c.execute("INSERT INTO VEHICLE_MAINTENANCE (vehicleId, maintenanceId) VALUES (?, ?)", vehicleMaintanance)
                conn.commit()
                conn.close()

                msg = "SERVER>>> addnewmaintanancesuccess".encode()
                self.clientSocket.send(msg)

            elif clientMsg[0] == "CLIENT>>> updatemaintanance":

                conn = sqlite3.connect("car.db")
                c = conn.cursor()
                print(originalMessage)

                # Get the SHOP ID
                c.execute("SELECT shopId FROM REPAIR_SHOP WHERE email=? AND password=?", (clientMsg[1], clientMsg[2]))
                shop_id = c.fetchone()[0]

                maintananceData = (int(clientMsg[4]), clientMsg[5], clientMsg[6], clientMsg[7], shop_id, int(clientMsg[3]))




                c.execute("UPDATE MAINTENANCE SET  cost=?, name=?, date=?, description=?, shopId=? WHERE maintenanceId=?",maintananceData)

                # Commit the changes
                conn.commit()
                conn.close()

                msg = "SERVER>>> updatemaintanancesuccess".encode()
                self.clientSocket.send(msg)



            elif clientMsg[0] == "CLIENT>>> showRepairshopAnalytics":
                conn = sqlite3.connect("car.db")
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
                conn = sqlite3.connect("car.db")
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



HOST = ""
PORT = 3389

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    serverSocket.bind((HOST, PORT))
except socket.error:
    print("Connection failed!")
    exit(1)
print("Waiting for connections")
while True:
    serverSocket.listen()
    clientSocket, clientAddress = serverSocket.accept()
    newThread = ClientThread(clientSocket, clientAddress)
    newThread.start()