document.addEventListener("DOMContentLoaded", function() {
    const slides = document.querySelectorAll(".slide");
    let currentIndex = 0;

    function showSlide(index) {
        slides.forEach((slide, i) => {
            if (i === index) {
                slide.style.transform = "translateX(0)";
                slide.style.opacity = "1";
            } else if (i < index) {
                slide.style.transform = "translateX(-100%)";
                slide.style.opacity = "0";
            } else {
                slide.style.transform = "translateX(100%)";
                slide.style.opacity = "0";
            }
        });
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % slides.length;
        showSlide(currentIndex);
    }

    showSlide(currentIndex);
    setInterval(nextSlide, 5000); // Каждые 5 секунд
});


