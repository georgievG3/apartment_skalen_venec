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
    
    if (additionalConveniences.style.display === "none" || additionalConveniences.style.display === "") {
        additionalConveniences.style.display = "grid";
        this.textContent = "Покажи по-малко екстри";
    } else {
        additionalConveniences.style.display = "none";
        this.textContent = "Покажи още екстри";
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const profileBtn = document.getElementById("profile-btn");
    const modal = document.getElementById("profile-modal");

    profileBtn.addEventListener("click", function (event) {
        event.stopPropagation();
        modal.style.display = modal.style.display === "flex" ? "none" : "flex";
    });

    document.addEventListener("click", function (event) {
        if (modal.style.display === "flex" && !modal.contains(event.target) && event.target !== profileBtn) {
            modal.style.display = "none";
        }
    });
});

