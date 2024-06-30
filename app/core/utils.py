from better_profanity import profanity
from groq import Groq

from app.core.config import settings


def contains_profanity(content: str) -> bool:
    return profanity.contains_profanity(content)


def generate_ai_response(post: str, comment: str):
    client = Groq(api_key=settings.AI_API_KEY)
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": settings.AI_PROMPT.format(post=post, comment=comment),
            },
        ],
        model=settings.AI_MODEL,
    )
    return response.choices[0].message.content
