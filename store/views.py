from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem

# 1. Homepage View
def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

# 2. Product Detail View
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

# 3. View Cart (Yeh missing tha!)
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            subtotal = product.price * quantity
            total_price += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
        except Product.DoesNotExist:
            continue

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'store/cart.html', context)

# 4. Add to Cart Logic (Yeh bhi missing tha!)
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('view_cart')

# 5. Remove from Cart Logic (Yeh bhi missing tha!)
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('view_cart')

# 6. Dynamic Plus/Minus Quantity Update Logic (Yeh bhi missing tha!)
def update_cart(request, product_id, action):
    cart = request.session.get('cart', {})
    p_id = str(product_id)
    
    if p_id in cart:
        if action == 'plus':
            cart[p_id] += 1
        elif action == 'minus':
            cart[p_id] -= 1
            if cart[p_id] <= 0:
                del cart[p_id]
        request.session['cart'] = cart
        request.session.modified = True
        
    return redirect('view_cart')

# 7. Checkout View (Multiple items handle karne ke liye)
def checkout(request):
    cart = request.session.get('cart', {})
    cart_items = []
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            cart_items.append({
                'product': product,
                'quantity': quantity,
            })
        except Product.DoesNotExist:
            continue
    
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        phone_number = request.POST.get('phone_number')
        shipping_address = request.POST.get('shipping_address')

        if cart_items:
            # Main Order create karein
            order = Order.objects.create(
                customer_name=customer_name,
                phone_number=phone_number,
                shipping_address=shipping_address
            )

            # Har item ko OrderItem table mein save karein
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['product'].price
                )

            # Order hone ke baad cart khali karein
            request.session['cart'] = {}
            request.session.modified = True
            
            return redirect('order_success') 
            
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'store/checkout.html', context)

# 8. Order Success View
def order_success(request):
    return render(request, 'store/order_success.html')
# store/views.py ke aakhir mein yeh add karein:

def cart_total_count(request):
    """
    Context processor: Jo pure website ke templates (jaise navbar) mein 
    total cart items count dikhane ke liye use hota hai.
    """
    cart = request.session.get('cart', {})
    total_count = 0
    
    # Har item ki quantity ko plus karein
    for product_id, quantity in cart.items():
        total_count += quantity
        
    return {'cart_total_count': total_count}