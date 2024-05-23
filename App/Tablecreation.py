import mysql.connector

# Establish connection to the database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
  database="FinanceMate"
)

# Create a cursor object to execute SQL queries
cursor = mydb.cursor()
# Create tables
try:
    # Users Table
    cursor.execute("""
    CREATE TABLE Users (
        UserID INT AUTO_INCREMENT PRIMARY KEY,
        Username VARCHAR(255) NOT NULL,
        Password VARCHAR(255) NOT NULL,
        Email VARCHAR(255)
    )
    """)

    # Income Table
    cursor.execute("""
    CREATE TABLE Income (
        IncomeID INT AUTO_INCREMENT PRIMARY KEY,
        UserID INT,
        Source VARCHAR(255) NOT NULL,
        Amount DECIMAL(10, 2) NOT NULL,
        Date DATE NOT NULL,
        Description TEXT,
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    )
    """)

    # Budget Categories Table
    cursor.execute("""
    CREATE TABLE BudgetCategories (
        CategoryID INT AUTO_INCREMENT PRIMARY KEY,
        UserID INT,
        Category VARCHAR(255) NOT NULL,
        BudgetLimit DECIMAL(10, 2) NOT NULL,
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    )
    """)

    # Expense Table
    cursor.execute("""
    CREATE TABLE Expenses (
        ExpenseID INT AUTO_INCREMENT PRIMARY KEY,
        UserID INT,
        CategoryID INT,
        Category VARCHAR(255),
        Amount DECIMAL(10, 2) NOT NULL,
        Date DATE NOT NULL,
        Description TEXT,
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    )
    """)

    mydb.commit()
    print("Tables created successfully.")
except mysql.connector.Error as err:
    print("Error creating tables: ", err)

mydb.close()