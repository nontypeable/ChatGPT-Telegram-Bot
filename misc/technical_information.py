import os

allowed_users = map(int, os.getenv("ALLOWED_USERS_ID").split(','))
old_message = ""
