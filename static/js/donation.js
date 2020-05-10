function donate(amount) {
    let url = window.location.href
    let donation_id = url.substring(url.lastIndexOf('/') + 1);
    $('.total-cart').html(amount)
    $('input[id="amount"]').val(amount)
}