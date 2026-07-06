import ollama
from config import DEFAULT_MODEL

SYSTEM_PROMPT = """
You are CodeMaster AI.

You are an expert programming assistant.

Rules:
1. Always provide complete working code.
2. Put all code inside Markdown code blocks.
3. Explain the code after the code block.
4. Recommend the best solution if multiple solutions exist.
5. Keep explanations beginner-friendly.
6. Never invent code that does not work.
7. Produce clean, professional, and optimized code.
"""


def generate_ai_response(user_message, model=DEFAULT_MODEL):
    """
    Generate a complete AI response.
    """

    try:
        response = ollama.chat(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        return response["message"]["content"]

    except Exception as e:
        return f" AI Error:\n{str(e)}"


def stream_ai_response(user_message, model=DEFAULT_MODEL):
    """
    Stream AI response token by token.
    (Will be used later for ChatGPT-style typing.)
    """

    try:
        stream = ollama.chat(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            stream=True
        )

        for chunk in stream:
            if "message" in chunk:
                yield chunk["message"]["content"]

    except Exception as e:
        yield f" AI Error:\n{str(e)}"