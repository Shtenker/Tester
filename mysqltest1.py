import mysql.connector
import time
import random
import string

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "demo"
}

def run_test_mysql(record_count=100):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255)
        )
    """)
    conn.commit()

   
    start_insert = time.time()
    for i in range(record_count):
        name = ''.join(random.choices(string.ascii_letters, k=8))
        email = f"{name.lower()}@example.com"
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    insert_time = time.time() - start_insert

    
    start_read = time.time()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    read_time = time.time() - start_read

    cursor.close()
    conn.close()
    return insert_time, read_time

if __name__ == "__main__":
    inserts, reads = run_test_mysql(100)
    print(f"MySQL: Inserted 100 records in {inserts:.4f}s, Read {100} records in {reads:.4f}s")
