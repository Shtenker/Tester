import firebase_admin
from firebase_admin import credentials, firestore
import time

 
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def run_test(record_count):
    collection_name = "scalability_test"
    print(f"\n🧪 Inserting {record_count} records...")
    start_time = time.time()

  
    batch = db.batch()
    for i in range(record_count):
        doc_ref = db.collection(collection_name).document(f"user_{i}")
        batch.set(doc_ref, {"name": f"User_{i}", "age": i % 100})
        
        if (i + 1) % 500 == 0:
            batch.commit()
            batch = db.batch()
    batch.commit()  
    insert_time = time.time() - start_time
    print(f"✅ Inserted {record_count} records in {insert_time:.2f}s")

    
    print("📖 Reading records...")
    start_time = time.time()
    docs = list(db.collection(collection_name).stream())
    read_time = time.time() - start_time
    print(f"📊 Read {len(docs)} records in {read_time:.2f}s")

    return insert_time, read_time


if __name__ == "__main__":
    total_records = 0
    for batch_size in [1000, 5000, 10000]:
        insert_time, read_time = run_test(batch_size)
        total_records += batch_size
        print(f"📈 Total records so far: {total_records}")
