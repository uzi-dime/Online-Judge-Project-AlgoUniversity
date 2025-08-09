// register.js
console.log('Register.js loading...');

import APIService from './services/api.js';
import { saveSignupToken } from './services/auth.js';

console.log('Imports completed');

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM Content Loaded');
    const form = document.getElementById('register-form');
    const errorMsg = document.getElementById('error-message');
    const successMsg = document.getElementById('success-message');

    console.log('Form element found:', form !== null);
    
    form.addEventListener('submit', async (e) => {
        console.log('Form submitted');
        e.preventDefault();
        errorMsg.textContent = '';
        successMsg.textContent = '';
        
        console.log('Form event:', e);

        // Get all form values
        const username = document.getElementById('username').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm-password').value;
        const institution = document.getElementById('institution').value.trim();
        const country = document.getElementById('country').value.trim();
        const skillLevel = document.getElementById('skill_level').value;

        // Validate all required fields
        if (!username || !email || !password || !institution || !country || !skillLevel) {
            errorMsg.style.display = 'block';
            errorMsg.textContent = 'All fields are required';
            return;
        }

        // Validate password match
        if (password !== confirmPassword) {
            errorMsg.style.display = 'block';
            errorMsg.textContent = 'Passwords do not match';
            return;
        }

        // Validate email format
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            errorMsg.style.display = 'block';
            errorMsg.textContent = 'Please enter a valid email address';
            return;
        }

        const userData = {
            username,
            email,
            password,
            institution,
            country,
            skill_level: skillLevel
        };
        console.log('Attempting registration with:', { username, email, password: '***' });

        try {
            console.group('Registration Process');
            const response = await APIService.register(userData);
            console.log('Registration response:', response);

            if (response) {
                console.log('Registration successful, preparing redirect...');
                successMsg.textContent = 'Registration successful! Redirecting...';
                
                try {
                    localStorage.setItem('user', JSON.stringify(response.user));
                    console.log('User data stored in localStorage');
                } catch (storageError) {
                    console.warn('Failed to store user data:', storageError);
                }
                
                // const response = await APIService.login(username, password);
                if (response.token) {
                    saveSignupToken(response.token, username);
                } else {
                    console.error('Login failed to provide token');
                }


                setTimeout(() => {
                    console.log('Redirecting to problems page...');
                    window.location.href = '../../../pages/login.html';
                }, 2000); // 2 seconds
            } else {
                console.warn('Registration response indicated failure:', response);
                errorMsg.textContent = response.message || 'Registration failed. Please try again.';
            }
            console.groupEnd();
        } catch (error) {
            console.group('Registration Error');
            console.error('Error object:', error);
            console.error('Error message:', error.message);
            console.error('Error stack:', error.stack);
            console.groupEnd();
            
            errorMsg.textContent = error.message || 'Registration failed. Please try again.';
        }
    });
});
