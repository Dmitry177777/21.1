from django.conf import settings
from django.core.cache import cache


def get_product_category(product):
    if settings.CACHE_ENABLED:
        key = 'product_category'
        product_category = cache.get(key)
        if product_category is None:
            product_category = object.category_set.all()
            cache.set(key, product_category)
    else:
        product_category = object.category_set.all()

    return product_category