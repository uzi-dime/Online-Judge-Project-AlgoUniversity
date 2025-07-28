import APIService from './services/api.js';

document.addEventListener('DOMContentLoaded', async () => {
    try {
        const problems = await APIService.getProblems();
        console.log('Problems loaded:', problems);

        if (!Array.isArray(problems.problems)) {
        console.error('Expected response.problems to be an array');
        showError('No problems to display.');
        return;
        }

        displayProblems(problems.problems);
        console.log('Problems loaded:', problems);
        // displayProblems(problems);
    } catch (error) {
        console.error('Error loading problems:', error);
        showError('Failed to load problems. Please try again later.');
    }
});

function displayProblems(problems) {
  const problemsList = document.getElementById('problemsList');

  problemsList.innerHTML = problems.map(problem => `
    <tr>
      <td>${problem.id}</td>
      <td>${problem.title}</td>
      <td>
        <span class="badge bg-${getDifficultyColor(problem.difficulty)}">
          ${problem.difficulty}
        </span>
      </td>
      <td>
        <a href="problem-detail.html?id=${problem.id}" class="btn btn-primary btn-sm">Solve</a>
      </td>
    </tr>
  `).join('');
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
    const container = document.querySelector('main.container');
    const alert = document.createElement('div');
    alert.className = 'alert alert-danger alert-dismissible fade show';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    container.insertBefore(alert, container.firstChild);
}
