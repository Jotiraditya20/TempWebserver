import os
import time
import google.generativeai as genai
from get_user_task_ids import get_user_task_ids
from PromptGenProgress import generate_task_progress_prompt

# --- Config ---
MODEL_NAME = "gemini-1.5-pro-latest"
MIN_DELAY_BETWEEN_REQUESTS = 12  # seconds (5 RPM)
last_call_time = 0

# --- Rate Limiter ---
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

# --- Main Logic ---
def main():
    git_username = input("Enter your GitHub username: ").strip()
    
    if not git_username:
        print("❌ GitHub username is required.")
        return

    # 1. Get user's tasks
    tasks = get_user_task_ids(git_username)
    if not tasks:
        print(f"❌ No tasks found for user: {git_username}")
        return

    # 2. Generate prompt
    prompt = generate_task_progress_prompt(git_username)
    print("📝 Prompt sent to Gemini:\n")
    print(prompt)
    
    # 3. Rate-limited call to Gemini
    rate_limited_call()
    try:
        response = model.generate_content(prompt)
        print("\n✅ Gemini Task Progress Report:\n")
        print(response.text.strip())
    except Exception as e:
        print(f"\n[ERROR calling Gemini]: {e}")

if __name__ == "__main__":
    main()
