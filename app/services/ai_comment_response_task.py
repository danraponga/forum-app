from app.core.db import sessionmanager
from app.core.utils import generate_ai_response
from app.models.comment import Comment
from app.models.common.enums.ai_roles import AIRoles
from app.repositories.comment_gateway import CommentDbGateway
from app.repositories.post_gateway import PostDbGateway
from app.schemas.comment import CreateAICommentDTO


async def create_comment_response_by_ai(dto: CreateAICommentDTO) -> None:
    async with sessionmanager.session() as db:
        post_gateway = PostDbGateway(db)
        comment_gateway = CommentDbGateway(db)
    post = await post_gateway.get_by_id(dto.post_id)
    if not post:
        return
    parent = await comment_gateway.get_by_id(dto.post_id, dto.parent_id)
    if not parent:
        return

    history = await parse_comments_history(comment_gateway, parent, post.id)
    ai_response = await generate_ai_response(post.content, history)

    comment = Comment(
        owner_id=post.owner_id,
        post_id=post.id,
        parent_id=parent.id,
        content=ai_response,
        is_ai=True,
    )
    await comment_gateway.create(comment)
    await db.close()


async def parse_comments_history(
    gateway: CommentDbGateway, parent: Comment, post_id: int
) -> list:
    prev = parent
    history = []
    while prev:
        role = AIRoles.USER.value
        if prev.is_ai:
            role = AIRoles.ASSISTANT.value
        elif prev.owner_id != parent.owner_id:
            break
        history.append({"role": role, "content": prev.content})
        prev = await gateway.get_by_id(post_id, prev.parent_id)
    return list(reversed(history))
