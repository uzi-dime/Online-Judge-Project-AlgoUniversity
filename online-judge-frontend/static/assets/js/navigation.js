import { Auth } from './config.js';

document.addEventListener('DOMContentLoaded', () => {
    // Load navbar component
    fetch('/components/navbar.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('navbar-placeholder').innerHTML = data;
            updateAuthNav();
        });
});

function updateAuthNav() {
    const authNav = document.getElementById('authNav');
    if (!authNav) return;

    if (Auth.isAuthenticated()) {
        authNav.innerHTML = `
            <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                    <i class="fas fa-user me-1"></i>Profile
                </a>
                <ul class="dropdown-menu dropdown-menu-end">
                    <li><a class="dropdown-item" href="/pages/profile.html">My Profile</a></li>
                    <li><a class="dropdown-item" href="/pages/my-submissions.html">My Submissions</a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="#" onclick="logout()">Logout</a></li>
                </ul>
            </li>
        `;
    } else {
        authNav.innerHTML = `
            <li class="nav-item">
                <a class="nav-link" href="/pages/login.html">Login</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="/pages/register.html">Register</a>
            </li>
        `;
    }
}

window.logout = function() {
    Auth.removeToken();
    window.location.href = '/pages/login.html';
};
