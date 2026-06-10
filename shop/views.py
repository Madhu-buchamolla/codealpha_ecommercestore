from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from django.contrib.auth.forms import UserCreationForm
from .models import Product, Order
from django.contrib.auth.decorators import login_required
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})


def add_to_cart(request, id):
    cart = request.session.get('cart', [])

    if id not in cart:
        cart.append(id)

    request.session['cart'] = cart

    return redirect('/')


def cart(request):
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)

    return render(request, 'cart.html', {'products': products})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login/')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

def remove_from_cart(request, id):
    cart = request.session.get('cart', [])

    if id in cart:
        cart.remove(id)

    request.session['cart'] = cart

    return redirect('/cart/')


@login_required
def place_order(request):
    cart = request.session.get('cart', [])

    for product_id in cart:
        product = Product.objects.get(id=product_id)

        Order.objects.create(
            user=request.user,
            product=product
        )

    request.session['cart'] = []

    return render(request, 'order_success.html')