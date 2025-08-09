// submissions.js
import APIService from './services/api.js';

document.addEventListener('DOMContentLoaded', async function () {
  const pagination = document.querySelector('.pagination');
  const tableBody = document.querySelector('tbody.submissions');
  if (!pagination || !tableBody) return;

  let currentPage = 1;
  let totalPages = 1;

  // Function to render submissions in table body
  function renderSubmissions(submissionsList) {
    tableBody.innerHTML = ''; // Clear existing rows

    if (!submissionsList || submissionsList.length === 0) {
      // Show no data row
      const noDataRow = document.createElement('tr');
      noDataRow.innerHTML = `<td colspan="6" class="text-center">No submissions found.</td>`;
      tableBody.appendChild(noDataRow);
      return;
    }

    submissionsList.forEach(submission => {
      const row = document.createElement('tr');

      const submittedAt = submission.created_at || submission.timestamp || '';
      const formattedDate = submittedAt ? new Date(submittedAt).toLocaleString() : 'N/A';

      const scoreDisplay = submission.score !== undefined && submission.score !== null ? submission.score : 'N/A';

      row.innerHTML = `
        <td>${submission.id}</td>
        <td>${submission.user?.username || 'N/A'}</td>
        <td>${submission.problem?.title || 'N/A'}</td>
        <td>${submission.status || 'N/A'}</td>
        <td>${scoreDisplay}</td>
        <td>${formattedDate}</td>
      `;
      tableBody.appendChild(row);
    });
  }

  // Function to render pagination links and bind events
  function renderPagination() {
    pagination.innerHTML = '';

    // Previous button
    const prevLi = document.createElement('li');
    prevLi.classList.add('page-item');
    if (currentPage === 1) prevLi.classList.add('disabled');
    prevLi.innerHTML = `<a class="page-link" href="#" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a>`;
    prevLi.addEventListener('click', (e) => {
      e.preventDefault();
      if (currentPage > 1) loadPage(currentPage - 1);
    });
    pagination.appendChild(prevLi);

    // Page numbers
    for (let i = 1; i <= totalPages; i++) {
      const pageLi = document.createElement('li');
      pageLi.classList.add('page-item');
      if (i === currentPage) pageLi.classList.add('active');
      pageLi.innerHTML = `<a class="page-link" href="#" data-page="${i}">${i}</a>`;
      pageLi.querySelector('a').addEventListener('click', (e) => {
        e.preventDefault();
        const pageNum = Number(e.target.dataset.page);
        if (pageNum !== currentPage) {
          loadPage(pageNum);
        }
      });
      pagination.appendChild(pageLi);
    }

    // Next button
    const nextLi = document.createElement('li');
    nextLi.classList.add('page-item');
    if (currentPage === totalPages) nextLi.classList.add('disabled');
    nextLi.innerHTML = `<a class="page-link" href="#" aria-label="Next"><span aria-hidden="true">&raquo;</span></a>`;
    nextLi.addEventListener('click', (e) => {
      e.preventDefault();
      if (currentPage < totalPages) loadPage(currentPage + 1);
    });
    pagination.appendChild(nextLi);
  }

  // Loads a specified page and updates UI
  async function loadPage(pageNum) {
    try {
        const response = await APIService.getSubmissions(null, pageNum);
        console.log(`Loaded submissions for page ${pageNum}:`, response);
        if (!response) throw new Error('No response from API');

        currentPage = response.current_page || pageNum;
        totalPages = response.total_pages || 1;

        renderSubmissions(response.solutions);
        renderPagination();

        // Optionally update URL without reload
        if (history.pushState) {
            const newUrl = new URL(window.location.href);
            newUrl.searchParams.set('page', currentPage);
            history.pushState(null, '', newUrl.toString());
        }
    } catch (error) {
        console.error('Error loading submissions for page', pageNum, error);
        tableBody.innerHTML = '<tr><td colspan="6" class="text-center">Failed to load submissions</td></tr>';
    }

  }

  // Initial load (check for query param 'page' in URL)
  const urlParams = new URLSearchParams(window.location.search);
  const initialPage = Number(urlParams.get('page')) || 1;
  await loadPage(initialPage);

  // Optional: Username filter
  const searchInput = document.getElementById('search-submissions');
  if (searchInput) {
    searchInput.addEventListener('input', function () {
      const filter = this.value.trim().toLowerCase();
      const rows = tableBody.querySelectorAll('tr');

      rows.forEach(row => {
        const usernameCell = row.querySelector('td:nth-child(2)');
        if (!usernameCell) return;

        const username = usernameCell.textContent.toLowerCase();
        row.style.display = username.includes(filter) ? '' : 'none';
      });
    });
  }
});
