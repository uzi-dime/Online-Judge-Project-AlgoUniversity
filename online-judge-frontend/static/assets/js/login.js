import APIService from './services/api.js';
import { API_CONFIG, Auth } from "../config.js";

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('loginForm');
    const errorBox = document.getElementById('loginError');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        errorBox.classList.add('d-none');

        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value;

        // Example POST using fetch (update URL as needed)
        try {
            const url = APIService.buildUrl('users', 'login');
            const response = await APIService.request(url, {
                method: 'POST',
                body: JSON.stringify({username, password})
            });
            const data = await response;

            if (response && data.token) {
                // Save token, redirect, etc. (use your auth.js helpers)
                Auth.setToken(data.token);
                // saveUsername(username);
                window.location.href = '/pages/problems.html'; // Redirect to home or dashboard
            } else {
                throw new Error(data.detail || data.error || 'Login failed');
            }
        } catch (err) {
            errorBox.textContent = err.message;
            errorBox.classList.remove('d-none');
        }
    });
});
