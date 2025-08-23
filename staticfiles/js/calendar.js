document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');

    var preselectedStart = document.getElementById('id_start_date').value;
    var preselectedEnd = document.getElementById('id_end_date').value;

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'bg',
        selectable: true,
        select: function(info) {
            fetch('/api/availability/booking/')
                .then(res => res.json())
                .then(events => {
                    let conflict = events.some(e =>
                        info.startStr < e.end && info.endStr > e.start
                    );
                    if (conflict) {
                        alert('Избраните дати вече са заети!');
                        return;
                    }

                    document.getElementById('id_start_date').value = info.startStr;
                    document.getElementById('id_end_date').value = info.endStr;
                    document.getElementById('reservation-form').style.display = 'block';
                })
                .catch(() => {
                    alert('Грешка при проверка на наличностите. Опитайте по-късно.');
                });
        },
        events: '/api/availability/booking/',
        eventDisplay: 'block',
        height: 'auto'
    });

    calendar.render();

    if(preselectedStart && preselectedEnd){
        calendar.select(preselectedStart, preselectedEnd);
        document.getElementById('reservation-form').style.display = 'block';
    }
});