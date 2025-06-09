import os
import subprocess
from dotenv import load_dotenv
from openai import OpenAI

# .env laden
load_dotenv()

# OpenAI-Client initialisieren
client = OpenAI()

# Projektverzeichnis aus .env
base_path = os.getenv("PROJECT_BASE_PATH")

if not base_path or not os.path.isdir(base_path):
    raise ValueError("PROJECT_BASE_PATH ist nicht gesetzt oder ungültig.")

def is_git_repo(path):
    return os.path.isdir(os.path.join(path, ".git"))

def has_github_remote(path):
    try:
        remotes = subprocess.check_output(["git", "-C", path, "remote", "-v"]).decode()
        return any("github.com" in line for line in remotes.splitlines())
    except subprocess.CalledProcessError:
        return False

def has_changes(path):
    try:
        status = subprocess.check_output(["git", "-C", path, "status", "--porcelain"]).decode()
        return bool(status.strip())
    except subprocess.CalledProcessError:
        return False

def get_diff(path):
    try:
        return subprocess.check_output(["git", "-C", path, "diff"]).decode()
    except subprocess.CalledProcessError:
        return ""

def generate_commit_message(diff):
    prompt = f"Write a concise and clear git commit message summarizing the following diff:\n{diff}\n"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who writes concise git commit messages."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100
    )
    return response.choices[0].message.content.strip()

def commit_changes(path, message):
    subprocess.run(["git", "-C", path, "add", "."], check=True)
    subprocess.run(["git", "-C", path, "commit", "-m", message], check=True)

def push_changes(path):
    subprocess.run(["git", "-C", path, "push"], check=True)

def scan_and_commit(base_path):
    for root, dirs, _ in os.walk(base_path):
        if is_git_repo(root) and has_github_remote(root):
            print(f"📁 GitHub-Repo gefunden: {root}")
            if has_changes(root):
                print(f"🔄 Änderungen gefunden in {root}")
                diff = get_diff(root)
                if diff:
                    message = generate_commit_message(diff)
                    print(f"📝 Commit-Message: {message}")
                    commit_changes(root, message)
                    push_changes(root)
            #dirs.clear()  # Unterordner nicht rekursiv prüfen

if __name__ == "__main__":
    scan_and_commit(base_path)
