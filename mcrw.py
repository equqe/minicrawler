from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import os

def get_all_routes(url, visited=None):
    if visited is None:
        visited = set()

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return visited

    soup = BeautifulSoup(response.text, 'html.parser')
    base_url = "{0.scheme}://{0.netloc}".format(urlparse(url))

    for link in soup.find_all('a', href=True):
        href = link.get('href')
        full_url = urljoin(base_url, href)

        if full_url not in visited and base_url in full_url:
            visited.add(full_url)
            get_all_routes(full_url, visited)

    return visited

def save_routes_to_file(url, routes):
    date_str = datetime.now().strftime("%m_%d_%y")
    filename = f"{urlparse(url).netloc}_{date_str}.txt"

    with open(filename, 'w') as file:
        for route in routes:
            file.write(route + '\n')

    print(f"Routes saved to {filename}")

def main():
    url = input("address: ")
    routes = get_all_routes(url)
    save_routes_to_file(url, routes)

if __name__ == "__main__":
    main()
