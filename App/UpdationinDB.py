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

cursor.execute("""SELECT CONSTRAINT_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE TABLE_NAME = 'Expenses' AND COLUMN_NAME = 'CategoryID';
""")
cons_name = cursor.fetchall()
print(cons_name)
# cursor.execute("""ALTER TABLE Expenses DROP FOREIGN KEY [constraint_name];""")

mydb.commit()

mydb.close()
