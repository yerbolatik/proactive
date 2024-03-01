$(document).ready(function () {
    const notification = $('#jq-notification');

    $(document).on("click", ".add-to-basket", function (e) {
        e.preventDefault();
        const productId = $(this).data("product-id");
        const csrfToken = $("[name=csrfmiddlewaretoken]").val();
        const addToBasketUrl = $(this).attr("href");

        $.ajax({
            type: "POST",
            url: addToBasketUrl,
            data: {
                product_id: productId,
                csrfmiddlewaretoken: csrfToken,
            },
            success: function (data) {
                notification.html(data.message);
                notification.fadeIn(400);
                setTimeout(function () {
                    notification.fadeOut(400);
                }, 7000);

                const goodsInBasketCount = $("#goods-in-basket-count");
                let basketCount = parseInt(goodsInBasketCount.text() || 0);
                basketCount++;
                goodsInBasketCount.text(basketCount);

                $("#basket-items-container").html(data.basket_items_html);
            },
            error: function (data) {
                console.log("Error adding item to basket");
            },
        });
    });

    $(document).on("click", ".remove-from-basket", function (e) {
        e.preventDefault();
        const basketId = $(this).data("basket-id");
        const removeFromBasketUrl = $(this).attr("href");

        $.ajax({
            type: "POST",
            url: removeFromBasketUrl,
            data: {
                basket_id: basketId,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                notification.html(data.message);
                notification.fadeIn(400);
                setTimeout(function () {
                    notification.fadeOut(400);
                }, 7000);

                const goodsInBasketCount = $("#goods-in-basket-count");
                let basketCount = parseInt(goodsInBasketCount.text() || 0);
                basketCount -= data.quantity_deleted;
                goodsInBasketCount.text(basketCount);

                $("#basket-items-container").html(data.basket_items_html);
            },
            error: function (data) {
                console.log("Error removing item from basket");
            },
        });
    });

    $(document).on("change", ".number", function () {
        const basketId = $(this).closest('.col-lg-5').data("basket-id");
        const url = $(this).closest('.col-lg-5').data("basket-change-url");
        const quantity = parseInt($(this).val());

        if (isNaN(quantity) || quantity < 1) {
            $(this).val(1);
            return;
        }

        updateBasket(basketId, quantity, url);
    });

    function updateBasket(basketId, quantity, url) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                basket_id: basketId,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                notification.html(data.message);
                notification.fadeIn(400);
                setTimeout(function () {
                    notification.fadeOut(400);
                }, 7000);

                const goodsInBasketCount = $("#goods-in-basket-count");
                let basketCount = parseInt(goodsInBasketCount.text() || 0);
                basketCount += (data.quantity_updated - quantity);
                goodsInBasketCount.text(basketCount);

                $("#basket-items-container").html(data.basket_items_html);
            },
            error: function (data) {
                console.log("Error updating basket");
            },
        });
    }

    if (notification.length > 0) {
        setTimeout(function () {
            notification.fadeOut(400);
        }, 7000);
    }
});
