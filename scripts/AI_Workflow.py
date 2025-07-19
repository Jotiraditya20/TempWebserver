import os
from get_user_task_ids import get_user_task_ids
from PromptGenProgress import generate_task_commit_prompt

git_username = os.getenv("GIT_USERNAME")

ruless_prompt = generate_task_commit_prompt(git_username)
print(ruless_prompt)