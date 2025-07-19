import os
from datetime import datetime
import requests
from summarizer import summarize_code_change
from MongoDB import AddSummaryToDB
from dotenv import load_dotenv
import json

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")  # e.g. Jotiraditya20/TempWebserver
GITHUB_EVENT_PATH = os.getenv("GITHUB_EVENT_PATH")

# Load GitHub event JSON
with open(GITHUB_EVENT_PATH, 'r') as f:
    event = json.load(f)

commit_sha = event.get('after')
branch_ref = event.get('ref')  # e.g. 'refs/heads/master'
branch = branch_ref.replace('refs/heads/', '') if branch_ref else 'unknown'

# Construct repo URL
repo_url = f"https://github.com/{GITHUB_REPOSITORY}"

# Get commit diff
commit_url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/commits/{commit_sha}"
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3.diff"
}
diff_response = requests.get(commit_url, headers=headers)
diff_code_text = diff_response.text

# Get commit details (JSON)
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
response = requests.get(commit_url, headers=headers)
commit_data = response.json()
committer_name = commit_data.get('commit', {}).get('committer', {}).get('name', 'Unknown')
committer_username = commit_data.get('committer', {}).get('login', 'Unknown')

# Summarize
summary = summarize_code_change(diff_code_text)

# 🔍 Print Required Info
'''print("===== GitHub Commit Info =====")
print(f"📦 Repository: {repo_url}")
print(f"🌿 Branch: {branch}")
print(f"🔐 Commit ID: {commit_sha}")
print(f"🔗 Commit URL: {commit_url}")
print("===== Code Diff Summary =====")
print(summary)'''

summary_of_code = {
    "repo_meta": {
        "repo": repo_url,
        "branch": branch,
        "author": committer_username
    },
    "commit_id": commit_sha,
    "summary": summary,
    "codediff": diff_code_text,
    "timestamp": datetime.now()  # must be datetime, not string
}
print(summary_of_code)