import os
import shutil

def erase_git_repo(repo_path="."):
    git_dir = os.path.join(repo_path, ".git")
    if os.path.isdir(git_dir):
        shutil.rmtree(git_dir)
        print(f"Removed Git repository at: {git_dir}")
    else:
        print("No Git repository found at the specified path.")

# Call with the path to the repo (or leave blank for current directory)
erase_git_repo()