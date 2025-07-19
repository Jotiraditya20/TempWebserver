import os
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid, PyMongoError
from bson import ObjectId
from dotenv import load_dotenv

def add_reason_to_task(task_id, commit_id, reason_text, helpful_bool, relevance):
    try:
        if not all([task_id, commit_id, reason_text]):
            raise ValueError("Missing required fields")

        if isinstance(task_id, str):
            try:
                task_id = ObjectId(task_id)
            except Exception as e:
                raise ValueError(f"Invalid task_id format: {e}")
        
        load_dotenv()
        MONGODB_URI = os.getenv("MONGODB_URI")
        if not MONGODB_URI:
            raise EnvironmentError("MONGODB_URI not set in .env")

        client = MongoClient(MONGODB_URI)
        db = client["AI_Results"]
        reasons_col = db["Reasons"]

        result = reasons_col.insert_one({
            "task_id": task_id,
            "commit_id": commit_id,
            "reason": reason_text,
            "progress_helpful": bool(helpful_bool),
            "relevance": relevance,
            "timestamp": datetime.now()
        })

        print(f"✅ Reason added to Reasons collection with ID: {result.inserted_id}")
        return str(result.inserted_id)

    except (PyMongoError, ValueError, EnvironmentError) as e:
        print(f"❌ Failed to add reason: {e}")
        return None
