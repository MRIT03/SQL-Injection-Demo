import sqlite3
import random

def create_database():
    # Connect to the SQLite database. If it doesn't exist, it will be created.
    conn = sqlite3.connect('Bank.db')
    c = conn.cursor()

    # Create a new table named 'Accounts'
    c.execute('''
        CREATE TABLE IF NOT EXISTS Accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            balance INTEGER NOT NULL
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def generate_username():
    # Generate a username using common names with a number appended
    names = ['alex', 'kim', 'chris', 'sam', 'jordan', 'morgan', 'pat', 'devon', 'taylor', 'casey']
    number = random.randint(1, 99)
    return random.choice(names) + str(number)

def generate_simple_password():
    # Generate a simple password consisting of a random word and numbers
    words = ['apple', 'banana', 'cherry', 'date', 'elderberry']
    number = random.randint(10, 99)
    return random.choice(words) + str(number)

def insert_random_data():
    # Connect to the SQLite database
    conn = sqlite3.connect('Bank.db')
    c = conn.cursor()

    # Insert 10 random entries into the Accounts table
    for _ in range(10):
        username = generate_username()
        password = generate_simple_password()
        balance = random.randint(1000, 100000)  # Balance as a whole number

        c.execute('''
            INSERT INTO Accounts (username, password, balance)
            VALUES (?, ?, ?)
        ''', (username, password, balance))

    # Add a special user 'admin' with password 'admin' and a balance of 0
    c.execute('''
        INSERT INTO Accounts (username, password, balance)
        VALUES (?, ?, ?)
    ''', ('admin', 'admin', 0))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Create the database and table
create_database()

# Insert random data into the table, including the admin user
insert_random_data()
