from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from decimal import Decimal
import stripe
from django.http import JsonResponse
from django.conf import settings
from .utils import round_price_to_99_cents
from .models import Product, Category
from .forms import ProductForm
from user_cart.models import CartItem, Cart
from reviews.forms import ReviewForm
from reviews.models import Review

stripe.api_key = settings.STRIPE_SECRET_KEY


def welcome(request):
    return render(request, 'store_app/welcome.html')


def home(request):
    products = Product.objects.all().order_by('id')
    categories = Category.objects.all()

    # Фильтры категорий
    selected_categories = request.GET.getlist('category')
    if selected_categories:
        products = products.filter(category__id__in=selected_categories)

    # Фильтр цены
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)

    # Применение скидок и округление цены
    for product in products:
        if product.discount_percentage > 0:
            discounted_price = product.price * (1 - product.discount_percentage / Decimal(100))
            product.discounted_price = round_price_to_99_cents(discounted_price)

    for product in products:
        product.average_rating = product.get_average_rating()
        product.review_count = product.reviews.count()
        
    paginator = Paginator(products, 14)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': products,
        'categories': categories,
        'selected_categories': selected_categories,
        'min_price': min_price,
        'max_price': max_price,
        'page_obj': page_obj,
    }
    return render(request, 'store_app/home.html', context)


def sale(request):
    products = Product.objects.filter(discount_percentage__gt=0).order_by('id')
    categories = Category.objects.all()

    # Применение скидок и округление цены
    for product in products:
        discounted_price = product.price * (1 - product.discount_percentage / Decimal(100))
        product.discounted_price = round_price_to_99_cents(discounted_price)

    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': products,
        'categories': categories,
        'page_obj': page_obj,
    }
    return render(request, 'store_app/sale.html', context)


def about(request):
    return render(request, 'store_app/about.html')


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'store_app/product_form.html', {'form': form})


def payment_page(request):
    return render(request, 'store_app/payment_page.html')


def process_payment(request):
    cart = request.session.get('cart', {})
    cart_total = sum(item['price'] * item['quantity'] for item in cart.values())

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item['name'],
                    },
                    'unit_amount': int(item['price'] * 100),  # сумма в центах
                },
                'quantity': item['quantity'],
            } for item in cart.values()
        ],
        mode='payment',
        success_url=request.build_absolute_uri('/success/'),
        cancel_url=request.build_absolute_uri('/cancel/'),
    )

    return JsonResponse({'url': session.url})


def success(request):
    return render(request, 'user_cart/checkout_success.html')


def cancel(request):
    return render(request, 'user_cart/checkout_cancel.html')


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = Review.objects.filter(product=product).order_by('-created_at')
    form = ReviewForm()

    colors = product._meta.get_field('color').choices

    return render(request, 'store_app/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
        'colors': colors,
    })

