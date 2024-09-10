from scraper.quotes_spider import QuotesSpider

def main():
    spider = QuotesSpider()
    spider.scrape_quotes_and_authors()
    spider.save_to_json()

if __name__ == "__main__":
    main()
