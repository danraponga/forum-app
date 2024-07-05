from better_profanity import profanity
from groq import AsyncGroq

from app.core.config import settings
from app.models.common.enums.ai_roles import AIRoles


def contains_profanity(content: str) -> bool:
    return profanity.contains_profanity(content)


async def generate_ai_response(post_content: str, history: list):
    client = AsyncGroq(api_key=settings.GROQ_API_KEY)
    messages = [
        {
            "role": AIRoles.SYSTEM.value,  # More about the roles - https://console.groq.com/docs/text-chat
            "content": settings.AI_PROMPT.format(post=post_content),
        }
    ]
    messages.extend(history)
    response = await client.chat.completions.create(
        messages=messages,
        model=settings.AI_MODEL,
    )
    return response.choices[0].message.content
