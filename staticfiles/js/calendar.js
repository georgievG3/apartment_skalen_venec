document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');
    const startInput = document.getElementById('id_start_date');
    const endInput = document.getElementById('id_end_date');
    const formEl = document.getElementById('reservation-form');

    const summaryEl = document.createElement('div');
    summaryEl.id = 'reservation-summary';
    summaryEl.style.margin = '10px 0';
    formEl.prepend(summaryEl);

    function updateReservationSummary() {
        const start = startInput.value;
        const end = endInput.value;

        if (start && end) {
            const startDate = new Date(start);
            const endDate = new Date(end);
            const nights = Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24)) + 1;
            const pricePerNight = parseFloat('{{ settings.PRICE_PER_NIGHT }}');
            const total = nights * pricePerNight;

            summaryEl.innerHTML = `<p>Нощувки: <strong>${nights}</strong></p>
                                   <p>Обща цена: <strong>${total.toFixed(2)} {{ settings.CURRENCY|upper }}</strong></p>`;
        } else {
            summaryEl.innerHTML = '';
        }
    }

    let firstClickDate = null;
    let selectionEvent = null;
    let busyDates = [];

    fetch('/api/availability/booking/')
        .then(res => res.json())
        .then(events => {
            busyDates = events.map(e => ({
                start: e.start,
                end: e.end
            }));
        })
        .catch(() => console.warn('Неуспешно зареждане на заетите дати.'));

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'bg',
        selectable: false,
        validRange: {
            start: new Date().toISOString().split('T')[0]
        },
        events: '/api/availability/booking/',
        eventDisplay: 'block',
        height: 'auto',

        dateClick: function(info) {
            const clickedDate = info.dateStr;

            const conflictSingle = busyDates.some(e => clickedDate >= e.start && clickedDate < e.end);
            if (conflictSingle) {
                alert('Тази дата е заета!');
                return;
            }

            if (!firstClickDate) {
                firstClickDate = clickedDate;

                if (selectionEvent) selectionEvent.remove();
                selectionEvent = calendar.addEvent({
                    start: firstClickDate,
                    end: firstClickDate,
                    display: 'background',
                    color: '#90caf9',
                    allDay: true
                });

                startInput.value = firstClickDate;
                endInput.value = '';
                formEl.style.display = 'none';
                updateReservationSummary();
            } else {
                let start = firstClickDate < clickedDate ? firstClickDate : clickedDate;
                let end = firstClickDate > clickedDate ? firstClickDate : clickedDate;

                const conflictRange = busyDates.some(e =>
                    start < e.end && new Date(new Date(end).getTime() + 24*60*60*1000).toISOString().split('T')[0] > e.start
                );

                if (conflictRange) {
                    alert('Избраният диапазон съдържа заети дати!');
                    firstClickDate = null;
                    if (selectionEvent) selectionEvent.remove();
                    return;
                }

                if (selectionEvent) selectionEvent.remove();
                selectionEvent = calendar.addEvent({
                    start: start,
                    end: new Date(new Date(end).getTime() + 24*60*60*1000).toISOString().split('T')[0],
                    display: 'background',
                    color: '#90caf9',
                    allDay: true
                });

                startInput.value = start;
                endInput.value = end;
                formEl.style.display = 'block';
                updateReservationSummary();

                firstClickDate = null;
            }
        }
    });

    calendar.render();
});
