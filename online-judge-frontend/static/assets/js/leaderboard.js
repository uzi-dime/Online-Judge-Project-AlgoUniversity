// leaderboard.js
import APIService from './services/api.js';




async function fetchAllSolutions(page = 1, allSolutions = []) {
  try {
    console.log(`Fetching solutions for page ${page}...`);
    const response = await APIService.getSubmissions(null, page);
    // if (!response.ok) throw new Error('Failed to fetch solutions');
    // const data = await response.json();
    console.log(`Fetched page ${page}:`, response);
    allSolutions = allSolutions.concat(response.solutions);

    if (response.current_page < response.total_pages) {
      // Fetch next page recursively
      return fetchAllSolutions(page + 1, allSolutions);
    }
    return allSolutions;
  } catch (error) {
    throw error;
  }
}

// This will now count unique problems solved per user
function processLeaderboard(solutions) {
  // Map from userId to { username, problems: Set of problemIds }
  const userMap = new Map();

  solutions.forEach(sol => {
    if (sol.status && sol.status.toLowerCase() === 'accepted') {
      const userId = sol.user.id;
      const username = sol.user.username;
      const problemId = sol.problem.id;

      if (!userMap.has(userId)) {
        userMap.set(userId, { username, problems: new Set() });
      }
      userMap.get(userId).problems.add(problemId);
    }
  });

  // Convert to array and count unique problems
  return Array.from(userMap.entries()).map(([userId, obj]) => ({
    userId,
    username: obj.username,
    problemsSolved: obj.problems.size
  }));
}

function renderLeaderboard(users) {
  const tbody = document.getElementById('hallOfFameBody');
  if (!tbody) {
    console.error('Element with id "hallOfFameBody" not found');
    return;
  }
  
  tbody.innerHTML = '';
  console.log('Rendering leaderboard with users:', users);
  if (users.length === 0) {
    tbody.innerHTML = '<tr><td colspan="3" class="text-center">No accepted solutions found.</td></tr>';
    return;
  }

  users.forEach((user, index) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${index + 1}</td>
      <td>${user.username}</td>
      <td>${user.problemsSolved}</td>
    `;
    tbody.appendChild(tr);
  });
}

async function loadLeaderboard() {
  const loadingMsg = document.getElementById('loadingMessage');
  const errorMsg = document.getElementById('errorMessage');
  if (loadingMsg) loadingMsg.style.display = 'block';
  if (errorMsg) errorMsg.style.display = 'none';

  try {
    const allSolutions = await fetchAllSolutions();
    console.log('All solutions fetched:', allSolutions);
    const users = processLeaderboard(allSolutions);

    // Sort descending by problemsSolved, then username (alphabetical)
    users.sort((a, b) => b.problemsSolved - a.problemsSolved || a.username.localeCompare(b.username));
    renderLeaderboard(users);
  } catch (error) {
    if (errorMsg) {
      errorMsg.textContent = 'Failed to load leaderboard: ' + error.message;
      errorMsg.style.display = 'block';
    }
  } finally {
    if (loadingMsg) loadingMsg.style.display = 'none';
  }
}

window.addEventListener('DOMContentLoaded', loadLeaderboard);
