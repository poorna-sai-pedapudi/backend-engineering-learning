import json
import logging
from database import cursor
from redis_client import redis_client

logger = logging.getLogger(__name__)

def get_dashboard_metrics():

    logger.info("[DASHBOARD] Fetch dashboard metrics")

    cache_key = "dashboard:metrics"

    cached_dashboard = redis_client.get(cache_key)

    if cached_dashboard:
        logger.info("[CACHE] Dashboard HIT")
        return json.loads(cached_dashboard)
    
    logger.info("[CACHE] Dashboard MISS")

    cursor.execute(
        """
        select 
	        (select count(*) from users) as total_users,
	        (select count(*) from orders) as total_orders,
            (select coalesce(sum(price), 0) from orders) as total_revenue,
            (select coalesce(avg(price), 0) from orders) as average_order_prices;
        """
    )

    metrics = cursor.fetchone()

    redis_client.setex(
        cache_key,
        60,
        json.dumps(metrics, default = str)
    )

    return metrics