document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('movie');
    const suggestionsContainer = document.getElementById('suggestions');
    const form = document.querySelector('form');
    let debounceTimeout;

    input.addEventListener('input', () => {
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(() => {
            const query = input.value.trim();
            if (query.length < 2) {
                suggestionsContainer.innerHTML = '';
                return;
            }

            fetch(`/autocomplete?query=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(suggestions => {
                    suggestionsContainer.innerHTML = '';
                    if (suggestions.length === 0) return;

                    suggestions.forEach(suggestion => {
                        const div = document.createElement('div');
                        div.classList.add('suggestion-item');
                        div.textContent = suggestion;
                        div.addEventListener('click', () => {
                            input.value = suggestion;
                            suggestionsContainer.innerHTML = '';
                        });
                        suggestionsContainer.appendChild(div);
                    });
                })
                .catch(error => console.error('Error fetching suggestions:', error));
        }, 300);
    });

    // Hide suggestions when clicking outside
    document.addEventListener('click', (e) => {
        if (!suggestionsContainer.contains(e.target) && e.target !== input) {
            suggestionsContainer.innerHTML = '';
        }
    });

    form.addEventListener('submit', () => {
        document.querySelector('.loading-overlay').style.display = 'flex';
    });

    // Add a beautiful animated background using JS (optional, for extra effect)
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