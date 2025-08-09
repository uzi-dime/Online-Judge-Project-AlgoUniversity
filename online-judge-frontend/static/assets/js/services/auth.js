const SIGNUP_TOKEN_KEY = 'signupToken';
const USERNAME_KEY = 'username';

function saveSignupToken(token, username) {
  localStorage.setItem(SIGNUP_TOKEN_KEY, token);
  localStorage.setItem(USERNAME_KEY, username);
}

function getSignupToken() {
  return localStorage.getItem(SIGNUP_TOKEN_KEY);
}

function getUsername() {
  return localStorage.getItem(USERNAME_KEY);
}

function removeSignupToken() {
  localStorage.removeItem(SIGNUP_TOKEN_KEY);
  localStorage.removeItem(USERNAME_KEY);
}

export { saveSignupToken, getSignupToken, getUsername, removeSignupToken };

