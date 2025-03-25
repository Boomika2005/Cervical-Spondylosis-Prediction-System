import sqlite3  

# Connect to the database
conn = sqlite3.connect("patients.db")  
cursor = conn.cursor()  

# Fetch all records
cursor.execute("SELECT * FROM patient_records")  
rows = cursor.fetchall()  

# Print all records
for row in rows:
    print(row)  

# Close connection
conn.close()  
