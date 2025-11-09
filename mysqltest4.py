import mysql.connector
import time
import random
import string

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="demo"
    )

def insert_users(conn, start, end):
    cursor = conn.cursor()
    for i in range(start, end):
        name = ''.join(random.choices(string.ascii_letters, k=8))
        email = f"{name.lower()}@example.com"
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
       
        if random.random() < 0.1:  
            print(f"💥 Simulating connection loss at record {i}")
            conn.close()
            raise mysql.connector.errors.OperationalError("Simulated connection loss")
    conn.commit()
    cursor.close()

start_time = time.time()
records_inserted = 0

while records_inserted < 100:
    try:
        conn = connect()
        insert_users(conn, records_inserted, records_inserted + 20)
        records_inserted += 20
        conn.close()
        print(f"✅ Inserted {records_inserted} records so far")
    except Exception as e:
        print(f"⚠️ Error: {e}. Reconnecting...")
        time.sleep(1)
        continue

print(f"\n✅ Test completed in {time.time() - start_time:.2f} seconds")


conn = connect()
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM users")
count = cursor.fetchone()[0]
print(f"📊 Final number of users in table: {count}")
cursor.close()
conn.close()
