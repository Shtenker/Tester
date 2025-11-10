import mysql.connector
import time

 
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "1234",
    "database": "demo"
}

def run_test(record_count):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scalability_test (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ph1 VARCHAR(255),
            ph2 INT
        )
    """)
    conn.commit()

    print(f"\n🧪 Inserting {record_count} records...")
    start_time = time.time()

   
    for i in range(record_count):
        cursor.execute(
            "INSERT (ph1, ph2) VALUES (%s, %s)",
            (f"User_{i}", i % 100)
        )

        
        if (i + 1) % 500 == 0:
            conn.commit()

    conn.commit()
    insert_time = time.time() - start_time
    print(f"✅ Inserted {record_count} records in {insert_time:.2f}s")

    
    print("📖 Reading records...")
    start_time = time.time()
    cursor.execute("SELECT * FROM scalability_test")
    rows = cursor.fetchall()
    read_time = time.time() - start_time
    print(f"📊 Read {len(rows)} records in {read_time:.2f}s")

    cursor.close()
    conn.close()

    return insert_time, read_time


if __name__ == "__main__":
    total_records = 0
    for batch_size in [1000, 5000, 10000]:
        insert_time, read_time = run_test(batch_size)
        total_records += batch_size
        print(f"📈 Total records so far: {total_records}")
