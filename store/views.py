from django.shortcuts import render
from .models import Product
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages

# func for product_list
def product_list(request):
    query = request.GET.get("q")
    category = request.GET.get("category")

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if category:
        products = products.filter(category=category)

    categories = Product.objects.values_list("category", flat=True).distinct()

    paginator = Paginator(products, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "store/product_list.html", {
        "products": page_obj,
        "page_obj": page_obj,
        "categories": categories,
        "selected_category": category,
        "query": query,
    })

 # func for product_detail
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html', {
        'product': product
        })

# func for add_to_cart
def add_to_cart(request, id):
    cart = request.session.get('cart', {})
    product_id = str(id)

    cart[product_id] = cart.get(product_id, 0) + 1
    request.session['cart'] = cart

    cart_count = sum(cart.values())

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'message': 'Product added to cart!',
            'cart_count': cart_count
        })

    messages.success(request, "Product added to cart!")
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))

# func for cart_page
def cart_page(request):
    cart = request.session.get('cart', {})

    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        item_total = product.price * quantity
        total += item_total

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total,
        })

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

# func for remove_from_cart
def remove_from_cart(request, id):
    cart = request.session.get('cart', {})
    product_id = str(id)

    if product_id in cart:
        cart[product_id] -= 1

        if cart[product_id] <= 0:
            del cart[product_id]

    request.session['cart'] = cart
    messages.success(request, "Cart updated.")

    return redirect('cart_page')

from .models import Product, Order

# func for checkout
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart_page')

    total = 0
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        total += product.price * quantity

    # ✅ ONLY inside POST
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        user = request.user if request.user.is_authenticated else None

        order = Order.objects.create(
             user=user,
            full_name=full_name,
           phone=phone,
         address=address,
         total_amount=total
           )

        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

        request.session['cart'] = {}
        messages.success(request, "Your order has been placed successfully.")

        return redirect('order_success', order_id=order.id)

    # ✅ GET request → just show page
    return render(request, 'store/checkout.html', {'total': total})

# func for checkout_success
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order_success.html', {
        'order': order
        })

# func for registration
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("product_list")
    else:
        form = UserCreationForm()

    return render(request, "store/register.html", {"form": form})

# func order_history
@login_required(login_url='login')
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {
        'orders': orders
        })

# func for order_detail
@login_required(login_url='login')
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)

    return render(request, 'store/order_detail.html', {
        'order': order,
        'order_items': order_items
    })