import APIService from './services/api.js';

let editor;
let currentProblem;

document.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const problemId = urlParams.get('id');

    if (!problemId) {
        window.location.href = 'problems.html';
        return;
    }

    try {
        currentProblem = await APIService.getProblem(problemId);
        displayProblem(currentProblem);
        initializeEditor();
        setupEventListeners();
    } catch (error) {
        console.error('Error loading problem:', error);
        showError('Failed to load problem. Please try again later.');
    }
});

function displayProblem(problem) {
    document.getElementById('problemTitle').textContent = problem.title;
    const difficultyBadge = document.getElementById('problemDifficulty');
    difficultyBadge.textContent = problem.difficulty;
    difficultyBadge.className = `badge bg-${getDifficultyColor(problem.difficulty)}`;
    
    // Display problem description
    document.getElementById('problemDescription').innerHTML = problem.description;
    document.getElementById('inputFormat').innerHTML = `
        <div class="format-section">
            <h3>Input Format</h3>
            <div class="format-content">${problem.input_format}</div>
        </div>
    `;
    document.getElementById('outputFormat').innerHTML = `
        <div class="format-section">
            <h3>Output Format</h3>
            <div class="format-content">${problem.output_format}</div>
        </div>
    `;
    document.getElementById('constraints').innerHTML = `
        <div class="constraints-section">
            <h3>Constraints</h3>
            <div class="format-content">${problem.constraints}</div>
        </div>
    `;

    // Display sample tests
    displaySampleTests(problem.id);
}

async function displaySampleTests(problemId) {
    try {
        const sampleTests = await APIService.getSampleTests(problemId);
        const sampleInputElem = document.getElementById('sampleInput');
        const sampleOutputElem = document.getElementById('sampleOutput');

        // Clear previous content just in case
        if (sampleInputElem) sampleInputElem.textContent = '';
        if (sampleOutputElem) sampleOutputElem.textContent = '';

        const inputTestCases = sampleTests.input_test_cases || [];
        const outputTestCases = sampleTests.output_test_cases || [];

        if (inputTestCases.length === 0 || outputTestCases.length === 0) {
            if (sampleInputElem) sampleInputElem.textContent = 'No sample input available.';
            if (sampleOutputElem) sampleOutputElem.textContent = 'No sample output available.';
            return;
        }

        // Show all sample test cases
        for (const test of inputTestCases.map((input, index) => ({
            input: inputTestCases[index],
            output: outputTestCases[index]
        }))) {
            if (sampleInputElem && test.input !== undefined) {
                sampleInputElem.textContent += `${test.input}\n`;
            }

            if (sampleOutputElem && test.output !== undefined) {
                sampleOutputElem.textContent += `${test.output}\n`;
            }
        }

    } catch (error) {
        console.error('Error loading sample tests:', error);
        const sampleTestsContainer = document.getElementById('sampleTests');
        if (sampleTestsContainer) {
            sampleTestsContainer.innerHTML = `
                <div class="error-message">Failed to load sample tests</div>
            `;
        }
    }
}

function getDifficultyClass(difficulty) {
    const classes = {
        'EASY': 'badge-success',
        'MEDIUM': 'badge-warning',
        'HARD': 'badge-danger',
        'EXPERT': 'badge-dark'
    };
    return classes[difficulty.toUpperCase()] || 'badge-secondary';
}

function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function initializeEditor() {
    require(['vs/editor/editor.main'], function() {
        editor = monaco.editor.create(document.getElementById('editor'), {
            value: getTemplateCode('python'),
            language: 'python',
            theme: 'vs-dark',
            automaticLayout: true
        });

        // Language change handler
        document.getElementById('languageSelect').addEventListener('change', (e) => {
            const language = e.target.value;
            monaco.editor.setModelLanguage(editor.getModel(), language);
            editor.setValue(getTemplateCode(language));
        });
    });
}

function setupEventListeners() {
    document.getElementById('submitBtn').addEventListener('click', async () => {
        const code = editor.getValue();
        const language = document.getElementById('languageSelect').value;
        
        // Disable submit button and show loading state
        const submitBtn = document.getElementById('submitBtn');
        const originalText = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Submitting...';

        try {
            const result = await APIService.submitSolution(currentProblem.id, code, language);
            // Redirect to verdict page
            print(result);
            console.log('Submission result:', result);  
            window.location.href = `verdict.html?id=${result.solution_id}`;
        } catch (error) {
            console.error('Submission error:', error);
            showError('Failed to submit solution. Please try again.');
            // Reset submit button
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    });
}

function showResults(result) {
    const modalBody = document.getElementById('resultsBody');
    modalBody.innerHTML = `
        <div class="card ${result.status === 'Accepted' ? 'border-success' : 'border-danger'}">
            <div class="card-body">
                <h5 class="card-title ${result.status === 'Accepted' ? 'text-success' : 'text-danger'}">
                    ${result.status}
                </h5>
                <p class="card-text">
                    <strong>Time:</strong> ${result.execution_time}ms<br>
                    <strong>Memory:</strong> ${result.memory_used}MB
                </p>
                ${result.error_message ? `
                    <div class="alert alert-danger">
                        <pre class="mb-0">${result.error_message}</pre>
                    </div>
                ` : ''}
            </div>
        </div>
    `;
    
    const modal = new bootstrap.Modal(document.getElementById('resultsModal'));
    modal.show();
}

function getTemplateCode(language) {
    const templates = {
        python: `def solution():
    # Write your solution here
    pass

# Example usage
if __name__ == "__main__":
    solution()`,
        javascript: `function solution() {
    // Write your solution here
}

// Example usage
solution();`,
        java: `public class Solution {
    public static void main(String[] args) {
        // Write your solution here
    }
}`,
        cpp: `#include <iostream>
using namespace std;

int main() {
    // Write your solution here
    return 0;
}`
    };
    
    return templates[language] || '';
}

function getDifficultyColor(difficulty) {
    switch (difficulty.toLowerCase()) {
        case 'easy':
            return 'success';
        case 'medium':
            return 'warning';
        case 'hard':
            return 'danger';
        default:
            return 'secondary';
    }
}

function showError(message) {
    const container = document.querySelector('main.container-fluid');
    const alert = document.createElement('div');
    alert.className = 'alert alert-danger alert-dismissible fade show';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    container.insertBefore(alert, container.firstChild);
}

