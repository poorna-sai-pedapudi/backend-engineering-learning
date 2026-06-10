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