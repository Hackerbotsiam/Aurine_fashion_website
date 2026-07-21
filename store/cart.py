from decimal import Decimal
from .models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, size_name='', quantity=1):
        item_key = f"{product.id}_{size_name}" if size_name else str(product.id)
        if item_key not in self.cart:
            self.cart[item_key] = {
                'product_id': product.id,
                'quantity': 0,
                'price': str(product.price),
                'size': size_name
            }
        self.cart[item_key]['quantity'] += quantity
        self.save()

    def remove(self, item_key):
        if item_key in self.cart:
            del self.cart[item_key]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = [item['product_id'] for item in self.cart.values()]
        products = Product.objects.filter(id__in=product_ids)
        product_map = {p.id: p for p in products}

        for item_key, item in self.cart.items():
            item_copy = item.copy()
            product = product_map.get(item['product_id'])
            if product:
                item_copy['product'] = product
                item_copy['item_key'] = item_key
                item_copy['price'] = Decimal(item_copy['price'])
                item_copy['total_price'] = item_copy['price'] * item_copy['quantity']
                yield item_copy

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
