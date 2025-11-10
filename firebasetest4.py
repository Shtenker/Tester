from google.cloud import firestore
from google.oauth2 import service_account
import time
import random
import string
import sys

 
creds = service_account.Credentials.from_service_account_file(
    "/Users/nilswahlberg/Desktop/keyyes/firebase-key.json"
)
db = firestore.Client(credentials=creds)
COLLECTION = "error_handling_test"

def insert_users(start, end):
    success_count = 0
    for i in range(start, end):
        name = ''.join(random.choices(string.ascii_letters, k=8))
        email = f"{name.lower()}@example.com"

        
        if random.random() < 0.1:
            print(f"💥 Simulating connection loss at record {i}")
            raise ConnectionError("Simulated Firestore connection loss")

        try:
            db.collection(COLLECTION).document(email).set({
                "name": name,
                "email": email,
                "timestamp": time.time()
            })
            success_count += 1
        except Exception as e:
            print(f"⚠️ Error writing record {i}: {e}")
            raise e
    return success_count

start_time = time.time()
records_inserted = 0
attempted = 0

while records_inserted < 100:
    try:
        attempted += 20
        inserted = insert_users(records_inserted, records_inserted + 20)
        records_inserted += inserted
        print(f"✅ Inserted {records_inserted} records so far")
    except Exception as e:
        print(f"⚠️ Error: {e}. Retrying in 1s...")
        time.sleep(1)
        continue

total_time = time.time() - start_time
print(f"\n✅ Test completed in {total_time:.2f} seconds")
print(f"📊 Insertions attempted: {attempted}")
print(f"📈 Insertions successful: {records_inserted}")

 
docs = list(db.collection(COLLECTION).stream())
print(f"📂 Final number of users in Firestore: {len(docs)}")
