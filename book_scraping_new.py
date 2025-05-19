import requests
import json
from bs4 import BeautifulSoup

class ScrapingBook:
    def __init__(self) -> None:
        self.base_url = "https://books.toscrape.com/catalogue/"
        self.start_url = self.base_url + "page-1.html"

    def get_html_source(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            return soup
        else:
            return None

    def scrape_all_pages(self):
        all_books = []
        for page in range(1, 51):  # There are 50 pages in total
            url = f"{self.base_url}page-{page}.html"
            soup = self.get_html_source(url)
            if not soup:
                print(f"Could not retrieve page: {url}")
                continue

            li_list = soup.find("ol", {"class": "row"}).find_all("li")

            for li in li_list:
                try:
                    title = li.article.h3.a["title"]
                    link = self.base_url + li.article.h3.a["href"]
                    price = li.find("p", class_="price_color").text
                    stars = li.find("p", class_="star-rating").get("class")[1] + " stars"

                    book = {
                        "bookName": title,
                        "bookLink": link,
                        "bookInfos": {
                            "book_price": price,
                            "book_star": stars
                        }
                    }
                    all_books.append(book)
                except Exception as e:
                    print(f"An error occurred: {e}")
                    continue

        return all_books

    def save_json(self, data):
        with open("books_new.json", "w", encoding="utf8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            print("✅ JSON file saved successfully.")


# Execution
scraper = ScrapingBook()
books = scraper.scrape_all_pages()
scraper.save_json(books)

print(f"Total number of books scraped: {len(books)}")

