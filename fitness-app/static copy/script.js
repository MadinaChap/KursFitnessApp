document.addEventListener("DOMContentLoaded", function() {
    const exerciseBoxes = document.querySelectorAll(".exercise-box");
    const infoPopup = document.getElementById("info-popup");
    const exerciseName = document.getElementById("exercise-name");
    const exerciseDescription = document.getElementById("exercise-description");
    const exerciseImagepath = document.getElementById("exercise-imagepath");
    const closePopup = document.getElementById("close-popup");

    exerciseBoxes.forEach(box => {
        box.addEventListener("click", function() {
            const exerciseData = JSON.parse(this.dataset.exercise);
            exerciseName.textContent = exerciseData.name_ypr;
            exerciseDescription.textContent = exerciseData.description;
            exerciseImagepath.src = exerciseData.image_path;
            infoPopup.style.display = "block";
        });
    });

    closePopup.addEventListener("click", function() {
        infoPopup.style.display = "none";
    });
});