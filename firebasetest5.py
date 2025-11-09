import threading
import time
from google.cloud import firestore
from google.oauth2 import service_account
import random

TABLE_NAME = "users_thread_test"
BATCH_SIZE = 5   
SLEEP_BETWEEN_BATCHES = 0.2  

creds = service_account.Credentials.from_service_account_file(
    "/Users/nilswahlberg/Desktop/keyyes/firebase-key.json"
)
db = firestore.Client(credentials=creds)

def insert_batch(thread_id, posts_per_thread):
    for i in range(posts_per_thread):
        batch = db.batch()
        for j in range(BATCH_SIZE):
            doc_id = f"user_{thread_id}_{i}_{j}"
            doc_ref = db.collection(TABLE_NAME).document(doc_id)
            batch.set(doc_ref, {
                "name": f"User_{thread_id}_{i}_{j}",
                "email": f"user_{thread_id}_{i}_{j}@example.com",
                "balance": random.randint(0, 1000)
            })
        try:
            batch.commit()
        except Exception as e:
            print(f"Thread {thread_id} batch {i} failed: {e}")
        time.sleep(SLEEP_BETWEEN_BATCHES)

def run_threads(thread_count, max_posts_per_thread):
    threads = []
    start = time.time()
    for t in range(thread_count):
        posts = (t + 1) * max_posts_per_thread   
        thread = threading.Thread(target=insert_batch, args=(t, posts))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    elapsed = time.time() - start
    print(f"{thread_count} threads, max {max_posts_per_thread} posts scaling -> {elapsed:.3f}s total")

if __name__ == "__main__":
    run_threads(thread_count=3, max_posts_per_thread=5)
