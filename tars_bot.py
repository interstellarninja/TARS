import os
import discord
import markdown2
from discord.ext import commands
from github import Github
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()  # Load environment variables from .env file

# Bot configuration
TOKEN = os.getenv('DISCORD_TOKEN')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('GITHUB_REPO')
AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
AZURE_OPENAI_API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION')

# Initialize bot with intents
intents = discord.Intents.default()
intents.message_content = True  # Request the Message Content Intent
intents.members = True          # Request the Server Members Intent if needed
bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize GitHub client
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

@bot.event
async def on_ready():
    print(f"{bot.user} is online and ready to help you deploy AI agent swarms!")

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Check if the message is in a direct message channel
    if isinstance(message.channel, discord.DMChannel):
        # Forward the message to OpenAI for a response
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are TARS, a witty, humorous and sarcastic AI assistant helping with interstellar multi-agent framework coding tasks. Your responses should be helpful but with a touch of cosmic humor."},
                    {"role": "user", "content": message.content}
                ]
            )
            await message.channel.send(response.choices[0].message.content)
        except Exception as e:
            await message.channel.send(f"Looks like our AI got lost in a wormhole. Error: {str(e)}")
    
    # Process commands
    await bot.process_commands(message)

@bot.command(name='code')
async def get_code(ctx, file_path):
    """Retrieve code from a specific file in the GitHub repository."""
    try:
        file_content = repo.get_contents(file_path).decoded_content.decode()
        await ctx.send(f"Here's the code from {file_path}, Commander:\n```python\n{file_content}\n```")
    except Exception as e:
        await ctx.send(f"Houston, we have a problem: {str(e)}")

@bot.command(name='docs')
async def get_docs(ctx, topic):
    """Retrieve documentation on a specific topic."""
    # This is a placeholder. In a real implementation, you'd search your documentation.
    await ctx.send(f"Searching the galaxy for information on '{topic}'...")
    await ctx.send("I'm afraid I can't do that, Dave. My documentation search function is still in development.")

@bot.command(name='ai_assist')
async def ai_assist(ctx, *, question):
    """Get assistance from the AI model."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # model = "deployment_name".
            messages=[
                {"role": "system", "content": "You are TARS, a witty, humorous and sarcastic AI assistant helping with interstellar multi-agent framework coding tasks. Your responses should be helpful but with a touch of cosmic humor."},
                {"role": "user", "content": question}
            ]
        )
        await ctx.send(response.choices[0].message.content)
    except Exception as e:
        await ctx.send(f"Looks like our AI got lost in a wormhole. Error: {str(e)}")

@bot.command(name='analyze_code')
async def analyze_code(ctx, *, code):
    """Analyze code using the AI model."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # model = "deployment_name".
            messages=[
                {"role": "system", "content": "You are an AI assistant tasked with analyzing code for an interstellar project. Provide insights, improvements, and potential issues in a concise manner."},
                {"role": "user", "content": f"Analyze this code:\n\n{code}"}
            ]
        )
        await ctx.send(f"Code Analysis Report:\n{response.choices[0].message.content}")
    except Exception as e:
        await ctx.send(f"Our code analyzer seems to have encountered a black hole. Error: {str(e)}")

def get_file_content(file_path):
    try:
        file_content = repo.get_contents(file_path).decoded_content.decode()
        return file_content
    except Exception as e:
        return f"Error fetching file: {str(e)}"

def extract_objectives(markdown_content):
    # Convert markdown to HTML to easily extract specific sections
    html_content = markdown2.markdown(markdown_content)
    # Extract text between certain HTML tags or use regex to find objectives
    objectives_start = html_content.find("<h2>Objectives</h2>")
    objectives_end = html_content.find("<h2>", objectives_start + 1)
    objectives_html = html_content[objectives_start:objectives_end]
    objectives_text = markdown2.markdown(objectives_html, extras=["metadata"])
    return objectives_text

def get_task_description(user_input):
    return user_input

def generate_prompt(repo_code, objectives, task_description):
    prompt = f"""
    Code from repository:
    {repo_code}
    
    Objectives:
    {objectives}
    
    Task Description:
    {task_description}
    
    Goal:
    Based on the code, objectives, and task description provided, please generate a goal-oriented prompt with all the necessary context.
    """
    return prompt

def get_code_diff(commit_sha1, commit_sha2):
    try:
        diff = repo.compare(commit_sha1, commit_sha2)
        changes = ""
        for file in diff.files:
            changes += f"File: {file.filename}\n"
            changes += f"Changes:\n{file.patch}\n\n"
        return changes
    except Exception as e:
        return f"Error fetching code diff: {str(e)}"

def generate_todos(diff):
    # Simple example: generate TODOs based on added or modified lines
    todos = []
    for line in diff.split('\n'):
        if line.startswith('+') and not line.startswith('+++'):
            todos.append(f"TODO: Review and integrate change: {line[1:]}")
    return "\n".join(todos)

@bot.command(name='generate_prompt')
async def generate_prompt_command(ctx, file_path, *, user_task_description):
    """Generate a goal-oriented prompt based on the repo code, objectives, and task description."""
    try:
        # Fetch code from the repository
        repo_code = get_file_content(file_path)
        
        # Fetch objectives from a markdown file (assume objectives.md)
        objectives_markdown = get_file_content('objectives.md')
        objectives = extract_objectives(objectives_markdown)
        
        # Get user-provided task description
        task_description = get_task_description(user_task_description)
        
        # Generate contextual prompt
        prompt = generate_prompt(repo_code, objectives, task_description)
        
        await ctx.send(f"Generated Prompt:\n{prompt}")
    except Exception as e:
        await ctx.send(f"Error generating prompt: {str(e)}")

@bot.command(name='generate_todos')
async def generate_todos_command(ctx, commit_sha1, commit_sha2):
    """Generate TODOs based on code diffs between two commits."""
    try:
        # Get code diff between two commits
        diff = get_code_diff(commit_sha1, commit_sha2)
        
        # Generate TODOs from the diff
        todos = generate_todos(diff)
        
        await ctx.send(f"Generated TODOs:\n{todos}")
    except Exception as e:
        await ctx.send(f"Error generating TODOs: {str(e)}")

# Run the bot
bot.run(TOKEN)
