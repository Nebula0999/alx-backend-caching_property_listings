import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    """
    Retrieve Redis keyspace hit/miss metrics and compute hit ratio.
    """
    conn = get_redis_connection("default")  # uses settings.CACHES["default"]
    info = conn.info("stats")

    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    total = hits + misses

    hit_ratio = (hits / total) if total > 0 else 0.0

    metrics = {
        "hits": hits,
        "misses": misses,
        "hit_ratio": round(hit_ratio, 2),
    }

    logger.info("Redis Cache Metrics: %s", metrics)

    return metrics
