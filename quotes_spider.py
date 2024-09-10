import requests
from bs4 import BeautifulSoup
import json
import os

class QuotesSpider:
    def __init__(self, base_url="http://quotes.toscrape.com"):
        self.base_url = base_url
        self.quotes = []
        self.authors = {}

    def scrape_quotes_and_authors(self):
        page = 1
        while True:
            response = requests.get(f"{self.base_url}/page/{page}/")
            soup = BeautifulSoup(response.text, "html.parser")
            quote_elements = soup.find_all("div", class_="quote")

            if not quote_elements:
                break

            for element in quote_elements:
                text = element.find("span", class_="text").get_text()
                author_name = element.find("small", class_="author").get_text()
                tags = [tag.get_text() for tag in element.find_all("a", class_="tag")]

                self.quotes.append({
                    "quote": text,
                    "author": author_name,
                    "tags": tags
                })

                if author_name not in self.authors:
                    author_url = element.find("a")["href"]
                    author_response = requests.get(f"{self.base_url}{author_url}")
                    author_soup = BeautifulSoup(author_response.text, "html.parser")

                    author_birth_date = author_soup.find("span", class_="author-born-date").get_text()
                    author_birth_place = author_soup.find("span", class_="author-born-location").get_text()
                    author_description = author_soup.find("div", class_="author-description").get_text().strip()

                    self.authors[author_name] = {
                        "name": author_name,
                        "birth_date": author_birth_date,
                        "birth_place": author_birth_place,
                        "description": author_description
                    }

            page += 1

    def save_to_json(self, quotes_file_path="data/quotes.json", authors_file_path="data/authors.json"):
        os.makedirs(os.path.dirname(quotes_file_path), exist_ok=True)

        with open(quotes_file_path, "w", encoding="utf-8") as quotes_file:
            json.dump(self.quotes, quotes_file, ensure_ascii=False, indent=4)

        with open(authors_file_path, "w", encoding="utf-8") as authors_file:
            json.dump(list(self.authors.values()), authors_file, ensure_ascii=False, indent=4)
