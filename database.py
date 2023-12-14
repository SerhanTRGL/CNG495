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
        (1, 200, 'Oil Change', '2023-01-15', 'Regular oil change', 1),
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
