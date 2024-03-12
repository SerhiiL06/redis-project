from typing import Annotated

from fastapi import APIRouter, Depends

from src.domain.posts import PostDomain, ReactionDomain

from .DTO import PostDTO

post_router = APIRouter(tags=["posts"])


@post_router.get("/posts")
async def content_list(service: Annotated[PostDomain, Depends()], category: str = None):
    return service.all(category)


@post_router.post("/posts")
async def create_post(service: Annotated[PostDomain, Depends()], data: PostDTO):
    return service.create(data)


@post_router.get("/posts/my")
async def my_post(service: Annotated[PostDomain, Depends()], user_id: int):
    return service.my_posts(user_id)


@post_router.get("/posts/{post_id}")
async def retrieve_post(service: Annotated[PostDomain, Depends()], post_id: int):
    return service.detail(post_id)


@post_router.post("/posts/{post_id}/like")
async def post_reaction(
    service: Annotated[ReactionDomain, Depends()], post_id: int, user_id: int
):
    return service.like(post_id, user_id)
