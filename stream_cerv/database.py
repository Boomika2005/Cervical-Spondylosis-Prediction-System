import sqlite3

# Connect to SQLite database (creates the file if it doesn't exist)
conn = sqlite3.connect("patients.db")
cursor = conn.cursor()

# Create a table to store patient details
cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER,
        gender TEXT,
        pain_score INTEGER,
        neck_flexibility REAL,
        neck_speed REAL,
        motion_range REAL,
        posture_stability REAL,
        muscle_tension REAL,
        frequency_combined REAL,
        peak_power REAL,
        predicted_severity TEXT
    )
''')

# Commit and close the connection
conn.commit()
conn.close()
print("Database and table created successfully!")
