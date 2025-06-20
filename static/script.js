document.addEventListener('DOMContentLoaded', () => {
    const horseForm = document.getElementById('horseForm');
    const horseList = document.getElementById('horseList');

    function fetchHorses() {
        fetch('/api/horses')
            .then(res => res.json())
            .then(data => {
                horseList.innerHTML = '';
                data.forEach(horse => {
                    const li = document.createElement('li');
                    li.className = 'list-group-item d-flex justify-content-between align-items-center';
                    li.innerHTML = `<div><strong>${horse.name}</strong>: ${horse.description}</div>` +
                        `<button class="btn btn-danger btn-sm" data-name="${horse.name}">Remove</button>`;
                    horseList.appendChild(li);
                });
            });
    }

    horseForm.addEventListener('submit', e => {
        e.preventDefault();
        const name = document.getElementById('name').value.trim();
        const description = document.getElementById('description').value.trim();
        if (!name || !description) return;
        fetch('/api/horses', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, description })
        })
        .then(res => res.json())
        .then(() => {
            horseForm.reset();
            fetchHorses();
        });
    });

    horseList.addEventListener('click', e => {
        if (e.target.tagName === 'BUTTON') {
            const name = e.target.getAttribute('data-name');
            fetch(`/api/horses/${encodeURIComponent(name)}`, {
                method: 'DELETE'
            })
            .then(() => fetchHorses());
        }
    });

    fetchHorses();
}); 