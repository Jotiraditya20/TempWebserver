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

with open(GITHUB_EVENT_PATH, 'r') as f:
    event = json.load(f)

commit_sha = event['after'] # Takes latest Commit
repo_api = f"https://api.github.com/repos/{GITHUB_REPOSITORY}"
diff_url = f"{repo_api}/commits/{commit_sha}"

#To get the code change
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3.diff"
}
response = requests.get(diff_url, headers=headers)
diff_code_text = response.text
summary = summarize_code_change(diff_code_text)
print("This is a Test")
print(diff_url)
print(diff_code_text)
print(summary)
AddSummaryToDB()
