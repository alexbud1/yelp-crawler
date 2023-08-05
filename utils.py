from bs4 import BeautifulSoup
import requests
from urllib.parse import parse_qs, quote, urlparse

# Function to scrape data from a given URL using css selectors(reviews)
def scrape_data_from_url(url, target_class):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        elements = soup.find_all(class_=target_class)
        scraped_data = [element.get_text(strip=True) for element in elements]
        return scraped_data
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching data from {url}: {e}")
        return None
    
def extract_website_from_url(url):
    print("Extracting website from URL")
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    # Check if the URL contains the 'redirect_url' parameter
    if 'redirect_url' in query_params:
        redirect_url = query_params['redirect_url'][0]
        parsed_redirect_url = urlparse(redirect_url)

        # Get the 'url' parameter from the redirected URL
        if 'url' in parse_qs(parsed_redirect_url.query):
            website_link = parse_qs(parsed_redirect_url.query)['url'][0]
            return website_link

    return None

# transform the city name to the format that Yelp uses
def encode_city_name(city_name):
    return quote(city_name)