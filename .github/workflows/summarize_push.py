import os
import requests
from summarizer import summarize_code_change
from MongoDB import AddSummaryToDB
from dotenv import load_dotenv
import json

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
GITHUB_EVENT_PATH = os.getenv("GITHUB_EVENT_PATH")

# Load GitHub event JSON
with open(GITHUB_EVENT_PATH, 'r') as f:
    event = json.load(f)

commit_sha = event['after']
repo_api = f"https://api.github.com/repos/{GITHUB_REPOSITORY}"
commit_url = f"{repo_api}/commits/{commit_sha}"

# Get commit details (JSON)
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
response = requests.get(commit_url, headers=headers)
commit_data = response.json()

# Extract committer info
committer_name = commit_data.get('commit', {}).get('committer', {}).get('name', 'Unknown')
committer_username = commit_data.get('committer', {}).get('login', 'Unknown')

# Optional: Get diff content
diff_headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3.diff"
}
diff_response = requests.get(commit_url, headers=diff_headers)
diff_code_text = diff_response.text

# Summarize and print
summary = summarize_code_change(diff_code_text)

print("🔍 Commit Info")
print(f"Committer Name: {committer_name}")
print(f"Committer GitHub Username: {committer_username}")
print(f"Commit URL: {commit_url}")
print("----- DIFF TEXT -----")
print(diff_code_text)
print("----- SUMMARY -----")
print(summary)

