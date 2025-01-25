document.addEventListener('mousemove', (e) => {
    const header = document.querySelector('header');

    header.style.setProperty('--x', e.pageX - 100); // смещаем на половину ширины блика
    header.style.setProperty('--y', e.pageY - 100); // смещаем на половину высоты блика
});