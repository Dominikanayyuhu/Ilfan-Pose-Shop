(function() {
    // Получаем текущую дату и время
    const now = new Date();
    
    // Устанавливаем период закрытия (30 декабря 2025 - 7 января 2026)
    const startVacation = new Date('2025-12-28T00:00:00');
    const endVacation = new Date('2026-01-07T00:00:00');

    // Если текущее время попадает в этот промежуток
    if (now >= startVacation && now < endVacation) {
        // Ждем загрузки страницы и заменяем всё содержимое черным экраном
        window.addEventListener('DOMContentLoaded', () => {
            document.body.innerHTML = `
                <div style="
                    position: fixed; 
                    top: 0; 
                    left: 0; 
                    width: 100%; 
                    height: 100%; 
                    background-color: #000; 
                    color: #fff; 
                    display: flex; 
                    justify-content: center; 
                    align-items: center; 
                    text-align: center; 
                    z-index: 999999; 
                    font-family: 'Arial', sans-serif;
                    padding: 20px;
                    box-sizing: border-box;
                ">
                    <h1 style="font-size: 28px; line-height: 1.6;">
                        Извините, но сайт закрыт с 30 декабря по 6 января,<br>
                        приносим свои извинение
                    </h1>
                </div>
            `;
            // Запрещаем прокрутку страницы
            document.body.style.overflow = 'hidden';
        });
    }
})();
