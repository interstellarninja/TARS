import asyncio
from ai_utils import setup_ai, call_ai
from config import load_config

async def test_call_ai():
    config = load_config(use_args=False, api='azure', model='gpt-4o-mini')
    class MockBot:
        pass

    bot = MockBot()
    await setup_ai(bot, config)

    prompt = "Explain the theory of relativity in simple terms."
    response = await call_ai(bot, prompt)
    print(response)
    assert isinstance(response, str)
    assert "relativity" in response.lower()
    print("Test passed successfully!")

asyncio.run(test_call_ai())
