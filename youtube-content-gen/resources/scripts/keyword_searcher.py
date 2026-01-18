import requests
from bs4 import BeautifulSoup
import urllib.parse

def search_videos_by_keyword(keyword: str) -> list:
    """
    Searches for YouTube videos based on a keyword using a simple Google scraping approach
    (Note: In production, use YouTube Data API or SerpAPI for reliability).
    """
    print(f"Searching for videos related to: {keyword}...")
    
    # Construct a search query (site:youtube.com "devil hunter")
    query = f'site:youtube.com "Devil Hunter" {keyword}'
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={encoded_query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        # Basic parsing of Google results (selectors change often, this is heuristic)
        for g in soup.find_all('div', class_='g'):
            anchors = g.find_all('a')
            if anchors:
                link = anchors[0]['href']
                title = g.find('h3').text if g.find('h3') else "Unknown Title"
                
                if 'youtube.com/watch' in link:
                    # Clean up URL params
                    if '&' in link:
                         link = link.split('&')[0]
                    
                    results.append({
                        "title": title,
                        "url": link,
                        "source": "google"
                    })
                    
        return results[:5] # Return top 5
    except Exception as e:
        print(f"Error during search: {e}")
        return []
