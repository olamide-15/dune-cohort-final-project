const hamburger = document.getElementById('hamburger');
const sidebar   = document.getElementById('sidebar');
const overlay   = document.getElementById('navOverlay');

function openNav() {
    sidebar.classList.add('open');
    overlay.classList.add('active');
    hamburger.classList.add('open');
    document.body.style.overflow = 'hidden'; // prevent scroll behind overlay
}

function closeNav() {
    sidebar.classList.remove('open');
    overlay.classList.remove('active');
    hamburger.classList.remove('open');
    document.body.style.overflow = '';
}

hamburger.addEventListener('click', () => {
    sidebar.classList.contains('open') ? closeNav() : openNav();
});

// Close when clicking the overlay
overlay.addEventListener('click', closeNav);

// Close when a nav link is clicked (good UX on mobile)
sidebar.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', closeNav);
});