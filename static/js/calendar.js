document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');
    const startInput = document.getElementById('id_start_date');
    const endInput = document.getElementById('id_end_date');
    const formEl = document.getElementById('reservation-form');
    let dailyPrices = {};


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

    fetch('/api/prices/')
        .then(res => res.json())
        .then(data => {
            data.forEach(p => {
                dailyPrices[p.date] = p.price;
            });
        calendar.render();
        });

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

        dayCellContent: function(arg) {
            const dateStr = arg.date.toISOString().split('T')[0];
            const price = dailyPrices[dateStr];

            if (!price) {
                return { html: `<div class="fc-day-number">${arg.dayNumberText}</div>` };
            }

            return {
                html: `
                    <div class="fc-day-number">${arg.dayNumberText}</div>
                    <div class="fc-day-price">${price} €</div>
            `
        };
    },


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

                let total = 0;
                let d = new Date(start);

                while (d < new Date(end)) {
                    const key = d.toISOString().split('T')[0];
                    total += dailyPrices[key] || 0;
                     d.setDate(d.getDate() + 1);
                }

                document.getElementById('total_amount').textContent = total.toFixed(2);


                firstClickDate = null;
            }
        }
    });
    calendar.render();
});
