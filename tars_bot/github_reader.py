# tars_github.py

from github import Github, GithubException
import logging
import asyncio
from collections import deque

class GithubRateLimiter:
    def __init__(self, calls_per_hour=5000):
        self.calls_per_hour = calls_per_hour
        self.call_times = deque(maxlen=calls_per_hour)

    async def wait(self):
        now = asyncio.get_event_loop().time()
        if len(self.call_times) == self.calls_per_hour:
            oldest_call = self.call_times[0]
            wait_time = 3600 - (now - oldest_call)
            if wait_time > 0:
                await asyncio.sleep(wait_time)
        self.call_times.append(now)

github_rate_limiter = GithubRateLimiter()

async def setup_github(bot, config):
    bot.github_client = Github(config.GITHUB_TOKEN)
    bot.repo = bot.github_client.get_repo(config.REPO_NAME)
    logging.info(f"GitHub integration setup complete for repo: {config.REPO_NAME}")

async def get_file_content(repo, file_path):
    try:
        await github_rate_limiter.wait()
        file_content = repo.get_contents(file_path)
        if file_content.size > 1000000:  # 1MB limit
            return "File is too large for interstellar transmission."
        return file_content.decoded_content.decode('utf-8')
    except UnicodeDecodeError:
        return "File contains non-UTF-8 encoded data. Perhaps alien encryption?"
    except GithubException as e:
        logging.error(f"Failed to fetch file from GitHub: {e}")
        return f"A space anomaly occurred: {str(e)}"

async def get_repo_structure(repo, path="", prefix=""):
    try:
        await github_rate_limiter.wait()
        if not path:
            structure = [f"{repo.name}/"]
            prefix = "  "
        else:
            structure = []

        contents = repo.get_contents(path)
        for i, content in enumerate(contents):
            is_last = (i == len(contents) - 1)
            if content.type == "dir":
                structure.append(f"{prefix}{'└── ' if is_last else '├── '}{content.name}/")
                structure.extend(await get_repo_structure(repo, content.path, prefix + ('    ' if is_last else '│   ')))
            else:
                structure.append(f"{prefix}{'└── ' if is_last else '├── '}{content.name}")
        
        return structure
    except GithubException as e:
        logging.error(f"Failed to get repo structure: {e}")
        return ["Error: Space debris interfering with repository scan."]

# Add more GitHub-related functions as needed