import urllib.parse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.conf import settings
from django.db.models import Q
from .models import Category, Product
from .cart import Cart

# 1. product search, list and filter
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)
    query = request.GET.get('q', '').strip()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    return render(request, 'store/index.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'query': query,
    })

# 2. product details page
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    return render(request, 'store/product_detail.html', {'product': product})

# 3. added cart
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        size_name = request.POST.get('size', '')
        quantity = int(request.POST.get('quantity', 1))
        cart.add(product=product, size_name=size_name, quantity=quantity)
    return redirect(request.META.get('HTTP_REFERER', 'store:product_list'))

# 4. remove frome cart
def cart_remove(request, item_key):
    cart = Cart(request)
    cart.remove(item_key)
    return redirect(request.META.get('HTTP_REFERER', 'store:product_list'))

# 5. messenger bKash cheakout link generator
def messenger_checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('store:product_list')

    lines = ["✨ *NEW ORDER - VELORA STORE* ✨", "----------------------------"]
    for item in cart:
        size_str = f" (Size: {item['size']})" if item['size'] else ""
        lines.append(f"• {item['product'].name}{size_str} x {item['quantity']} = ৳{item['total_price']:.2f}")
    
    lines.append("----------------------------")
    lines.append(f"💰 *Total Amount:* ৳{cart.get_total_price():.2f}")
    lines.append("\nHi! I would like to place this order and pay via bKash. Please send me your bKash details!")

    full_message = "\n".join(lines)
    encoded_message = urllib.parse.quote(full_message)
    
    fb_page = getattr(settings, 'FACEBOOK_PAGE_USERNAME', 'velora.official')
    messenger_url = f"https://m.me/{fb_page}?text={encoded_message}"
    
    return HttpResponseRedirect(messenger_url)
