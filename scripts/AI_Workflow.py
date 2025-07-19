import os
from get_user_task_ids import get_user_task_ids
from PromptGenProgress import fetch_prompt

git_username = os.getenv("GIT_USERNAME")

ruless_prompt = fetch_prompt()