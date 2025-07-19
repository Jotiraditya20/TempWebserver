import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

#Test Summary
summary = {
    "repo_meta": {
        "repo": "github.com/Jotiraditya20/TempWebserver",
        "branch": "master",
        "author": "Jotiraditya20"
    },
    "diffcode": "This is a test",
    "commit_id": "a1b2c3d4e5",
    "summary": "Refactored login logic and added tests.",
    "timestamp": datetime.now()  # must be datetime, not string
}

def AddSummaryToDB(data=summary):
    load_dotenv()
    MONGO_URI = os.getenv("MONGODB_URI")
    if not MONGO_URI:
        print("MONGODB_URI not Found!")
        exit(0)
    client = MongoClient(MONGO_URI)
    db = client["AI_Results"]
    collection = db["summaries"]
    result = collection.insert_one(data)
    print(f"✅ Inserted into time series collection with ID: {result.inserted_id}")
    return None
