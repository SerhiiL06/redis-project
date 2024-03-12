import re
from datetime import datetime

from core.database import session
from src.presentation.DTO import PostDTO

from .validators import validate_post


class PostDomain:
    POST_KEY = "posts:"

    def all(self, category: str = None) -> list[PostDTO]:

        result = []

        if category:
            ids = session.smembers(f"category:{category}")
            for i in ids:
                retrieve = session.hgetall(i)
                reaction = self.add_reaction(i)
                retrieve.update({"post_id": i})
                retrieve["likes"] = reaction[0] if reaction[0] is not None else 0
                result.append(retrieve)
        else:
            for i in session.keys("posts:[0-9]"):
                retrieve = session.hgetall(i)
                reaction = self.add_reaction(i)
                retrieve.update({"post_id": i})
                retrieve["likes"] = reaction[0] if reaction[0] is not None else 0
                result.append(retrieve)
        result = sorted(result, key=lambda x: str(x.get("post_id")), reverse=True)
        return result

    @classmethod
    def add_reaction(cls, ids):
        return session.zmscore(
            "count:reaction", [re.findall(r":([0-9]{1,})", str(ids))[0]]
        )

    def create(self, data: PostDTO):
        errors = validate_post(data)
        if errors:
            return {"error": 400, "message": errors}

        increment = session.incrby("posts:count", 1)
        hash_key = self.POST_KEY + str(increment)
        session.rpush(f"user:posts:{data.owner_id}", hash_key)

        session.sadd(f"category:{data.category}", hash_key)
        session.hset(
            hash_key,
            mapping={
                "title": data.title,
                "desciption": data.description,
                "created": str(datetime.now()),
                "owner_id": data.owner_id,
            },
        )

        return {"ok": "create"}

    def detail(self, post_id: int) -> PostDTO:
        post = session.hgetall(self.POST_KEY + str(post_id))
        if not post:
            return {"error": "object doesnt exists"}
        return post

    def my_posts(self, user_id):
        posts_ids = session.lrange(f"user:posts:{user_id}", 0, -1)

        posts = []

        for i in posts_ids:
            post = session.hgetall(i)
            posts.append(post)
        return posts


class ReactionDomain:
    def __init__(self) -> None:
        self.repo = PostDomain()

    def like(self, post_id: int, user_id: int):
        check_exists = session.keys(f"posts:{post_id}")

        if not check_exists:
            return {"error": "post doesnt exists"}

        reaction_key = f"reaction:posts:{post_id}"
        reaction_count = f"count:reaction"
        if session.sismember(reaction_key, user_id) == 1:
            session.srem(reaction_key, user_id)
            session.zadd(reaction_count, mapping={post_id: -1}, incr=True)
            return {"ok": "like delete"}
        if session.sismember(reaction_key, user_id) == 0:
            session.sadd(reaction_key, user_id)
            session.zadd(reaction_count, mapping={post_id: 1}, incr=True)
            return {"ok": "like add"}
