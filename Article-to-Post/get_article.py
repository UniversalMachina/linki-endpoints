import requests


def get_news_articles(api_key, query, page_size=10):
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': query,
        'apiKey': api_key,
        'pageSize': page_size
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        articles = response.json().get('articles', [])
        return articles
    else:
        print(f"Failed to fetch articles: {response.status_code}")
        return []


# Example usage
api_key = '1e122eff2e0b493da33b20990695a541'  # Replace with your News API key
query = 'Artificial Intelligence'
articles = get_news_articles(api_key, query)

# Displaying the articles
for i, article in enumerate(articles, 1):
    print(f"{i}. {article['title']}")
    print(f"   Source: {article['source']['name']}")
    print(f"   URL: {article['url']}")
    print(f"   Published At: {article['publishedAt']}")
    print()


#llm to convert random text to prompt
#llm to convert random text to prompt

#function given a search it looks up articles and then have a blurb around it


#function take in article and write an article around it