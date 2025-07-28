// API Configuration
console.log('Loading API configuration...');

const API_CONFIG = {
    BASE_URL: 'http://127.0.0.1:8080',  // Django backend API URL
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
            profile: '/users/profile/'
        }
    }
};

// Authentication helper functions
const Auth = {
  getToken: () => {
    const token = localStorage.getItem('authToken');
    console.log('getToken:', token);
    return token;
  },
  setToken: (token) => {
    console.log('setToken:', token);
    localStorage.setItem('authToken', token);
  },
  removeToken: () => {
    console.log('removeToken called');
    localStorage.removeItem('authToken');
  },
  isAuthenticated: () => {
    const exists = !!localStorage.getItem('authToken');
    console.log('isAuthenticated:', exists);
    return exists;
  }
};


export { API_CONFIG, Auth };
