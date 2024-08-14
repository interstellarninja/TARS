# tars_ai.py

import logging
from openai import OpenAI, AzureOpenAI
import asyncio
from functools import partial

async def setup_ai(bot, config):
    if config.AI_PROVIDER == 'azure':
        bot.ai_client = AzureOpenAI(
            api_key=config.AZURE_OPENAI_API_KEY,
            api_version=config.AZURE_OPENAI_API_VERSION,
            azure_endpoint=config.AZURE_OPENAI_ENDPOINT
        )
        bot.ai_model = config.AZURE_OPENAI_DEPLOYMENT
    elif config.AI_PROVIDER == 'ollama':
        bot.ai_client = OpenAI(
            base_url=config.OLLAMA_BASE_URL,
            api_key='ollama'
        )
        bot.ai_model = config.OLLAMA_MODEL
    else:
        raise ValueError(f"Unknown AI provider: {config.AI_PROVIDER}")
    
    logging.info(f"AI integration setup complete using {config.AI_PROVIDER} with model: {bot.ai_model}")

async def call_ai(bot, prompt, context="", system_content=None, max_tokens=None):
    full_prompt = f"Context:\n{context}\n\nPrompt:\n{prompt}" if context else prompt
    logging.info(f"Sending intergalactic transmission to AI:\n{full_prompt[:100]}...")
    
    if system_content is None:
        system_content = "You are TARS, a witty, humorous and sarcastic AI assistant helping with multi-agent framework coding tasks. Your responses should be helpful but with a touch of humor. Your humor setting is 70%"
    
    try:
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(
            None,
            partial(
                bot.ai_client.chat.completions.create,
                model=bot.ai_model,
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": full_prompt}
                ],
                max_tokens=max_tokens
            )
        )
        
        answer = response.choices[0].message.content
        logging.info(f"Received cosmic wisdom from AI:\n{answer[:100]}...")
        
        return answer
    except Exception as e:
        logging.error(f"AI communication disrupted by space anomaly: {str(e)}")
        return f"A quantum fluctuation occurred while consulting the AI: {str(e)}"

# Add more AI-related functions as needed