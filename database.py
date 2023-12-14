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
