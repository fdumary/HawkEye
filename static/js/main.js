/* Main JavaScript */

// Smooth scrolling for links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Check if user is logged in on page load
window.addEventListener('load', () => {
    fetch('/api/check-session')
        .then(response => response.json())
        .then(data => {
            if (data.logged_in && !window.location.pathname.includes('/dashboard')) {
                window.location.href = '/dashboard';
            }
        });
});
