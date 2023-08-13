import requests
from bs4 import BeautifulSoup
import csv
import concurrent.futures

def get_user_agent():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    return user_agent

def get_search_results(search_query, page=1, user_agent=None):
    headers = {
        "User-Agent": user_agent if user_agent else "Your Default User Agent",
    }

    params = {
        "q": search_query,
        "start": (page - 1) * 10,
    }

    response = requests.get("https://www.google.com/search", headers=headers, params=params)
    if response.status_code == 200:
        return response.content

def extract_links_from_results(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    links = []
    for result in soup.find_all("a"):
        link = result.get("href")
        if link.startswith("http"):
            links.append(link)
    return links

def scrape_search_results(search_query, page):
    user_agent = get_user_agent()
    search_results_page = get_search_results(search_query, page, user_agent)
    links = extract_links_from_results(search_results_page)
    return links

def scrape_champion_hoodies_sites():
    search_query = "Champion hoodies for sale"
    num_pages = 5
    max_threads = 5  # Number of threads for concurrent scraping

    all_links = []
    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        future_to_page = {executor.submit(scrape_search_results, search_query, page): page for page in range(1, num_pages + 1)}
        for future in concurrent.futures.as_completed(future_to_page):
            page = future_to_page[future]
            try:
                links = future.result()
                all_links.extend(links)
            except Exception as e:
                print(f"Error scraping page {page}: {e}")

    return all_links

def save_links_to_csv(links, filename):
    with open(filename, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Website URL"])
        for link in links:
            csv_writer.writerow([link])

if __name__ == "__main__":
    scraped_links = scrape_champion_hoodies_sites()
    save_links_to_csv(scraped_links, "champion_hoodies_sites.csv")
