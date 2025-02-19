document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Предотвращаем стандартное поведение формы

    const formData = new FormData(this);

    fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) {
            // Если ответ не успешный, возвращаем текст ошибки
            return response.text().then(text => { throw new Error(text); });
        }
        // Если авторизация успешна, перенаправляем на новую страницу
        window.location.href = '/index'; // Замените на нужный вам URL
    })
    .catch(error => {
        document.getElementById('error-message').innerText = 'Ошибка: ' + error.message;
    });
});
