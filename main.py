import json

from INF8007Projet.Crawler import Crawler
from INF8007Projet.Scraper import Scraper, NotHTMLException
from urllib import parse

base_url = "https://spacejam.com"

def main():
    link_status_report = {}
    recursive_check(input_url=base_url, input_file="", input_stdin="", link_status_report=link_status_report,
                    crawling_state=True, checked_links={})
    with open('./link_status_report.json', 'w') as file:
        print(link_status_report)
        json.dump(link_status_report, file)


def recursive_check(input_url: str, input_file: str, input_stdin: str, crawling_state: bool, link_status_report: dict, checked_links: dict):
    """
    Identify all the links in the page at the input url and recursively
    checks their status, and crawl those who are on the same domain as
    the base_url
    :param input_url:
    :param link_status_report:
    """
    if input_url != "":
        print(input_url)
        input_page = Crawler.get_html(input_url)
    if input_file != "":
        input_page = input_file
    else:
        return ("Pas d'input")

    scraper = Scraper()
    links = list(scraper.extract_links(input_page, input_url))
    crawler = Crawler(urls=links, checked=checked_links)
    crawler.crawl()
    checked_links = crawler.get_responses()

    link_status_report[input_url] = checked_links

    if crawling_state is True:
        valid_links = filter(lambda link: link[1] == 200, checked_links)

        for link in valid_links:
            if link[0] in link_status_report.keys():
                continue
            if parse.urlparse(base_url).netloc in link[0]: #crawl only links on the same domain
                try:
                    recursive_check(input_url=link[0], link_status_report=link_status_report, crawling_state=True,
                                    checked_links=crawler.get_checked())
                except NotHTMLException:
                    print("link is not html page, skipping...")
                pass


if __name__ == '__main__':
    main()
    print()