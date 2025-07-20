import os
import google.generativeai as genai
from get_user_task_ids import get_user_task_ids
from PromptGenProgress import generate_task_progress_prompt
from dotenv import load_dotenv
import google.generativeai as genai
import time

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

# --- Constants ---
MODEL_NAME = "gemini-2.5-pro"
MIN_DELAY_BETWEEN_REQUESTS = 12       # Rate limit: 5 requests per minute
last_call_time = 0


# --- Rate Limiting Function ---
def rate_limited_call():
    global last_call_time
    now = time.time()
    elapsed = now - last_call_time
    if elapsed < MIN_DELAY_BETWEEN_REQUESTS:
        time.sleep(MIN_DELAY_BETWEEN_REQUESTS - elapsed)
    last_call_time = time.time()

# --- Gemini Setup ---
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel(MODEL_NAME)

# --- Function to Call Gemini ---
def send_prompt_to_gemini(prompt_text):
    rate_limited_call()
    try:
        response = model.generate_content(prompt_text)
        response = response.text.strip()
        print("\n🧠 Gemini Response:\n")
    except Exception as e:
        print(f"[❌ Gemini Error]: {e}")
    return response

response = send_prompt_to_gemini(prompt)
print(response)