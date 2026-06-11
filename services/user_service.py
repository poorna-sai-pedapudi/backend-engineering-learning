import json
import logging 

from database import cursor
from redis_client import redis_client
from fastapi import HTTPException
from utils import build_user_response, error_response

logger = logging.getLogger(__name__)

def get_user_by_id(id: int):

    logger.info(f"[USERS] Fetch user id={id}")

    cache_key = f"user:{id}"

    cached_user = redis_client.get(cache_key)

    if cached_user:
        logger.info(f"[CACHE] Cache HIT for user id = {id}")

        return json.loads(cached_user)
    
    logger.info(f"[CACHE] Cache MISS for user id = {id}")

    cursor.execute("select id, name, email, age, created_at from users where id = %s", (id,))

    user = cursor.fetchone()
    
    if user is None:
        raise HTTPException(
            status_code=404, 
            detail = error_response("User not found")
        )
    
    redis_client.setex(
        cache_key,
        60,
        json.dumps(build_user_response(user), default = str)
    )
    
    return build_user_response(user)


def get_all_users(page: int = 1, limit: int = 5):

    logger.info(f"[Users] Fetch users page = {page}, limit = {limit}")

    cache_key = f"users:page={page}:limit={limit}"

    cached_users = redis_client.get(cache_key)

    if cached_users:
        logger.info(f"[CACHE] Cache HIT for users page = {page}")

        return json.loads(cached_users)
    
    logger.info(f"[CACHE] Cache MISS for users page = {page}")

    offset = (page - 1) * limit
    cursor.execute("select id, name, email, age, created_at from users order by id limit %s offset %s", (limit, offset))
    
    users = cursor.fetchall()
    cursor.execute("select count(*) as total from users")
    total = cursor.fetchone()["total"]

    response = {
        "page": page,
        "limit": limit,
        "count": len(users),
        "total": total,
        "data": users
    }

    redis_client.setex(
        cache_key,
        60,
        json.dumps(response, default=str)
    )

    return response