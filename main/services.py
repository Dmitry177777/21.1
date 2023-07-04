from django.conf import settings
from django.core.cache import cache


def get_category_product(category):
    if settings.CACHE_ENABLED:
        key = 'product_list'
        product_list = cache.get(key)
        if product_list is None:
            product_list = category.product_set.all()
            cache.set(key, product_list)
    else:
        product_list = category.product_set.all()

    return product_list