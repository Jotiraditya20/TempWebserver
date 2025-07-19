import os
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
from keybert import KeyBERT
from bson import ObjectId
from dotenv import load_dotenv

# Load .env and DB
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    print("MONGODB_URI not Found!")
    exit(0)

client = MongoClient(MONGODB_URI)
db = client["AI_Results"]

# ---------- Ensure Time Series Collection ----------
def ensure_tasks_collection():
    if "Tasks" not in db.list_collection_names():
        try:
            db.create_collection(
                name="Tasks",
                timeseries={
                    "timeField": "timestamp",
                    "granularity": "seconds"
                }
            )
            print("✅ Created time series collection: Tasks")
        except CollectionInvalid as e:
            print(f"❌ Collection creation failed: {e}")

# ---------- Create User ----------
def create_user(name, gitname):
    existing = db.Users.find_one({"gitname": gitname})
    if existing:
        print("⚠️ User already exists.")
        return
    db.Users.insert_one({
        "name": name,
        "gitname": gitname,
        "taskIds": [],
        "completion": []
    })
    print(f"✅ User {gitname} created.")

# ---------- Create Task ----------
def Create_Task(Title, Description, AssignedTo):
    ensure_tasks_collection()
    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(
        Description,
        keyphrase_ngram_range=(1, 2),
        stop_words='english',
        top_n=10
    )

    data = {
        "Title": Title,
        "description": Description,
        "assigned_to": AssignedTo,
        "keywords": keywords,
        "commits": [],
        "timestamp": datetime.now()
    }

    result = db.Tasks.insert_one(data)
    print(f"✅ Task inserted with ID: {result.inserted_id}")
    return result.inserted_id

# ---------- Add Task to User with 0–100% Completion ----------
def add_task_to_user(gitname, task_id, completion_percent=0):
    task_oid = ObjectId(task_id) if not isinstance(task_id, ObjectId) else task_id

    # Ensure value is within 0–100
    if not (0 <= completion_percent <= 100):
        print("❌ Completion must be between 0 and 100.")
        return

    result = db.Users.update_one(
        {"gitname": gitname},
        {"$push": {
            "taskIds": task_oid,
            "completion": completion_percent
        }}
    )
    if result.modified_count:
        print(f"✅ Linked task {task_oid} to user {gitname} with {completion_percent}% completion")
    else:
        print("⚠️ Failed to link task — user not found.")

# ---------- Delete Task ----------
def delete_task(task_id):
    load_dotenv()
    MONGODB_URI = os.getenv("MONGODB_URI")
    client = MongoClient(MONGODB_URI)
    db = client["AI_Results"]

    users_col = db["Users"]
    tasks_col = db["Tasks"]
    history_col = db["TaskHistory"]
    reasons_col = db["Reasons"]
    task_oid = ObjectId(task_id) if not isinstance(task_id, ObjectId) else task_id

    # 1. Remove from Tasks collection
    task = db.Tasks.find_one({"_id": task_oid})
    if not task:
        print("❌ Task not found in Tasks collection.")
        return

    db.Tasks.delete_one({"_id": task_oid})
    print(f"🗑️ Deleted task from Tasks collection: {task_oid}")

    # 2. Remove from assigned user's taskIds + completion
    gitname = task.get("assigned_to")
    user = db.Users.find_one({"gitname": gitname})

    if not user:
        print("⚠️ Assigned user not found.")
        return

    task_ids = user.get("taskIds", [])
    if task_oid in task_ids:
        index = task_ids.index(task_oid)

        # Step 1: remove taskId and unset corresponding completion index
        db.Users.update_one(
            {"gitname": gitname},
            {
                "$pull": {"taskIds": task_oid},
                "$unset": {f"completion.{index}": ""}
            }
        )
        # Step 2: remove null from completion
        db.Users.update_one(
            {"gitname": gitname},
            {"$pull": {"completion": None}}
        )
        print(f"🧹 Removed task ID and its completion from user: {gitname}")
    else:
        print("⚠️ Task ID not found in user's task list.")


#-----Edit %---------
def update_completion_by_index(gitname, index, new_percent):
    if not (0 <= new_percent <= 100):
        print("❌ Completion must be between 0 and 100.")
        return

    user = users_col.find_one({"gitname": gitname})
    if not user:
        print("❌ User not found.")
        return

    task_ids = user.get("taskIds", [])
    completions = user.get("completion", [])

    if index < 0 or index >= len(task_ids):
        print("❌ Invalid index.")
        return

    task_id = task_ids[index]
    field = f"completion.{index}"

    users_col.update_one({"gitname": gitname}, {"$set": {field: new_percent}})
    print(f"✅ Updated completion of task {task_id} to {new_percent}%")

    if new_percent == 100:
        # Insert into TaskHistory
        history_col.insert_one({
            "task_id": task_id,
            "completed_by": gitname,
            "timestamp": datetime.now()
        })

        # Remove task from user's list
        users_col.update_one(
            {"gitname": gitname},
            {
                "$unset": {f"taskIds.{index}": "", f"completion.{index}": ""},
            }
        )
        # Clean up array nulls (rebuild without None)
        users_col.update_one(
            {"gitname": gitname},
            {
                "$pull": {"taskIds": None, "completion": None}
            }
        )
        print("🧹 Task completed and removed from user's list.")


# ---------- Example Usage ----------
if __name__ == "__main__":
    # ✅ Create user once
    #create_user("Jotir Aditya", "Jotiraditya20")

    # ✅ Create task and link it with 25% done
    '''task_id = Create_Task(
        "Build CLI login system",
        "Make a CLI app to register/login using JSON storage and password hashing.",
        "Jotiraditya20"
    )'''
    #add_task_to_user("Jotiraditya20", task_id)

    # 🗑️ Delete task (if needed)
    delete_task("687bec215db2915eea231d17")