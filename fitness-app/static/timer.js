var startTime = new Date().getTime();
var exerciseTime = 5 * 1000;
var currentExerciseIndex = 0; // Индекс текущего упражнения

function updateTimer() {
    var currentTime = new Date().getTime();
    var timeElapsed = currentTime - startTime;
    var minutes = Math.floor(timeElapsed / 60000);
    var seconds = Math.floor((timeElapsed % 60000) / 1000);

    var display = minutes.toString().padStart(2, '0') + ':' + seconds.toString().padStart(2, '0');
    document.getElementById('timer').innerHTML = display;

    if (timeElapsed >= exerciseTime) {
        clearInterval(timerInterval); // Останавливаем интервал, так как достигнуто нужное время
        document.getElementById('timer').innerHTML = "Время вышло";
    }
}

var timerInterval = setInterval(updateTimer, 1000);