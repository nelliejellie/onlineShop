import redis
from django.conf import settings
from .models import Product

# connect to redis
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)

class Recommender(object):
    def get_product_key(self, id):
        return f'product:{id}:purchased_with'

    def products_bought(self, products):
        products_ids = [p.id for p in products]
        for product_id in products_ids:
            # get the other products bought with each product
            if products_id != with_id:
                # increment score for the product purchased together
                r.zincrby(self.get_product_key(product_id),1, with_id)

    def suggest_products_for(self, products, max_results=6):
        product_ids = [p.id for p in products]
        if len(products) == 1:
            # only 1 product
            suggestions = r.zrange(self.get_product_key(product_ids[0]),
                            0, -1, desc=True)[:max_results]
                            
        else:
            # generate a temporary key
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = f'tmp_{flat_ids}'
            # multiple products, combine scores of all products
            # store the resulting sorted set in a temporary key
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)
            # remove ids for the products the recommendations is for
            r.zrem(tmp_key, *product_ids)
            # get the product ids by their score, descendat sort
            suggestions = r.zrange(tmp_key, 0, 1,
                            desc=True
                            )[:max_results]
            # remove the temprary key
            r.delete(tmp_key)
            suggested_products_ids = [int(id) for id in suggestions]
            #get suggested products and sort by order of appearance
            suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
            suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
            return suggested_products
        
    def clear_purchase(self):
        for id in Product.values_list('id', flat=True):
            r.delete(self.get_product_key(id))


