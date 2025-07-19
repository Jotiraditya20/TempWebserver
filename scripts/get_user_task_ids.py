import os
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv

def get_user_task_ids(git_username):
    load_dotenv()
    MONGODB_URI = os.getenv("MONGODB_URI")

    client = MongoClient(MONGODB_URI)
    db = client["AI_Results"]
    users_col = db["Users"]

    user_doc = users_col.find_one({"gitname": git_username})
    if not user_doc:
        print("❌ User not found.")
        return None

    task_ids = user_doc.get("Taskids", [])
    print(f"📋 Task IDs for user '{git_username}':")
    for i, tid in enumerate(task_ids):
        print(f"{i + 1}. {str(tid)}")

    return task_ids