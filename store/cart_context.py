# store/cart_context.py

def cart_total_count(request):
    cart = request.session.get('cart', {})
    total_items = sum(cart.values())  
    return {'cart_total_count': total_items}