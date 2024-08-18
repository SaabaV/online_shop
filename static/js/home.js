$(document).ready(function() {
    console.log("Document is ready");

    const indicator = document.querySelector('.nav-indicator');
    const items = document.querySelectorAll('.nav-item');

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

    $('.product-image').click(function() {
        $(this).toggleClass('expanded');
    });

    $('#category-toggle').click(function() {
        $('#category-menu').toggle();
    });

    $('#price-range').slider({
        range: true,
        min: 0,
        max: 250,
        values: [0, 250],
        slide: function(event, ui) {
            $('#min_price').val(ui.values[0]);
            $('#max_price').val(ui.values[1]);
            $('#price-label').text('€' + ui.values[0] + ' - €' + ui.values[1]);
        }
    });

    $('#min_price').val($('#price-range').slider('values', 0));
    $('#max_price').val($('#price-range').slider('values', 1));
    $('#price-label').text('€' + $('#price-range').slider('values', 0) + ' - €' + $('#price-range').slider('values', 1));

    // Category choice handling
    $('.category-yes').click(function() {
        $(this).closest('.category-option').find('.category-yes').css('color', 'green');
        $(this).closest('.category-option').find('.category-no').css('color', 'grey');
        $(this).closest('.category-option').find('input[type="hidden"]').val('yes');
    });

    $('.category-no').click(function() {
        $(this).closest('.category-option').find('.category-no').css('color', 'red');
        $(this).closest('.category-option').find('.category-yes').css('color', 'grey');
        $(this).closest('.category-option').find('input[type="hidden"]').val('no');
    });

    $('.btn-primary').click(function() {
        let categories = [];
        let minPrice = $('#min_price').val();
        let maxPrice = $('#max_price').val();

        $('.category-option input[type="hidden"]').each(function() {
            if ($(this).val() === 'yes') {
                categories.push($(this).closest('.category-option').data('category-id'));
            }
        });

        let query = '?';
        if (categories.length > 0) {
            categories.forEach(cat => {
                query += 'category=' + cat + '&';
            });
        }
        if (minPrice) {
            query += 'min_price=' + minPrice + '&';
        }
        if (maxPrice) {
            query += 'max_price=' + maxPrice + '&';
        }

        window.location.href = query.slice(0, -1); // Remove the trailing '&'
    });
});






