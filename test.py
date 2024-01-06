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



def userMenu(conn, user_id):
    # User menu function
    c = conn.cursor()
    while True:
        print("\nMenu:")
        print("1. Show Past Maintenance Records")
        print("2. Add New Vehicle")
        print("3. Add New Appointment")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            # Show Past Maintenance Records
            c.execute("""
                SELECT M.maintenanceId, M.name, M.date, M.description, V.model
                FROM MAINTENANCE M
                JOIN VEHICLE_MAINTENANCE VM ON M.maintenanceId = VM.maintenanceId
                JOIN USER_VEHICLE UV ON VM.vehicleId = UV.vehicleId
                JOIN VEHICLE V ON UV.vehicleId = V.vehicleId
                WHERE UV.userId = ?
            """, (user_id,))
            maintenance_records = c.fetchall()
            if maintenance_records:
                for record in maintenance_records:
                    print(
                        f"Maintenance ID: {record[0]}, Name: {record[1]}, Date: {record[2]}, Description: {record[3]}, Vehicle Model: {record[4]}")
            else:
                print("No past maintenance records found for this user.")

        elif choice == '2':
            model = input("Enter vehicle model: ")
            miles = int(input("Enter vehicle miles: "))
            type_ = input("Enter vehicle type: ")
            year = int(input("Enter vehicle year: "))
            c.execute("INSERT INTO VEHICLE (miles, type, model, year) VALUES (?, ?, ?, ?)",
                      (miles, type_, model, year))
            vehicle_id = c.lastrowid
            c.execute("INSERT INTO USER_VEHICLE (userId, vehicleId) VALUES (?, ?)", (user_id, vehicle_id))
            conn.commit()
            print("New vehicle added.")

            # Display all vehicles for the user
            c.execute("""
                                SELECT V.vehicleId, V.model, V.type, V.year, V.miles
                                FROM VEHICLE V
                                JOIN USER_VEHICLE UV ON V.vehicleId = UV.vehicleId
                                WHERE UV.userId = ?
                            """, (user_id,))
            vehicles = c.fetchall()
            print("\nAll Vehicles:")
            for vehicle in vehicles:
                print(
                    f"Vehicle ID: {vehicle[0]}, Model: {vehicle[1]}, Type: {vehicle[2]}, Year: {vehicle[3]}, Miles: {vehicle[4]}")


        elif choice == '3':
            # Add New Appointment

            # List Vehicles
            c.execute(
                "SELECT V.vehicleId, V.model FROM VEHICLE V JOIN USER_VEHICLE UV ON V.vehicleId = UV.vehicleId WHERE UV.userId = ?",
                (user_id,))
            vehicles = c.fetchall()
            for vehicle in vehicles:
                print(f"Vehicle ID: {vehicle[0]}, Model: {vehicle[1]}")
            vehicle_id = input("Choose your vehicle ID: ")

            # List Repair Shops
            c.execute("SELECT shopId, address FROM REPAIR_SHOP")
            shops = c.fetchall()
            for shop in shops:
                print(f"Shop ID: {shop[0]}, Address: {shop[1]}")
            shop_id = input("Choose repair shop ID: ")

            date = input("Enter the date of the appointment (YYYY-MM-DD): ")

            c.execute("INSERT INTO APPOINTMENT (date, userId, vehicleId, shopId) VALUES (?, ?, ?, ?)",
                      (date, user_id, vehicle_id, shop_id))
            conn.commit()
            print("New appointment added.")


