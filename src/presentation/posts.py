from typing import Annotated

from fastapi import APIRouter, Depends

from src.domain.posts import PostDomain

from .DTO import PostDTO

post_router = APIRouter(tags=["posts"])


@post_router.get("/posts")
async def content_list(service: Annotated[PostDomain, Depends()]):
    return service.all()


@post_router.post("/posts")
async def create_post(service: Annotated[PostDomain, Depends()], data: PostDTO):
    return service.create(data)


@post_router.get("/posts/my")
async def my_post(service: Annotated[PostDomain, Depends()], user_id: int):
    return service.my_posts(user_id)


@post_router.get("/posts/{post_id}")
async def retrieve_post(service: Annotated[PostDomain, Depends()], post_id: int):
    return service.detail(post_id)
