import firebase_admin
from firebase_admin import credentials, firestore
import time
import random

# Initialize Firebase app
cred = credentials.Certificate("firebase-key.json")  # make sure this path is correct
firebase_admin.initialize_app(cred)
db = firestore.client()

collection_name = "fault_tolerance_test"

# Test setup
num_records = 100
batch_size = 20

def insert_with_retries():
    inserted = 0
    start_time = time.time()

    while inserted < num_records:
        try:
            batch = db.batch()
            for i in range(batch_size):
                # Simulate random connection loss
                if random.random() < 0.1:
                    raise ConnectionError("Simulated network drop")

                doc_ref = db.collection(collection_name).document()
                batch.set(doc_ref, {
                    "user_id": inserted + i,
                    "name": f"user_{inserted + i}",
                    "email": f"user_{inserted + i}@example.com",
                    "timestamp": time.time()
                })

            batch.commit()
            inserted += batch_size
            print(f"✅ Inserted {inserted} records so far")

        except ConnectionError as e:
            print(f"💥 Connection error: {e}")
            print("⚠️ Retrying after short delay...")
            time.sleep(1)
            continue

    total_time = time.time() - start_time
    print(f"\n✅ Test completed in {total_time:.2f} seconds")

if __name__ == "__main__":
    insert_with_retries()
