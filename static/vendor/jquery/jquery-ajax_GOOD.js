$(document).ready(function () {
    var successMessage = $("#jq-notification");

    function updateBasketAndPage(data) {
        // Обновляем сообщение и содержимое корзины
        successMessage.html(data.message);
        successMessage.fadeIn(400);
        setTimeout(function () {
            successMessage.fadeOut(400);
        }, 7000);

        var goodsInBasketCount = $("#goods-in-basket-count");
        goodsInBasketCount.text(data.basket_count);

        var basketItemsContainer = $("#basket-items-container");
        basketItemsContainer.html(data.basket_items_html);

        var deliveryInfoContainer = $("#delivery-info-container");
        deliveryInfoContainer.html(data.delivery_info_html);
    }

    $(document).on("click", ".add-to-basket", function (e) {
        e.preventDefault();
        var add_to_basket_url = $(this).attr("href");
        $.ajax({
            type: "POST",
            url: add_to_basket_url,
            data: {
                product_id: $(this).data("product-id"),
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: updateBasketAndPage,
            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });

    $(document).on("click", ".remove-from-basket", function (e) {
        e.preventDefault();
        var remove_from_basket_url = $(this).attr("href");
        $.ajax({
            type: "POST",
            url: remove_from_basket_url,
            data: {
                basket_id: $(this).data("basket-id"),
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: updateBasketAndPage,
            error: function (data) {
                console.log("Ошибка при удалении товара из корзины");
            },
        });
    });

    $(document).on("click", ".decrement", function () {
        var url = $(this).data("basket-change-url");
        var basketID = $(this).data("basket-id");
        var $input = $(this).closest('.input-group').find('.number');
        var currentValue = parseInt($input.val());
        if (currentValue > 1) {
            $input.val(currentValue - 1);
            updateBasket(basketID, currentValue - 1, -1, url);
        }
    });

    $(document).on("click", ".increment", function () {
        var url = $(this).data("basket-change-url");
        var basketID = $(this).data("basket-id");
        var $input = $(this).closest('.input-group').find('.number');
        var currentValue = parseInt($input.val());
        $input.val(currentValue + 1);
        updateBasket(basketID, currentValue + 1, 1, url);
    });

    function updateBasket(basketID, quantity, change, url) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                basket_id: basketID,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Передаем showMessage=false, чтобы не отображать сообщение
                updateBasketAndPage(data, false);
            },
            error: function (data) {
                console.log("Ошибка при обновлении корзины");
            },
        });
    }

    var notification = $('#notification');
    if (notification.length > 0) {
        setTimeout(function () {
            notification.alert('close');
        }, 7000);
    }

    $('#modalButton').click(function () {
        $('#exampleModal').appendTo('body');
        $('#exampleModal').modal('show');
    });

    $('#exampleModal .btn-close').click(function () {
        $('#exampleModal').modal('hide');
    });

    $("input[name='requires_delivery']").change(function () {
        var selectedValue = $(this).val();
        if (selectedValue === "1") {
            $("#deliveryAddressField").show();
        } else {
            $("#deliveryAddressField").hide();
        }
    });
});
