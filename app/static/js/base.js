document.addEventListener('mousemove', (e) => {
    const header = document.querySelector('header');

    header.style.setProperty('--x', e.pageX - 100); // смещаем на половину ширины блика
    header.style.setProperty('--y', e.pageY - 100); // смещаем на половину высоты блика
});

document.addEventListener("DOMContentLoaded", function () {
    let alerts = document.querySelectorAll(".flash-message");
    alerts.forEach(function (alert) {
        setTimeout(function () {
            let bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000); // Закрывается через 5 секунд
    });
});
