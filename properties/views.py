from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Property
from django.http import JsonResponse
from .utils import get_all_properties

def property_list(request):
    properties = get_all_properties()
    return JsonResponse({"data": properties})


@cache_page(60 * 15)  # cache for 15 minutes
def property_list(request):
    properties = Property.objects.all().values("id", "title", "description", "price", "location", "created_at")
    return JsonResponse({"data": list(properties)})

def cache_metrics(request):
    metrics = get_redis_cache_metrics()
    return JsonResponse(metrics)