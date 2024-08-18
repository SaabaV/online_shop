$(document).ready(function() {
    console.log("Document is ready");



    function handleIndicator(el) {
        items.forEach(item => {
            item.classList.remove('is-active');
            item.removeAttribute('style');
        });

        indicator.style.width = `${el.offsetWidth}px`;
        indicator.style.left = `${el.offsetLeft}px`;
        indicator.style.backgroundColor = el.getAttribute('active-color');

        el.classList.add('is-active');
        el.style.color = el.getAttribute('active-color');
    }

    items.forEach((item, index) => {
        item.addEventListener('click', (e) => { handleIndicator(e.target) });
        item.classList.contains('is-active') && handleIndicator(item);
    });

    $('.quantity-input').change(function() {
        var $input = $(this);
        var quantity = $input.val();
        var productId = $input.closest('tr').data('product-id');
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

        $.ajax({
            url: '/cart/update/' + productId + '/',
            method: 'POST',
            data: {
                'quantity': quantity,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response) {
                $input.closest('tr').find('.item-total').text('$' + response.item_cost);
                $('#cart-total').text(response.total_cost);
                console.log("Quantity updated successfully");
            },
            error: function(response) {
                console.log("Error updating quantity");
            }
        });
    });

    $('#checkout-form').submit(function(event) {
        console.log("Checkout form submitted");
    });

    $('.close').click(function() {
        $('#empty-cart-modal').hide();
    });
});
