from django.shortcuts import redirect, render
from .models import Product

# Create your views here.

def index(request):
    return render(request, 'index.html', {})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product/product_list.html', {'products' : products})

def cart_list(request):
    cart = request.session.get('cart', {})

    # 상품ID 로 상품 정보를 가져오기
    product_ids = cart.keys()
    products = Product.objects.filter(id__in = product_ids)

    # 장바구니 정보를 상품 정보와 함께 매핑
    carts = []
    for product in products:
        quantity = cart.get(str(product.id), 0)
        total_price = product.price * quantity
        carts.append({
            'product' : product,
            'quantity' : quantity,
            'total_price' : total_price,
        })

    return render(request, 'product/cart_list.html', {'carts' : carts})


def cart_add(request, product_id):
    # 세션에서 장바구니 정보 가져오기
    print('장바구니 추가...')
    cart = request.session.get('cart', {})

    # 상품 ID 가 이미 장바구니에 있는지 확인
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart
    return redirect('cart_list')

def cart_remove(request, product_id):
    # 세션에서 장바구니 정보 가져오기
    cart = request.session.get('cart', {})

    # 상품 ID 가 이미 장바구니에 있는지 확인
    if str(product_id) in cart:
        del cart[str(product_id)]

    request.session['cart'] = cart
    return redirect('cart_list')