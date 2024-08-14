# tars_discord_commands.py
import logging
from github_reader import get_file_content, get_repo_structure
from ai_utils import call_ai
from utils import send_long_message, generate_prompt

def setup_commands(bot):
    
    @bot.command(name='repo_chat')
    async def repo_chat(ctx, *, question):
        """Chat with the repository's codebase."""
        logging.info(f"Received repo_chat command: {question}")
        try:
            repo_content = await get_file_content(bot.repo, "README.md")
            context = f"Repository content:\n{repo_content}\n\nUser question: {question}"
            response = await call_ai(bot, question, context=context)
            await send_long_message(ctx, response)
        except Exception as e:
            await ctx.send(f"A cosmic disturbance prevented me from accessing the repository: {str(e)}")

    @bot.command(name='ai_chat')
    async def ai_chat(ctx, *, question):
        """Get assistance from the AI model."""
        logging.info(f"Received ai_chat command: {question}")
        try:
            response = await call_ai(bot, question)
            await send_long_message(ctx, response)
        except Exception as e:
            await ctx.send(f"The AI's response was lost in a wormhole: {str(e)}")

    @bot.command(name='analyze_code')
    async def analyze_code(ctx, file_path):
        """Analyze code from a specific file in the repository."""
        logging.info(f"Received analyze_code command for file: {file_path}")
        try:
            code_content = await get_file_content(bot.repo, file_path)
            prompt = f"Analyze the following code and provide insights:\n\n{code_content}"
            analysis = await call_ai(bot, prompt)
            await send_long_message(ctx, analysis)
        except Exception as e:
            await ctx.send(f"A black hole swallowed the code analysis: {str(e)}")

    @bot.command(name='generate_prompt')
    async def generate_prompt_command(ctx, file_path, *, task_description):
        """Generate a goal-oriented prompt based on the repo code and task description."""
        logging.info(f"Received generate_prompt command: {file_path}, {task_description}")
        try:
            repo_code = await get_file_content(bot.repo, file_path)
            prompt = generate_prompt(file_path, repo_code, task_description)
            response = await call_ai(bot, prompt)
            await send_long_message(ctx, response)
        except Exception as e:
            await ctx.send(f"The prompt generator malfunctioned in zero gravity: {str(e)}")

    @bot.command(name='dir')
    async def dir_command(ctx):
        """Display the repository file structure."""
        try:
            structure = await get_repo_structure(bot.repo)
            formatted_structure = "Repository Structure:\n```\n" + "\n".join(structure) + "\n```"
            await send_long_message(ctx, formatted_structure)
        except Exception as e:
            await ctx.send(f"The repository map was scrambled by solar radiation: {str(e)}")

    # Add more commands as needed

    logging.info("Discord commands setup complete")