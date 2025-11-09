import time
import threading
import firebase_admin
from firebase_admin import credentials, firestore
import statistics

 
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def measure_latency():
    insert_latencies = []
    read_latencies = []

    for i in range(100):
        doc_ref = db.collection("latency_test").document(f"doc_{i}")

        
        start = time.time()
        doc_ref.set({"value": i, "timestamp": time.time()})
        insert_latencies.append(time.time() - start)

         
        start = time.time()
        doc_ref.get()
        read_latencies.append(time.time() - start)

    print("\n✅ Firestore Latency Test Completed.")
    print(f"📥 Avg Insert Latency: {sum(insert_latencies)/len(insert_latencies):.5f} s")
    print(f"📤 Avg Read Latency:   {sum(read_latencies)/len(read_latencies):.5f} s")
    print(f"📊 Insert Std Dev:     {statistics.stdev(insert_latencies):.5f}")
    print(f"📊 Read Std Dev:       {statistics.stdev(read_latencies):.5f}")

if __name__ == "__main__":
    print("\n🧪 Starting Firestore Latency Test...\n")
    measure_latency()
