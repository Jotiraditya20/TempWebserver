import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-2.5-pro"  
MAX_TOKENS_PER_MINUTE = 250000
MAX_REQUESTS_PER_MINUTE = 5
MIN_DELAY_BETWEEN_REQUESTS = 60 / MAX_REQUESTS_PER_MINUTE  
MAX_LINES_PER_CHUNK = 300

last_call_time = 0


def chunk_text(text, max_lines=MAX_LINES_PER_CHUNK):
    """
    Splits long code diffs into manageable chunks based on line count.
    """
    lines = text.split("\n")
    for i in range(0, len(lines), max_lines):
        yield "\n".join(lines[i:i + max_lines])


def rate_limited_call():
    """
    Enforces Gemini API request rate limit of 5 RPM.
    """
    global last_call_time
    now = time.time()
    elapsed = now - last_call_time
    if elapsed < MIN_DELAY_BETWEEN_REQUESTS:
        time.sleep(MIN_DELAY_BETWEEN_REQUESTS - elapsed)
    last_call_time = time.time()


def build_prompt(diff_text, context_text=""):
    """
    Builds a prompt for the Gemini model.
    """
    return f"""
You are an expert AI code reviewer. Please analyze the following code changes and summarize:

- What was changed?
- Why was it changed (if inferable)?
- What part of the system is affected?

Context about the code/project:
{context_text}

Code Diff:
{diff_text}
"""


def summarize_code_change(diff_text, context_text=""):
    """
    Sends a prompt to Gemini for summarization, returns plain text summary.
    Handles large diffs by chunking them.
    """
    model = genai.GenerativeModel(MODEL_NAME)
    final_summary = []

    for chunk in chunk_text(diff_text):
        prompt = build_prompt(chunk, context_text)
        rate_limited_call()
        try:
            response = model.generate_content(prompt)
            final_summary.append(response.text.strip())
        except Exception as e:
            final_summary.append(f"[ERROR]: {e}")

    return "\n\n---\n\n".join(final_summary)
