// Когда html документ готов (прорисован)
$(document).ready(function () {
    // берем в переменную элемент разметки с id jq-notification для оповещений от ajax
    var successMessage = $("#jq-notification");

    // Ловим собыитие клика по кнопке добавить в корзину
    $(document).on("click", ".add-to-basket", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();

        // Берем элемент счетчика в значке корзины и берем оттуда значение
        var goodsInBasketCount = $("#goods-in-basket-count");
        var basketCount = parseInt(goodsInBasketCount.text() || 0);

        // Получаем id товара из атрибута data-product-id
        var product_id = $(this).data("product-id");

        // Из атрибута href берем ссылку на контроллер django
        var add_to_basket_url = $(this).attr("href");

        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({
            type: "POST",
            url: add_to_basket_url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Сообщение
                showNotification(data.message);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    hideNotification();
                }, 700);

                // Увеличиваем количество товаров в корзине (отрисовка в шаблоне)
                basketCount++;
                goodsInBasketCount.text(basketCount);

                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                var basketItemsContainer = document.getElementById("basket-items-container");
                basketItemsContainer.innerHTML = data.basket_items_html;

                $("#delivery-info-container").html(data.delivery_info_html);


            },

            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });




    // Ловим собыитие клика по кнопке удалить товар из корзины
    $(document).on("click", ".remove-from-basket", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();

        // Берем элемент счетчика в значке корзины и берем оттуда значение
        var goodsInBasketCount = $("#goods-in-basket-count");
        var basketCount = parseInt(goodsInBasketCount.text() || 0);

        // Получаем id корзины из атрибута data-basket-id
        var basket_id = $(this).data("basket-id");
        // Из атрибута href берем ссылку на контроллер django
        var remove_from_basket = $(this).attr("href");

        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({

            type: "POST",
            url: remove_from_basket,
            data: {
                basket_id: basket_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Сообщение
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Уменьшаем количество товаров в корзине (отрисовка)
                basketCount -= data.quantity_deleted;
                goodsInBasketCount.text(basketCount);

                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                var basketItemsContainer = document.getElementById("basket-items-container");
                basketItemsContainer.innerHTML = data.basket_items_html;

                $("#delivery-info-container").html(data.delivery_info_html);


            },

            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });




    // Теперь + - количества товара 
    // Обработчик события для уменьшения значения
    $(document).on("click", ".decrement", function () {
        // Берем ссылку на контроллер django из атрибута data-basket-change-url
        var url = $(this).data("basket-change-url");
        // Берем id корзины из атрибута data-basket-id
        var basketID = $(this).data("basket-id");
        // Ищем ближайшеий input с количеством 
        var $input = $(this).closest('.input-group').find('.number');
        // Берем значение количества товара
        var currentValue = parseInt($input.val());
        // Если количества больше одного, то только тогда делаем -1
        if (currentValue > 1) {
            $input.val(currentValue - 1);
            // Запускаем функцию определенную ниже
            // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
            updateBasket(basketID, currentValue - 1, -1, url);
        }
    });

    // Обработчик события для увеличения значения
    $(document).on("click", ".increment", function () {
        // Берем ссылку на контроллер django из атрибута data-basket-change-url
        var url = $(this).data("basket-change-url");
        // Берем id корзины из атрибута data-basket-id
        var basketID = $(this).data("basket-id");
        // Ищем ближайшеий input с количеством 
        var $input = $(this).closest('.input-group').find('.number');
        // Берем значение количества товара
        var currentValue = parseInt($input.val());

        $input.val(currentValue + 1);

        // Запускаем функцию определенную ниже
        // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
        updateBasket(basketID, currentValue + 1, 1, url);
    });

        // Обработчик события для изменения значения в поле типа "number"
    $(document).on("input", ".number", function () {
        var newValue = parseInt($(this).val());
        var oldValue = parseInt($(this).attr("data-old-value"));
        var url = $(this).closest('.input-group').find('.increment').data("basket-change-url");
        var basketID = $(this).closest('.input-group').find('.increment').data("basket-id");

        // Проверяем, было ли изменено значение
        if (newValue !== oldValue) {
            updateBasket(basketID, newValue, newValue - oldValue, url);
            // Обновляем атрибут data-old-value для будущего использования
            $(this).attr("data-old-value", newValue);
        }
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
                // Отображаем сообщение об успешном обновлении корзины
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Обновляем количество товаров в корзине
                var goodsInBasketCount = $("#goods-in-basket-count");
                var basketCount = parseInt(goodsInBasketCount.text() || 0);
                basketCount += change;
                goodsInBasketCount.text(basketCount);

                // Обновляем содержимое корзины
                var basketItemsContainer = document.getElementById("basket-items-container");
                basketItemsContainer.innerHTML = data.basket_items_html;
                
                var totalSumElement = $("#total-sum-for-item-" + basketID); // предположим, что у вас есть элемент с id, содержащий общую сумму за товар
                totalSumElement.text(data.total_sum_for_item); // обновляем текст элемента новым значением общей суммы за товар из ответа сервера
             
                $("#delivery-info-container").html(data.delivery_info_html);

            },
            error: function (data) {
                console.log("Ошибка при обновлении корзины");
            },
        });
    }

    

    // Берем из разметки элемент по id - оповещения от django
    var notification = $('#notification');
    // И через 7 сек. убираем
    if (notification.length > 0) {
        setTimeout(function () {
            notification.alert('close');
        }, 7000);
    }
    

    // При клике по значку корзины открываем всплывающее(модальное) окно
    $('#modalButton').click(function () {
        $('#exampleModal').appendTo('body');

        $('#exampleModal').modal('show');
    });

    // Собыите клик по кнопке закрыть окна корзины
    $('#exampleModal .btn-close').click(function () {
        $('#exampleModal').modal('hide');
    });

    // Обработчик события радиокнопки выбора способа доставки
    $("input[name='requires_delivery']").change(function () {
        var selectedValue = $(this).val();
        // Скрываем или отображаем input ввода адреса доставки
        if (selectedValue === "1") {
            $("#deliveryAddressField").show();
        } else {
            $("#deliveryAddressField").hide();
        }
    });

    // Покажите overlay и уведомление
    function showNotification(message) {
        $("#overlay").show();
        $("#notification-container").show();
        $("#jq-notification").html(message);
    }
    
    // Спрячьте overlay и уведомление
    function hideNotification() {
        $("#overlay").hide();
        $("#notification-container").hide();
    }

});