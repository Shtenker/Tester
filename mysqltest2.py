 
import os
import time
import mysql.connector
from mysql.connector import Error

 
DB_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASS = os.getenv("MYSQL_PASSWORD", "")
DB_NAME = os.getenv("MYSQL_DB", "testdb")

TABLE_NAME = "users_test_100k"
RECORD_COUNT = 100_000
BATCH_SIZE = 1000   

CREATE_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS `{TABLE_NAME}` (
  `id` VARCHAR(100) PRIMARY KEY,
  `name` VARCHAR(200),
  `email` VARCHAR(200),
  `balance` INT
) ENGINE=InnoDB;
"""

INSERT_SQL = f"INSERT INTO `{TABLE_NAME}` (`id`, `name`, `email`, `balance`) VALUES (%s, %s, %s, %s)"

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        autocommit=False  
    )

def prepare_table(conn):
    with conn.cursor() as cur:
        cur.execute(CREATE_TABLE_SQL)
        conn.commit()

def insert_records(conn, record_count, batch_size=BATCH_SIZE):
    start_time = time.time()
    cur = conn.cursor()
    batch = []
    committed = 0
    try:
        for i in range(record_count):
            row = (f"user_{i}", f"User_{i}", f"user_{i}@example.com", 100)
            batch.append(row)
            if len(batch) >= batch_size:
                cur.executemany(INSERT_SQL, batch)
                conn.commit()
                committed += len(batch)
                batch.clear()
               
                if committed % 10000 == 0:
                    print(f"Committed {committed:,}/{record_count:,} rows")
        
        if batch:
            cur.executemany(INSERT_SQL, batch)
            conn.commit()
            committed += len(batch)
    finally:
        cur.close()
    elapsed = time.time() - start_time
    return elapsed

def read_all_records(conn):
    start_time = time.time()
    cur = conn.cursor(buffered=True)
    try:
        cur.execute(f"SELECT COUNT(*) FROM `{TABLE_NAME}`")
        total = cur.fetchone()[0]
        
        cur.execute(f"SELECT `id` FROM `{TABLE_NAME}`")
        read_count = 0
        chunk_size = 10000
        while True:
            rows = cur.fetchmany(chunk_size)
            if not rows:
                break
            read_count += len(rows)
        elapsed = time.time() - start_time
    finally:
        cur.close()
    return total, elapsed

def main():
    print(f"Connecting to MySQL at {DB_HOST} as {DB_USER} ...")
    try:
        conn = get_connection()
    except Error as e:
        print("Connection error:", e)
        return

    try:
        prepare_table(conn)
        print(f"🧪 MySQL Large-Scale Test: {RECORD_COUNT:,} records into `{TABLE_NAME}`\n")

        insert_time = insert_records(conn, RECORD_COUNT)
        total, read_time = read_all_records(conn)

        print(f"\n✅ Inserted {total:,} rows in {insert_time/60:.2f} min ({insert_time:.2f} s)")
        print(f"📖 Read {total:,} rows in {read_time:.2f} s")
    except Exception as e:
        print("Error during test:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
