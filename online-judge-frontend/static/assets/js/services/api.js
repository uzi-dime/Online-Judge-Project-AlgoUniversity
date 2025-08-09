import { API_CONFIG, Auth } from "../config.js";
// Importing Auth functions directly from config.js
import { getSignupToken, saveSignupToken } from './auth.js';

class APIService {
    // Helper to build full URL with optional params (e.g., IDs, query strings)
    static buildUrl(endpointKey, method, id = null, queryParams = {}) {
        const base = API_CONFIG.BASE_URL.endsWith('/') ? API_CONFIG.BASE_URL.slice(0, -1) : API_CONFIG.BASE_URL;
        let path = API_CONFIG.ENDPOINTS[endpointKey][method];
        if (id) {
            path = path.replace('<int:id>', id);
        }
        let url = base + path;

        const query = new URLSearchParams(queryParams).toString();
        if (query) {
            url += `?${query}`;
        }

        return url;
    }

    static async getSampleTests(problemId) {
        try {
            const url = this.buildUrl('problems', 'sample_tests', problemId);
            console.log(`Fetching sample tests from: ${url}`);  // Debug log
            const response = await this.request(url, { method: 'GET' });
            console.log('Sample tests response:', response);
            if (!response) {
                throw new Error('Failed to fetch sample tests');
            }

            return await response;
        } catch (error) {
            console.error('Error fetching sample tests:', error);
            throw error;
        }
    }

    static async request(url, options = {}) {
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    let token; // declare here once

    if (url.includes('login')) {
        console.log('Login URL detected');
        token = getSignupToken();
        // Add any additional logic you need here
    } else {
        token = Auth.getToken();
    }

    console.log(`Making request to: ${token}`);

    if (token) {
        headers['Authorization'] = `Bearer ${token}`; // Or 'Token' if your backend uses DRF's TokenAuthentication
    }

    const fetchOptions = {
        ...options,
        headers,
    };

    const response = await fetch(url, fetchOptions);

    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
    }

    return await response.json();
}




    // Problems
    static async getProblems() {
        const url = this.buildUrl('problems', 'list');
        console.log(`Fetching problems from: ${url}`);  // Debug log
        return await this.request(url, { method: 'GET' });
    }

    static async getProblem(id) {
        const url = this.buildUrl('problems', 'detail', id);
        return await this.request(url, { method: 'GET' });
    }

    // Submissions
    static async submitSolution(problemId, code, language) {
        const url = APIService.buildUrl('submissions', 'submit', problemId);
        try {
            return await this.request(url, {
                method: 'POST',
                body: JSON.stringify({
                    code,
                    language
                })
            });
        } catch (error) {
            console.error(`Error submitting solution: ${error}`);
            throw error;
        }
    }

    static async getSubmissions(problemId = null, pageId = 1) {
        const query = problemId ? { problem: problemId } : {};
        const url = this.buildUrl('submissions', 'list');
        const queryWithPageId = { ...query, page: pageId };
        
        // Construct query string properly
        const queryString = new URLSearchParams(queryWithPageId).toString();
        console.log(`Fetching submissions from: ${url}${queryString ? '?' + queryString : ''}`);  // Debug log
        return await this.request(`${url}${queryString ? '?' + queryString : ''}`, { method: 'GET' });
    }


    static async getSubmissionDetails(submissionId) {
        const url = this.buildUrl('submissions', 'detail', submissionId);
        return await this.request(url, { method: 'GET' });
    }

    static async getVerdictStatus(submissionId) {
        const url = this.buildUrl('submissions', 'verdict', submissionId);
        return await this.request(url, { method: 'GET' });
    }

    
    static async getTestCaseVerdict(problemId) {
        const url = this.buildUrl('submissions', 'test_verdict', problemId);
        return await this.request(url, { method: 'GET' });
    }

    // Authentication
    static async login(username, password) {
        const url = API_CONFIG.BASE_URL + API_CONFIG.ENDPOINTS.auth.login;
        const response = await this.request(url, {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
        if (response.token) {
            Auth.setToken(response.token);
        }
        return response;
    }

    static async register(userData) {
        if (!userData.username || !userData.email || !userData.password) {
            return { status: 'error', error: 'Missing required fields for registration' };
        }

        const url = API_CONFIG.BASE_URL + API_CONFIG.ENDPOINTS.users.signup;

        try {
            const response = await this.request(url, {
                method: 'POST',
                body: JSON.stringify(userData)
            });

            // Store token if present
            if (response.token) {
                saveSignupToken(response.token);
            }
            return { ...response, status: 'success' };
        } catch (error) {
            // If backend gave JSON error details, fetch them:
            let errMsg = error.message || 'Registration failed';
            if (error.response && typeof error.response.json === 'function') {
                try {
                    const data = await error.response.json();
                    errMsg = data.error || errMsg;
                } catch {}
            }
            return { status: 'error', error: errMsg };
        }
    }


    static async getUserProfile() {
        const url = API_CONFIG.BASE_URL + API_CONFIG.ENDPOINTS.auth.profile;
        return await this.request(url, { method: 'GET' });
    }
}

export default APIService;
