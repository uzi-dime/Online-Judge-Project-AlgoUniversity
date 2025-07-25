import json
import sys
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup

def setup_driver(headless=True):
    try:
        options = Options()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        # Change this path to your installed chromedriver binary location
        service = ChromeService(executable_path="/usr/local/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        tb = traceback.format_exc()
        raise RuntimeError(f"Error setting up ChromeDriver: {e}\nTraceback:\n{tb}") from e

def scrape_problemset():
    driver = None
    try:
        driver = setup_driver()
        driver.get("https://cses.fi/problemset/")
        driver.implicitly_wait(5)  # wait for elements to load

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        problems = []
        # print(soup.text)
        task_tables = soup.find_all('ul', class_='task-list')[1:]  # skip the first ul
        if not task_tables:
            raise RuntimeError("Failed to find any task lists on the page.")

        for table in task_tables:
            heading = table.find_previous('h2')
            category = heading.text.strip() if heading else "Unknown"
            rows = table.find_all('li')
            if not rows:
                continue  # no problems in this category, skip

            for row in rows:
                link = row.find('a')
                if not link:
                    continue
                problem_id = link['href'].split('/')[-1]
                problem_name = link.text.strip()
                solved_span = row.find('span', class_='detail')
                solved_count = solved_span.text.strip() if solved_span else "0"
                problems.append({
                    'category': category,
                    'id': problem_id,
                    'name': problem_name,
                    'solved_count': solved_count,
                    'url': f"https://cses.fi{link['href']}"
                })
        return problems

    except Exception as e:
        tb = traceback.format_exc()
        raise RuntimeError(f"Error scraping problem set: {e}\nTraceback:\n{tb}") from e

    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    try:
        problems = scrape_problemset()
        with open('cses_problems.json', 'w', encoding='utf-8') as f:
            json.dump(problems, f, indent=2, ensure_ascii=False)
        print(f"Scraped {len(problems)} problems. Saved to cses_problems.json")
    except Exception as e:
        print(f"Failed: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
