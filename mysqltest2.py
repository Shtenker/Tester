import mysql.connector
import time
import statistics

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "1234",
    "database": "testdb",
}


def measure_latency():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS latency_test (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50),
            timestamp FLOAT
        )
    """)
    conn.commit()

    insert_latencies = []
    read_latencies = []

    for i in range(100):
        start = time.time()
        cursor.execute("INSERT INTO latency_test (name, timestamp) VALUES (%s, %s)", (f"user_{i}", time.time()))
        conn.commit()
        insert_latencies.append(time.time() - start)

        start = time.time()
        cursor.execute("SELECT * FROM latency_test WHERE id = %s", (i + 1,))
        cursor.fetchall()
        read_latencies.append(time.time() - start)

    cursor.close()
    conn.close()

    print("\n✅ MySQL Latency Test Completed.")
    print(f"📥 Avg Insert Latency: {sum(insert_latencies)/len(insert_latencies):.5f} s")
    print(f"📤 Avg Read Latency:   {sum(read_latencies)/len(read_latencies):.5f} s")
    print(f"📊 Insert Std Dev:     {statistics.stdev(insert_latencies):.5f}")
    print(f"📊 Read Std Dev:       {statistics.stdev(read_latencies):.5f}")

if __name__ == "__main__":
    print("🧪 Starting MySQL Latency Test...\n")
    measure_latency()
