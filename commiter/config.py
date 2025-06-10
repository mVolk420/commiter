import os
from dotenv import load_dotenv

load_dotenv()

BASE_PATH = os.getenv("PROJECT_BASE_PATH")
if not BASE_PATH or not os.path.isdir(BASE_PATH):
    raise ValueError("PROJECT_BASE_PATH ist nicht gesetzt oder ungültig.")
