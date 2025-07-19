import os
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv

def generate_task_commit_prompt(task_ids):
    load_dotenv()
    MONGODB_URI = os.getenv("MONGODB_URI")
    client = MongoClient(MONGODB_URI)
    db = client["AI_Results"]

    users_col = db["Users"]
    tasks_col = db["Tasks"]
    reasons_col = db["Reasons"]

    prompt_lines = []

    for idx, task_id in enumerate(task_ids):
        if isinstance(task_id, str):
            task_id = ObjectId(task_id)

        task = tasks_col.find_one({"_id": task_id})
        task_desc = task["task_description"] if task else "No description found"

        # Fetch all related commit_ids from Reasons collection
        reason_docs = reasons_col.find({"task_id": task_id})
        commit_ids = [doc.get("commit_id") for doc in reason_docs if doc.get("commit_id")]

        if commit_ids:
            code_diff = " + ".join(commit_ids)
        else:
            code_diff = "None"

        prompt_line = f"{idx}: {str(task_id)}: {task_desc} : Code diff {code_diff}"
        prompt_lines.append(prompt_line)

    # Step 3: Print prompt
    final_prompt = "\n".join(prompt_lines)
    return final_prompt