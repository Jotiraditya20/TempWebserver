import os
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv

def generate_task_progress_prompt(git_username):
    load_dotenv()
    MONGODB_URI = os.getenv("MONGODB_URI")
    client = MongoClient(MONGODB_URI)
    db = client["AI_Results"]

    users_col = db["Users"]
    tasks_col = db["Tasks"]
    reasons_col = db["Reasons"]
    summaries_col = db["summaries"]

    git_username = git_username.strip()

    # Step 1: Get user
    user = users_col.find_one({"gitname": git_username})
    if not user:
        print("❌ User not found.")
        return ""

    task_ids = user.get("taskIds", [])
    prompt_blocks = []

    for task_id in task_ids:
        if isinstance(task_id, str):
            task_id = ObjectId(task_id)

        task = tasks_col.find_one({"_id": task_id})
        task_desc = task.get("description", "No description found")

        # Get related commit IDs from Reasons collection
        reason_docs = reasons_col.find({"task_id": task_id})
        commit_ids = [doc.get("commit_id") for doc in reason_docs if doc.get("commit_id")]

        # Fetch corresponding codediffs from summaries
        code_diffs = []
        for cid in commit_ids:
            summary_doc = summaries_col.find_one({"commit_id": cid})
            if summary_doc and "codediff" in summary_doc:
                code_diffs.append(f"Commit: {cid}\n{summary_doc['codediff']}")

        code_diff_text = "\n\n".join(code_diffs) if code_diffs else "None"

        prompt_blocks.append(f"""
taskId: {str(task_id)}
Description: {task_desc}
Code Diff:
{code_diff_text}
""".strip())

    full_prompt = """
You are an AI code reviewer helping track development progress.

Analyze each task below and return the following for **each** task in this JSON-style format:

{
  "taskId": "<task_id>",
  "progress percentage": <0-100>,
  "progress helpfulness": true/false,
  "relevance": "<reason why this commit/code is or isn't relevant to the task>",
  "reason": "<short reasoning for progress percentage and helpfulness>"
}

Tasks:
""" + "\n\n".join(prompt_blocks)

    print("🔹 Gemini Prompt:\n")
    print(full_prompt)
    return full_prompt
