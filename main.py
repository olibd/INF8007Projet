import json

from INF8007Projet.Crawler import Crawler
from INF8007Projet.Scraper import Scraper, NotHTMLException
from urllib import parse

base_url = "https://www.fogcam.org/"

def main():
    link_status_report = {}
    recursive_check(base_url, link_status_report)
    with open('./link_status_report.json', 'w') as file:
        print(link_status_report)
        json.dump(link_status_report, file)


def recursive_check(input_url: str, link_status_report: dict):
    print(input_url)
    input_page = Crawler.get_html(input_url)
    scraper = Scraper()
    links = list(scraper.extract_links(input_page))
    crawler = Crawler(links, base_url=input_url)
    crawler.crawl()
    checked_links = crawler.get_responses()

    link_status_report[input_url] = checked_links

    valid_links = filter(lambda link: link[1] == 200, checked_links)

    for link in valid_links:
        if parse.urlparse(base_url).netloc in link[0]:
            try:
                recursive_check(link[0], link_status_report)
            except NotHTMLException:
                print("link is not html page, skipping...")
                pass

if __name__ == '__main__':
    main()
