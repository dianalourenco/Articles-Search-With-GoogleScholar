import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import random


# Keyword categories
ALGAE_KEYWORDS = [
    'algae', 'microalgae', 'cyanobacteria', 'diatoms']
PLASTIC_KEYWORDS = [
    'plastic', 'microplastic', 'polymeric materials']
DEGRADATION_KEYWORDS = [
    'degradation', 'biodegradation', 'degrade']


queries = []
def generate_queries():
    """Generate search query combinations."""
    queries = []
    for algae in ALGAE_KEYWORDS:
        for plastic in PLASTIC_KEYWORDS:
            for degradation in DEGRADATION_KEYWORDS:
                queries.append(f'{algae} {plastic} {degradation}')
    return queries

def find_articles(keyword):
    """Search for articles on Google Scholar."""
    headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.361681261652"
        }
    url = f"https://scholar.google.com/scholar?q={keyword.replace(' ', '+')}"
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    time.sleep(random.uniform(15,30))

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []

    for result in soup.select('.gs_r'):
        title_elem = result.select('.gs_rt')
        link_elem = result.select('.gs_rt a')

        # Only add articles that have title or link
        if title_elem or link_elem:
            title = title_elem[0].text.strip()
            link = link_elem[0]['href']
                
            # Skip if either title or link is empty after stripping
            if title or link:
                articles.append({
                    'title': title,
                    'url': link
                })

    print(f'\nFound {len(articles)} articles for query: {keyword}')

    return articles

def save_articles(articles, filename="articles.txt"):
    """Save articles to a text file."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("Retrieved Articles:\n\n")
        for i, article in enumerate(articles):
            f.write(f"{i}. Title: {article['title']}\n")
            f.write(f"   Link: {article['url']}\n\n")

def main():
    search_queries = generate_queries()
    all_articles = []
        
    for keyword in tqdm(search_queries, desc="Searching articles"):
        articles = find_articles(keyword)
        all_articles.extend(articles)    
    # Remove duplicates based on URL
    unique_articles = {article['url']: article for article in all_articles}.values()
    
    save_articles(list(unique_articles))

if __name__ == "__main__":
    main()