document.addEventListener('mousemove', (e) => {
    const header = document.querySelector('header');
    const offsetX = 0; // не нужно смещение, чтобы было точно под курсором
    const offsetY = 0; // не нужно смещение, чтобы было точно под курсором

    header.style.setProperty('--x', e.pageX - 100); // смещаем на половину ширины блика
    header.style.setProperty('--y', e.pageY - 100); // смещаем на половину высоты блика
});