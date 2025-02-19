// script.js

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('settingsForm');
    const saveButton = document.getElementById('saveButton');
    const themeToggleButton = document.getElementById('themeToggleButton');

    // Обработчик события для кнопки "Сохранить настройки"
    saveButton.addEventListener('click', function(event) {
        event.preventDefault(); // Предотвращаем стандартное поведение кнопки

        // Здесь можно добавить валидацию, если это необходимо
        const startSetting = document.getElementById('id_start_setting').checked;
        const anotherSetting = document.getElementById('id_another_setting').checked;

        if (!startSetting && !anotherSetting) {
            alert('Пожалуйста, выберите хотя бы одну настройку.');
            return;
        }

        // Если все в порядке, отправляем форму
        form.submit();
    });

    // Обработчик события для переключения темы
    themeToggleButton.addEventListener('click', function() {
        document.body.classList.toggle('dark-theme');
        const container = document.querySelector('.container');
        container.classList.toggle('dark-theme');
        themeToggleButton.classList.toggle('dark-theme');
    });
});
