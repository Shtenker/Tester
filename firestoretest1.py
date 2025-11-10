import firebase_admin
from firebase_admin import credentials, firestore
import time
import random
import string

cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def run_test_firestore(record_count=100):
    collection_name = "users"

 
    start_insert = time.time()
    batch = db.batch()
    for i in range(record_count):
        name = ''.join(random.choices(string.ascii_letters, k=8))
        email = f"{name.lower()}@example.com"
        doc_ref = db.collection(collection_name).document(email)
        batch.set(doc_ref, {"name": name, "email": email})
        if (i + 1) % 500 == 0:   
            batch.commit()
            batch = db.batch()
    batch.commit()
    insert_time = time.time() - start_insert

     
    start_read = time.time()
    docs = list(db.collection(collection_name).stream())
    read_time = time.time() - start_read

    return insert_time, read_time

if __name__ == "__main__":
    inserts, reads = run_test_firestore(100)
    print(f"Firestore: Inserted 100 records in {inserts:.4f}s, Read {len(list(range(100)))} records in {reads:.4f}s")
