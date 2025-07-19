import os
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv

def get_git_username():
    import subprocess
    result = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True)
    return result.stdout.strip()

def fetch_prompt():
    load_dotenv()
    MONGODB_URI = os.getenv("MONGODB_URI")
    client = MongoClient(MONGODB_URI)
    db = client["AI_Results"]
    
    tasks_col = db["Tasks"]
    commits_col = db["Commits"]

    git_user = get_git_username()

    tasks = list(tasks_col.find({"gitname": git_user}))
    if not tasks:
        print("❌ No tasks found for user:", git_user)
        return

    prompt_lines = [
        "You are an AI code reviewer helping track development progress.",
        "",
        "I have multiple tasks assigned to me, each with a task description and the list of code changes (diffs) made so far related to one of the task.",
        "",
        "Please analyze and return a JSON-style response with the following keys for each task:",
        "",
        "taskId: the unique ID of the task.",
        "progress percentage: Estimate from 0 to 100 how much of the task seems complete based on the code provided. If already fully implemented, use 100.",
        "progress helpfulness: True or False – does the new code help towards completing the task?",
        "relevance: Explain how relevant the code is to the task.",
        "reason: A short explanation for your estimate and judgment.",
        "",
        "My Tasks:"
    ]

    for task in tasks:
        task_id = task["_id"]
        description = task.get("description", "No description")
        commits = list(commits_col.find({"task_id": task_id}))
        code_diffs = "\n\n".join(commit.get("diff", "No diff") for commit in commits) if commits else "None"
        prompt_lines.append(f"\ntaskId: {str(task_id)}\nDescription: {description}\nCode Diff: {code_diffs}")

    prompt = "\n".join(prompt_lines)
    print("🔹 Gemini Prompt:\n")
    print(prompt)

# Call it
