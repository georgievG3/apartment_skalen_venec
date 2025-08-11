const imageRow = document.getElementById('imageRow');

function scrollLeft() {
    imageRow.scrollLeft -= imageRow.clientWidth / 2; // Scroll left by half the container width
}

function scrollRight() {
    imageRow.scrollLeft += imageRow.clientWidth / 2; // Scroll right by half the container width
}

function openFullscreen(img) {
    const fullscreenModal = document.getElementById('fullscreenModal');
    const fullscreenImage = document.getElementById('fullscreenImage');
    fullscreenModal.style.display = "flex";
    fullscreenImage.src = img.src;
}

function closeFullscreen() {
    const fullscreenModal = document.getElementById('fullscreenModal');
    fullscreenModal.style.display = "none";
}

var button = document.getElementById("reservation-btn");

    window.onscroll = function() {
      if (document.body.scrollTop > 600 || document.documentElement.scrollTop > 600) {
        button.classList.add("fixed-bottom-right");
      } else {
        button.classList.remove("fixed-bottom-right");
      }
    };

document.getElementById("show-more").addEventListener("click", function() {
    var additionalConveniences = document.querySelector(".additional-conveniences");
    
    // Променяме видимостта на допълнителните екстри
    if (additionalConveniences.style.display === "none" || additionalConveniences.style.display === "") {
        additionalConveniences.style.display = "grid";
        this.textContent = "Покажи по-малко екстри"; // Променяме текста на бутона
    } else {
        additionalConveniences.style.display = "none";
        this.textContent = "Покажи още екстри"; // Връщаме текста обратно
    }
});

