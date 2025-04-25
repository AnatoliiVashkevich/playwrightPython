import sqlite3
import random

def get_random_user():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    print("Fetched user sample:", users[0])
    return random.choice(users)

if __name__ =="__main__":
    user = get_random_user()
    print("Random user", user)

