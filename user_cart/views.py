from django.shortcuts import render, redirect, get_object_or_404
from store_app.models import Product
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.http import require_POST
import stripe
from django.core.mail import send_mail
from django.urls import reverse
from .models import ShippingAddress
from .forms import ShippingAddressForm
from .models import Cart, CartItem, Purchase
from .models import Order, OrderItem
from django.utils import timezone
from django.utils.encoding import force_str
from django.core.mail import EmailMessage
from django.http import HttpResponse


stripe.api_key = settings.STRIPE_SECRET_KEY


def cart_detail(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)

    return render(request, 'user_cart/cart_detail.html',
                  {'cart': cart, 'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY})


def buy_now(request, pk):
    product = get_object_or_404(Product, pk=pk)
    price = product.discounted_price if product.discounted_price else product.price

    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)

            if request.user.is_authenticated:
                shipping_address.user = request.user
            else:
                shipping_address.session_id = session_id

            shipping_address.save()

            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                first_name=shipping_address.first_name,
                last_name=shipping_address.last_name,
                address=f"{shipping_address.address}, {shipping_address.city}, {shipping_address.state}, {shipping_address.postal_code}, {shipping_address.country}",
                total_price=price,
                shipping_address=shipping_address,
                created_at=timezone.now()
            )

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=1,
                price=price,
            )

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': product.name,},
                        'unit_amount': int(price * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('checkout_success', args=[str(order.order_number)])),
                cancel_url=request.build_absolute_uri('/cancel/'),
            )

            return redirect(session.url, code=303)
    else:
        form = ShippingAddressForm()

    return render(request, 'store_app/payment_page.html', {'form': form, 'product': product})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)

    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity

    cart_item.price = product.discounted_price if product.discounted_price else product.price
    cart_item.save()

    return redirect('cart_detail')


def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    cart_item.delete()
    return JsonResponse({'success': True})


@require_POST
def update_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart = Cart.objects.get(session_id=session_id)

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found in cart'}, status=404)

    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()

    # Пересчет общей стоимости корзины
    total_cost = cart.get_total_cost()

    return JsonResponse({'success': True, 'total_cost': total_cost})


@require_POST
def create_checkout_session(request):
    global form

    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart = Cart.objects.get(session_id=session_id)

    if not cart.items.exists():
        return JsonResponse({'error': 'Cart is empty'}, status=400)

    # Фильтруем товары с количеством больше 0
    valid_items = cart.items.filter(quantity__gt=0)

    if not valid_items.exists():
        return JsonResponse({'error': 'No valid items in cart'}, status=400)

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)

            if request.user.is_authenticated:
                shipping_address.user = request.user
            else:
                shipping_address.session_id = request.session.session_key

            shipping_address.save()

            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                first_name=shipping_address.first_name,
                last_name=shipping_address.last_name,
                address=f"{shipping_address.address}, {shipping_address.city}, {shipping_address.state}, {shipping_address.postal_code}, {shipping_address.country}",
                total_price=cart.get_total_cost(),
                shipping_address=shipping_address,
                status='pending',
                created_at=timezone.now()
            )

            # Логика для создания сессии оплаты через Stripe
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': item.product.name,
                            },
                            'unit_amount': int(item.price * 100),
                        },
                        'quantity': item.quantity,
                    } for item in valid_items
                ],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('checkout_success', args=[str(order.order_number)])),
                cancel_url=request.build_absolute_uri('/cancel/'),
            )

            # Сохраняем товары в заказе
            for item in valid_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.price
                )

            # Очистка корзины после успешного создания заказа
            cart.items.all().delete()

            return redirect(session.url, code=303)

    return render(request, 'user_cart/checkout.html', {'form': form, 'cart': cart})


def checkout_success(request, order_id):
    # Получаем заказ по order_number
    order = get_object_or_404(Order, order_number=order_id)

    print(f"Order Shipping Address: {order.shipping_address}")

    # Проверка, что у заказа есть адрес доставки
    if not order.shipping_address:
        return HttpResponse('No shipping address associated with this order.', status=400)

    # Обновляем статус заказа на "Оплачено" и сохраняем дату оплаты
    order.status = 'paid'
    order.payment_date = timezone.now()
    order.save()

    # Подготовка данных для отправки письма
    try:
        order_details = "\n".join([
            f"{item.product.name} (Quantity: {item.quantity})"
            for item in order.items.all()
        ])
    except Exception as e:
        order_details = "Order items could not be retrieved."

    # Отправка email администратору
    try:
        send_mail(
            subject=f"New Order #{order.order_number}",
            message=f"User {order.user.get_full_name()} has placed an order.\n\n"
                    f"Order Number: {order.order_number}\n"
                    f"Date: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"Total Price: ${order.total_price}\n"
                    f"Shipping Address: {order.shipping_address.address}, "
                    f"{order.shipping_address.city}, {order.shipping_address.postal_code}\n\n"
                    f"Order Details:\n" +
                    order_details,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],  # Make sure you have ADMIN_EMAIL in your settings
        )
    except Exception as e:
        # Логируем ошибку отправки письма
        print(f"Error sending email: {e}")

    # Отображение страницы успешной оплаты
    return render(request, 'user_cart/checkout_success.html', {'order': order})


def checkout_cancel(request):
    return render(request, 'user_cart/checkout_cancel.html')
