Car Repair Shop Management System with Cloud Server

--Client.py
- Which you can run on your machine to connect to the server!
-   As of right now, there is only a single admin account and below are the details:
-     admin@example.com
-     adminpassword
-     admin (choose it on the "Roles" radio button!)
-   For user login, follow the registration process

--Client.py Registration
-   With the *new* update, you may register to the system with your own details!
-   Right after registration, you will be directed to the login page.
-   Login with the email and password you used for the registration.
-   After registration, all new users get *user* role, so make sure to choose that role in login page.

--Server.py
- Which is currently and will be running 24/7 on Google Cloud Platform.
- It handles generating queries with the details sent by a number of clients
- Executes these queries on the database (which is also located on Google Cloud Platform)
- And sends the result of these queries back to the client.

--Server.py Sending Emails
- After a client makes an appointmnet, the server will send an email to the user's email address with the details of their appointment.
- This is handled using SMTP.

--Submissions (Folder)
- Here you may find all the submissions that was made on ODTUClass
