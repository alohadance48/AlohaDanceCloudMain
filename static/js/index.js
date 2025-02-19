// Функция для загрузки файлов из localStorage
function loadFiles() {
    const files = JSON.parse(localStorage.getItem('files')) || [];
    const fileList = document.querySelector('.file-list');
    fileList.innerHTML = ''; // Очистить текущий список файлов

    files.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        fileItem.textContent = file.name;

        // Добавление иконки файла
        const fileIcon = document.createElement('i');
        fileIcon.className = 'fas fa-file'; // Используем иконку файла
        fileItem.appendChild(fileIcon);

        // Кнопка удаления файла
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Удалить';
        deleteButton.className = 'delete-button';
        deleteButton.addEventListener('click', () => deleteFile(index)); // Удаляем файл по индексу
        fileItem.appendChild(deleteButton);

        fileList.appendChild(fileItem);
    });
}

// Функция для обработки загрузки файла
document.getElementById('uploadForm').addEventListener('submit', (event) => {
    event.preventDefault(); // Предотвращаем стандартное поведение формы

    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (!file) {
        alert("Пожалуйста, выберите файл для загрузки.");
        return;
    }

    const files = JSON.parse(localStorage.getItem('files')) || [];
    files.push({ name: file.name }); // Сох
    // Сохраняем только имя файла
    files.push({ name: file.name }); // Сохраняем имя файла в массив
    localStorage.setItem('files', JSON.stringify(files)); // Сохраняем массив файлов в localStorage

    loadFiles(); // Обновляем список файлов после загрузки
    fileInput.value = ''; // Очищаем поле ввода файла
});

// Функция для удаления файла
const deleteFile = (index) => {
    const files = JSON.parse(localStorage.getItem('files')) || [];
    files.splice(index, 1); // Удаляем файл по индексу
    localStorage.setItem('files', JSON.stringify(files)); // Обновляем localStorage
    loadFiles(); // Обновляем список файлов после удаления
};

// Инициализация: загрузка файлов при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    loadFiles(); // Загружаем файлы при загрузке страницы

    // Переключение между разделами "Файлы" и "Профиль"
    const filesTab = document.getElementById('filesTab');
    const profileTab = document.getElementById('profileTab');
    const filesSection = document.getElementById('filesSection');
    const profileSection = document.getElementById('profileSection');

    filesTab.addEventListener('click', (event) => {
        event.preventDefault();
        filesSection.style.display = 'block';
        profileSection.style.display = 'none';
    });

    profileTab.addEventListener('click', (event) => {
        event.preventDefault();
        filesSection.style.display = 'none';
        profileSection.style.display = 'block';
    });

    // Инициализация: показываем раздел "Файлы" по умолчанию
    filesSection.style.display = 'block';
    profileSection.style.display = 'none';
});
