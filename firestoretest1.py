import threading
import time
import random
import string
import firebase_admin
from firebase_admin import credentials, firestore


cred = credentials.Certificate("firebase-key.json")  
firebase_admin.initialize_app(cred)
db = firestore.client()

def insert_records(thread_id, num_records):
    for i in range(num_records):
        name = ''.join(random.choices(string.ascii_letters, k=8))
        email = f"{name.lower()}@example.com"
        db.collection("users_concurrent").add({
            "thread": thread_id,
            "name": name,
            "email": email
        })

def run_test(threads_count, records_per_thread):
    threads = []
    start = time.time()
    
    for t in range(threads_count):
        thread = threading.Thread(target=insert_records, args=(t, records_per_thread))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_time = time.time() - start
    total_records = threads_count * records_per_thread
    print(f"{threads_count} threads inserted {total_records} records in {total_time:.4f} seconds")


run_test(1, 20)
run_test(5, 20)
run_test(10, 20)
