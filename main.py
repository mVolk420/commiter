import os
import subprocess

from commiter.config import BASE_PATH
from commiter.git_utils import (
    is_git_repo,
    has_github_remote,
    has_changes,
    get_diff,
    commit_changes,
    push_changes,
)
from commiter.openai_utils import generate_commit_message


def scan_and_commit(base_path: str = BASE_PATH) -> None:
    for root, dirs, _ in os.walk(base_path):
        if is_git_repo(root) and has_github_remote(root):
            print(f"\U0001F4C1 GitHub-Repo gefunden: {root}")
            if has_changes(root):
                print(f"\U0001F501 \u00c4nderungen gefunden in {root}")
                subprocess.run(["git", "-C", root, "add", "-A"], check=True)
                diff = get_diff(root)
                if diff:
                    message = generate_commit_message(diff)
                    print(f"\U0001F4DD Commit-Message: {message}")
                    confirm = input("Commit message verwenden? (y/[n]): ").strip().lower()
                    if confirm == "y":
                        commit_changes(root, message)
                        push_changes(root)
                    else:
                        print("Commit abgebrochen.")
            dirs.clear()  # Unterordner nicht rekursiv prüfen


if __name__ == "__main__":
    scan_and_commit()
