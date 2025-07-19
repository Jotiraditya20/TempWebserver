import os
from get_user_task_ids import get_user_task_ids
from PromptGenProgress import generate_task_progress_prompt

git_username = os.getenv("GIT_USERNAME")

prompt = generate_task_progress_prompt(git_username)