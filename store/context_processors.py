from .models import Product

def categories_processor(request):
    categories = Product.objects.values_list('category', flat=True).distinct()
    return {
        'categories': categories
    }
    
def cart_count(request):
    cart = request.session.get('cart', {})
    total_items = sum(cart.values())
    
    return {
        'cart_count': total_items
    }