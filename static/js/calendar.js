document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');
    const startInput = document.getElementById('id_start_date');
    const endInput = document.getElementById('id_end_date');
    const formEl = document.getElementById('reservation-form');

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'bg',
        selectable: true,
        select: function(info) {
            fetch('/api/availability/booking/')
                .then(res => res.json())
                .then(events => {
                    const conflict = events.some(e =>
                        info.startStr < e.end && info.endStr > e.start
                    );
                    if (conflict) {
                        alert('Избраните дати вече са заети!');
                        return;
                    }

                    // Попълваме формата само за текущата сесия
                    startInput.value = info.startStr;
                    endInput.value = info.endStr;
                    formEl.style.display = 'block';
                })
                .catch(() => alert('Грешка при проверка на наличностите. Опитайте по-късно.'));
        },
        events: '/api/availability/booking/',
        eventDisplay: 'block',
        height: 'auto'
    });

    calendar.render();
});
