import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)

def get_all_properties():
    from django.core.cache import cache
    from .models import Property

    properties = cache.get("all_properties")

    if properties is None:
        properties = list(Property.objects.all().values(
            "id", "title", "description", "price", "location", "created_at"
        ))
        cache.set("all_properties", properties, 3600)

    return properties


def get_redis_cache_metrics():
    """
    Retrieve Redis keyspace hit/miss metrics and compute hit ratio.
    Logs errors if Redis is unavailable.
    """
    try:
        conn = get_redis_connection("default")
        info = conn.info("stats")

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total_requests = hits + misses

        hit_ratio = (hits / total_requests) if total_requests > 0 else 0

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": round(hit_ratio, 2),
        }

        logger.info("Redis Cache Metrics: %s", metrics)
        return metrics

    except Exception as e:
        logger.error("Failed to fetch Redis metrics: %s", e)
        return {       
            "hits": 0,
            "misses": 0,
            "hit_ratio": 0,
            "error": str(e)
        }