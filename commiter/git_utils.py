import os
import subprocess


def is_git_repo(path: str) -> bool:
    return os.path.isdir(os.path.join(path, ".git"))


def has_github_remote(path: str) -> bool:
    try:
        remotes = subprocess.check_output(["git", "-C", path, "remote", "-v"]).decode()
        return any("github.com" in line for line in remotes.splitlines())
    except subprocess.CalledProcessError:
        return False


def has_changes(path: str) -> bool:
    try:
        status = subprocess.check_output(["git", "-C", path, "status", "--porcelain"]).decode()
        return bool(status.strip())
    except subprocess.CalledProcessError:
        return False


def get_diff(path: str) -> str:
    """Return the diff of staged changes for the given git repository."""
    try:
        return subprocess.check_output([
            "git",
            "-C",
            path,
            "diff",
            "--staged",
        ]).decode()
    except subprocess.CalledProcessError:
        return ""


def commit_changes(path: str, message: str) -> None:
    subprocess.run(["git", "-C", path, "add", "."], check=True)
    subprocess.run(["git", "-C", path, "commit", "-m", message], check=True)


def push_changes(path: str) -> None:
    try:
        subprocess.run(["git", "-C", path, "push"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to push changes in {path}: {e}")
