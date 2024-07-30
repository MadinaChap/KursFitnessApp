document.getElementById('exercise-button').addEventListener('click', function() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'http://127.0.0.1:8000/'); 
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log(xhr.responseText); // Вывод ответа сервера в консоль
        }
    };
    xhr.send();
});