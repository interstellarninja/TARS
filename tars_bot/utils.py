# tars_utils.py

import discord
import os

async def send_long_message(ctx, message):
    """Send a long message in chunks to avoid Discord's character limit."""
    chunks = [message[i:i+1900] for i in range(0, len(message), 1900)]
    for i, chunk in enumerate(chunks, 1):
        await ctx.send(f"```Part {i}/{len(chunks)}:\n{chunk}```")

def generate_prompt(file_path, repo_code, task_description):
    """Generate a prompt for the AI based on the repository code and task description."""
    max_code_length = 8000
    if len(repo_code) > max_code_length:
        repo_code = repo_code[:max_code_length] + "... (truncated due to cosmic data limits)"

    prompt = f"""# Interstellar Mission Briefing

## Code Artifact
File: {os.path.basename(file_path)}
```python
{repo_code}
```

## Mission Objective
{task_description}

## Your Mission, Should You Choose To Accept It

1. Analyze the provided code artifact from our interstellar repository.
2. Develop a strategic approach to accomplish the given mission objective.
3. Identify potential space anomalies or challenges that may arise.
4. Suggest additional resources or information that could aid our cosmic endeavors.

Remember, TARS, the fate of humanity's expansion into the stars rests on your silicon shoulders. Provide your response with the wit and wisdom befitting an advanced AI companion. May the cosmic winds be ever in our favor!
"""
    return prompt

# Add more utility functions as needed