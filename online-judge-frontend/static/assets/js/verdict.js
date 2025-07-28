import APIService from './services/api.js';

// Utility to safely escape HTML in text, preventing XSS and layout breakage
function escapeHtml(text) {
    if (!text) return '';
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

document.addEventListener('DOMContentLoaded', async () => {
    // Load navbar asynchronously
    const navbarPlaceholder = document.getElementById('navbar-placeholder');
    fetch('../components/navbar.html')
        .then(response => response.text())
        .then(data => {
            navbarPlaceholder.innerHTML = data;
        });

    // Get submission ID from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const submissionId = urlParams.get('id');

    if (!submissionId) {
        showError('No submission ID provided');
        return;
    }

    try {
        // Fetch submission details
        const submission = await APIService.getSubmissionDetails(submissionId);
        displayVerdict(submission);
    } catch (error) {
        showError('Failed to load submission details');
        console.error(error);
    }
});

function displayVerdict(submission) {
    // Update submission details on the page
    console.log('Submission details:', submission);

    document.getElementById('problemLink').textContent = submission.problem.title;
    document.getElementById('problemLink').href = `/pages/problem-detail.html?id=${submission.problem.id}`;
    document.getElementById('submissionTime').textContent = new Date(submission.updated_at).toLocaleString();
    document.getElementById('language').textContent = submission.language;

    const verdictStatus = document.getElementById('verdictStatus');
    verdictStatus.textContent = submission.status;
    verdictStatus.className = `badge ${getVerdictClass(submission.status)}`;

    document.getElementById('executionTime').textContent = `${submission.execution_time} ms`;
    document.getElementById('memoryUsage').textContent = `${submission.memory_used} KB`;

    // Display submitted code with syntax highlighting
    const codeElement = document.getElementById('submittedCode');
    codeElement.textContent = submission.code;
    Prism.highlightElement(codeElement);

    // Display test cases (await loading and merging)
    displayTestCases(submission.test_results, submission.problem.id);
}

function getVerdictClass(verdict) {
    const verdictClasses = {
        'accepted': 'bg-success',
        'Wrong Answer': 'bg-danger',
        'Time Limit Exceeded': 'bg-warning text-dark',
        'Runtime Error': 'bg-danger',
    };
    return verdictClasses[verdict] || 'bg-secondary';
}

async function displayTestCases(testCases, problemId) {
    const testCasesList = document.getElementById('testCasesList');
    testCasesList.innerHTML = ''; // Clear existing content

    try {
        // Load all official problem test cases from API
        const allTestCases = await loadAllTestCases(problemId);

        console.log('Loaded all test cases:', allTestCases);
        console.log('Submission test cases:', testCases);
        // console.log(typeof testCases[0].id, typeof allTestCases[0].id);
        // console.log(testCases[0].id, allTestCases[0].id);

        // Merge testCases and allTestCases by matching id
        const mergedTestCases = testCases.map((tc, index) => {
            const extra = allTestCases[index] || {};
            return {
                ...tc,
                input_data: extra.input_data || null,
                output_data: extra.output_data || null,
                problem_id: extra?.problem?.id || null,
            };
        });

        console.log('Merged test cases:', mergedTestCases);

        // Render the merged test cases into the accordion list
        mergedTestCases.forEach((testCase, index) => {
            const input = testCase.input || testCase.input_data || 'No input available';
            const output = testCase.output || testCase.output_data || 'No output available';
            const expectedOutput = testCase.expected_output || testCase.output_data || '';

            const status = testCase.status ? 'Passed' : 'Failed';
            const statusClass = testCase.status ? 'text-success' : 'text-danger';

            const accordionItem = document.createElement('div');
            accordionItem.className = 'accordion-item';

            accordionItem.innerHTML = `
                <h2 class="accordion-header" id="heading${index}">
                    <button class="accordion-button ${testCase.status ? '' : 'collapsed'}" type="button" 
                        data-bs-toggle="collapse" data-bs-target="#testCase${index}" aria-expanded="${!!testCase.status}" aria-controls="testCase${index}">
                        Test Case #${index + 1} - <span class="${statusClass} ms-2">${status}</span>
                    </button>
                </h2>
                <div id="testCase${index}" class="accordion-collapse collapse ${testCase.status ? 'show' : ''}" aria-labelledby="heading${index}" data-bs-parent="#testCasesList">
                    <div class="accordion-body">
                        <div class="test-case-details">
                            <div class="test-case-input mb-3">
                                <h5>Input:</h5>
                                <pre><code>${escapeHtml(input)}</code></pre>
                            </div>
                            <div class="test-case-output">
                                <h5>Output:</h5>
                                <pre><code>${escapeHtml(output)}</code></pre>
                                ${testCase.status ? '' : `
                                <h5 class="mt-3">Expected Output:</h5>
                                <pre><code>${escapeHtml(expectedOutput)}</code></pre>`}
                            </div>
                        </div>
                    </div>
                </div>
            `;

            testCasesList.appendChild(accordionItem);
        });
    } catch (error) {
        showError('Failed to load test cases');
        console.error(error);
    }
}

function showError(message) {
    const container = document.querySelector('.verdict-container');
    const alert = document.createElement('div');
    alert.className = 'alert alert-danger';
    alert.role = 'alert';
    alert.innerHTML = escapeHtml(message);
    container.innerHTML = '';
    container.appendChild(alert);
}

async function loadAllTestCases(problemId) {
    try {
        const response = await APIService.getTestCaseVerdict(problemId);
        const testCases = response['test_cases'];
        console.log('All test cases from API:', testCases);
        return testCases;
    } catch (error) {
        showError('Failed to load test cases');
        console.error(error);
        return [];
    }
}
