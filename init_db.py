import sqlite3

#Connect to the DB
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

#Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    company TEXT NOT NULL,
    address TEXT NOT NULL,
    address2 TEXT NOT NULL,
    state TEXT NOT NULL,
    city TEXT NOT NULL,
    zipcode TEXT NOT NULL,
    mobileNumber TEXT NOT NULL
)
''')

#Insert some users
users = [
    ("Alice", "alice@example.com", "pass1234", "Alice", "Petrovich", "Roga i Kopita", "12 Avenue", "aprt 205", "FL", "Miami", "33432", "9992228877"),
    ("Bob", "Bob@example.com", "pass1234", "Bob", "Petrovich", "Roga i Kopita", "12 Avenue", "aprt 205", "FL", "Miami", "33432", "9992228877"),
    ("Charlie", "Charlie@example.com", "pass1234", "Charlie", "Petrovich", "Roga i Kopita", "12 Avenue", "aprt 205", "FL", "Miami", "33432", "9992228877")
]

cursor.executemany("INSERT INTO users (name, email, password, firstName, lastName, company, address, address2, state, city, zipcode, mobileNumber) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", users)
conn.commit()
conn.close()