import os
import google.generativeai as genai
from get_user_task_ids import get_user_task_ids
from PromptGenProgress import generate_task_progress_prompt
from dotenv import load_dotenv

# Load environment variables (ensure you have GOOGLE_API_KEY and GIT_USERNAME in .env)
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Step 1: Get GitHub username from env
git_username = os.getenv("GIT_USERNAME")
if not git_username:
    print("❌ GIT_USERNAME not found in .env or environment.")
    exit(1)

# Step 2: Generate the Gemini prompt
prompt = generate_task_progress_prompt(git_username)

if not prompt:
    print("❌ Could not generate prompt.")
    exit(1)

# Step 3: Use Gemini 2.5 Pro to get the result
model = genai.GenerativeModel("gemini-1.5-pro-latest")
response = model.generate_content(prompt)

# Step 4: Print result
print("🧠 Gemini 2.5 Response:\n")
print(response.text)
