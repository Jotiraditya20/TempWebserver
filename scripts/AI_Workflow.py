import os
from get_user_task_ids import get_user_task_ids

git_username = os.getenv("GIT_USERNAME")

user_task_ids = get_user_task_ids(git_username)
if user_task_ids == None:
    exit(1)

print(user_task_ids)
