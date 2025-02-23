// index.js
console.log("index.js загружен");

document.addEventListener('DOMContentLoaded', function() {
    const filesTab = document.getElementById('filesTab');
    const profileTab = document.getElementById('profileTab');
    const filesSection = document.getElementById('filesSection');
    const profileSection = document.getElementById('profileSection');

    // Переключение между секциями
    filesTab.addEventListener('click', function(event) {
        event.preventDefault();
        filesSection.style.display = 'block';
        profileSection.style.display = 'none';
    });

    profileTab.addEventListener('click', function(event) {
        event.preventDefault();
        filesSection.style.display = 'none';
        profileSection.style.display = 'block';
    });

    // Функция для обработки загрузки файла
    document.getElementById('uploadForm').addEventListener('submit', (event) => {
        const fileInput = document.getElementById('fileInput');
        const file = fileInput.files[0];

        if (!file) {
            alert("Пожалуйста, выберите файл для загрузки.");
            event.preventDefault(); // Отменяем отправку формы, если файл не выбран
            return;
        }

        // Здесь можно добавить дополнительные проверки, если нужно
        // Например, проверка типа файла или размера

        // Если файл выбран, форма будет отправлена автоматически
    });

    // Функция для получения CSRF-токена (если нужно)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
