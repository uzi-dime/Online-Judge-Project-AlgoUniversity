// config.js

// Log that configuration is loading
console.log('Loading API configuration...');

// API configuration object
export const API_CONFIG = {
  BASE_URL: 'http://127.0.0.1:8080', // Django backend API URL (change as needed)
  ENDPOINTS: {
    problems: {
      list: '/problems/problems/',
      detail: '/problems/problems/<int:id>/',
      sample_tests: '/problems/problems/sample-tests/<int:id>/',
    },
    submissions: {
      list: '/solutions/solutions/',
      detail: '/solutions/solutions/<int:id>/',
      submit: '/compilers/problems/submit/<int:id>/',
      verdict: '/submissions/verdict/<int:id>/',
      test_verdict: '/solutions/problems/testcases/<int:id>/',
    },
    users: {
      signup: '/users/signup/',
      login: '/users/login/',
      logout: '/users/logout/',
      profile: '/users/profile/',
    }
  }
};

/**
 * Authentication helpers for token management.
 * Tokens are stored in localStorage under "authToken".
 */
export const Auth = {
  /**
   * Retrieves the stored authentication token.
   * @returns {string|null} The token, or null if not set.
   */
  getToken() {
    const token = localStorage.getItem('authToken');
    return token || null;
  },

  /**
   * Sets the authentication token.
   * @param {string} token
   */
  setToken(token) {
    localStorage.setItem('authToken', token);
  },

  /**
   * Removes the authentication token.
   */
  removeToken() {
    localStorage.removeItem('authToken');
  },

  /**
   * Checks if the user is authenticated (token exists).
   * @returns {boolean}
   */
  isAuthenticated() {
    return !!localStorage.getItem('authToken');
  },

  /**
   * Provides the Authorization header for API requests.
   * @returns {Object} Header object or empty object.
   */
  getAuthHeader() {
    const token = this.getToken();
    return token ? { Authorization: `Bearer ${token}` } : {};
  }
};

// Example usage elsewhere:
// import { API_CONFIG, Auth } from "./config.js";