def repairShopMenu(conn, shop_id):
    c = conn.cursor()
    while True:
        print("\nRepair Shop Menu:")
        print("1. Show All User Information")
        print("2. Add New Maintenance Record")
        print("3. View Appointments")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            # Show All User Information
            c.execute("""
                SELECT U.userId, U.name, U.email, U.phoneNumber
                FROM USER U
                JOIN APPOINTMENT A ON U.userId = A.userId
                JOIN SHOP_APPOINTMENT SA ON A.appointmentId = SA.appointmentId
                WHERE SA.shopId = ?
            """, (shop_id,))
            users = c.fetchall()
            if users:
                for user in users:
                    print(f"User ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Phone: {user[3]}")
            else:
                print("No users found for this repair shop.")

        elif choice == '2':
            # Add New Maintenance Record

            # Step 1: List Users and Select User
            c.execute("""
                            SELECT U.userId, U.name
                            FROM USER U
                            JOIN APPOINTMENT A ON U.userId = A.userId
                            JOIN SHOP_APPOINTMENT SA ON A.appointmentId = SA.appointmentId
                            WHERE SA.shopId = ?
                        """, (shop_id,))
            users = c.fetchall()
            for user in users:
                print(f"User ID: {user[0]}, Name: {user[1]}")

            selected_user_id = input("Enter the User ID for maintenance: ")

            # Step 2: List User's Vehicles
            c.execute("""
                            SELECT V.vehicleId, V.model
                            FROM VEHICLE V
                            JOIN USER_VEHICLE UV ON V.vehicleId = UV.vehicleId
                            WHERE UV.userId = ?
                        """, (selected_user_id,))
            vehicles = c.fetchall()
            for vehicle in vehicles:
                print(f"Vehicle ID: {vehicle[0]}, Model: {vehicle[1]}")

            selected_vehicle_id = input("Enter the Vehicle ID for maintenance: ")

            # Step 3 & 4: Enter Maintenance Details
            cost = input("Enter maintenance cost: ")
            name = input("Enter maintenance name: ")
            date = input("Enter date (YYYY-MM-DD): ")
            description = input("Enter maintenance description: ")

            c.execute("INSERT INTO MAINTENANCE (cost, name, date, description, shopId) VALUES (?, ?, ?, ?, ?)",
                      (cost, name, date, description, shop_id))
            maintenance_id = c.lastrowid
            c.execute("INSERT INTO VEHICLE_MAINTENANCE (vehicleId, maintenanceId) VALUES (?, ?)",
                      (selected_vehicle_id, maintenance_id))
            conn.commit()
            print("New maintenance record added with ID:", maintenance_id)

        elif choice == '3':
            # View Appointments
            c.execute("""
                        SELECT A.appointmentId, A.date, U.name, V.model
                        FROM APPOINTMENT A
                        JOIN USER U ON A.userId = U.userId
                        JOIN VEHICLE V ON A.vehicleId = V.vehicleId
                        WHERE A.shopId = ?
                    """, (shop_id,))
            appointments = c.fetchall()
            if appointments:
                for appt in appointments:
                    print(f"Appointment ID: {appt[0]}, Date: {appt[1]}, User Name: {appt[2]}, Vehicle Model: {appt[3]}")
            else:
                print("No appointments found for this shop.")

        elif choice == '4':
            # Exit the menu
            print("Exiting Repair Shop Menu...")
            break

def adminMenu(conn):
    c = conn.cursor()
    while True:
        print("\nAdmin Menu:")
        print("1. View Repair Shop Statistics")
        print("2. Add New Repair Shop")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            # View Repair Shop Statistics
            c.execute("""
                SELECT RS.shopId, RS.email, SUM(M.cost) AS total_income
                FROM REPAIR_SHOP RS
                JOIN MAINTENANCE M ON RS.shopId = M.shopId
                GROUP BY RS.shopId
            """)
            stats = c.fetchall()
            for stat in stats:
                print(f"Repair Shop {stat[0]} ({stat[1]}) Total Income: {stat[2]}")

        elif choice == '2':
            # Add New Repair Shop
            email = input("Enter repair shop email: ")
            phone = input("Enter repair shop phone number: ")
            address = input("Enter repair shop address: ")
            status = input("Enter repair shop status: ")
            password = input("Enter repair shop password: ")
            c.execute("INSERT INTO REPAIR_SHOP (email, phoneNumber, address, status, password) VALUES (?, ?, ?, ?, ?)",
                      (email, phone, address, status, password))
            conn.commit()
            print("New repair shop added.")

        elif choice == '3':
            print("Exiting Admin Menu...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    dbname = input("Enter db name: ")
    createDatabase(dbname)
    insertRecords(dbname)

    conn = sqlite3.connect(dbname)
    c = conn.cursor()


    userType = input("Are you a 'user', 'repair shop', or 'admin'? Enter 'user', 'shop', or 'admin': ")
    email = input("Enter email: ")
    password = input("Enter password: ")

    if userType.lower() == 'user':
        c.execute("SELECT userId FROM USER WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        if user:
            userMenu(conn, user[0])
        else:
            print("Invalid user credentials.")

    elif userType.lower() == 'shop':
        c.execute("SELECT shopId FROM REPAIR_SHOP WHERE email=? AND password=?", (email, password))
        shop = c.fetchone()
        if shop:
            repairShopMenu(conn, shop[0])
        else:
            print("Invalid repair shop credentials.")

    elif userType.lower() == 'admin':
        c.execute("SELECT adminId FROM ADMIN WHERE email=? AND password=?", (email, password))
        admin = c.fetchone()
        if admin:
            adminMenu(conn)
        else:
            print("Invalid admin credentials.")

    conn.close()
