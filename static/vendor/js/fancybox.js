$(document).ready(function () {
    $(".fancybox").fancybox();
});


document.addEventListener("DOMContentLoaded", function() {
    var footer = document.querySelector("footer");
    window.addEventListener("scroll", function() {
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
            // Если пользователь прокрутил страницу до конца, показываем футер
            footer.style.display = "block";
        } else {
            // В противном случае скрываем футер
            footer.style.display = "none";
        }
    });
});
