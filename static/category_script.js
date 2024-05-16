// Получаем модальное окно
var modal = document.getElementById("myModal");

// Получаем кнопку, которая закрывает модальное окно
var span = document.getElementsByClassName("close")[0];

// Получаем все ссылки категорий
var categoryLinks = document.getElementsByClassName("category-link");

// Перебираем все ссылки категорий и добавляем обработчик события на клик
Array.from(categoryLinks).forEach(function(element) {
    element.addEventListener('click', function() {
        // Получаем URL категории из data-атрибута
        var categoryUrl = this.getAttribute("data-url");
        // Устанавливаем значение скрытого поля в форме
        document.getElementById("category_url").value = categoryUrl;
        // Открываем модальное окно
        modal.style.display = "block";
    });
});

// Закрываем модальное окно при клике на крестик
span.onclick = function() {
    modal.style.display = "none";
}

// Закрываем модальное окно при клике вне его области
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
