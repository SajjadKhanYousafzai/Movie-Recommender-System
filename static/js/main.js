document.addEventListener('DOMContentLoaded', function() {
    const movieInput = document.getElementById('movie');
    const datalist = document.getElementById('movie-list');

    // Autocomplete using /autocomplete endpoint
    movieInput.addEventListener('input', function() {
        const query = this.value;
        if (query.length < 2) return;
        fetch(`/autocomplete?query=${encodeURIComponent(query)}`)
            .then(res => res.json())
            .then(suggestions => {
                datalist.innerHTML = '';
                suggestions.forEach(title => {
                    const option = document.createElement('option');
                    option.value = title;
                    datalist.appendChild(option);
                });
            });
    });

    // Animated floating film reels (optional, for extra beauty)
    const createFloatingImage = (src, left, top, size, duration) => {
        const img = document.createElement('img');
        img.src = src;
        img.style.position = 'fixed';
        img.style.left = left;
        img.style.top = top;
        img.style.width = size;
        img.style.height = size;
        img.style.opacity = '0.10';
        img.style.pointerEvents = 'none';
        img.style.zIndex = '0';
        img.style.transition = `transform ${duration}s linear`;
        document.body.appendChild(img);
        setInterval(() => {
            img.style.transform = `rotate(${Math.random()*360}deg) scale(${0.8 + Math.random()*0.4})`;
        }, duration * 1000);
    };
    createFloatingImage('https://cdn-icons-png.flaticon.com/512/833/833314.png', '3vw', '7vh', '120px', 12);
    createFloatingImage('https://cdn-icons-png.flaticon.com/512/616/616554.png', '85vw', '80vh', '120px', 16);
});
