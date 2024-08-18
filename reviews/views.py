# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user_cart.models import Purchase


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if not Purchase.objects.filter(user=request.user, product=product).exists():
        messages.error(request, 'To leave a review, make a purchase of this product.')
        return redirect('product_detail', pk=product_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('product_detail', pk=product_id)
    else:
        form = ReviewForm()
    return render(request, 'store_app/add_review.html', {'form': form, 'product': product})