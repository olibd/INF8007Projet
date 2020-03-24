import json
from Crawler import Crawler
from Scraper import Scraper, NotHTMLException
from urllib import parse
import sys
base_url = "https://spacejam.com"

# input_stdin: Page HTML à Crawler OU liste de sites Web à vérifier OU liste de fichiers à vérifier

# Type argument possibles :
# - html
# - websites
# - files

def main():
    link_status_report = {}
    input_stdin = sys.argv[1]
    type_stdin = sys.argv[2]
    if type_stdin == 'html':
        # page html à Crawler
    elif type_stdin == 'websites':
        # liste de sites web à vérifier
    elif type_stdin == 'files':
        # liste de fichiers à vérifier
    # recursive_check(input_url=base_url, input_file="", link_status_report=link_status_report,
    #                 crawling_state=True, checked_links={})
    # with open('./link_status_report.json', 'w') as file:
    #     print(link_status_report)
    #     json.dump(link_status_report, file)


def recursive_check(input_url: str, input_file: str, crawling_state: bool, link_status_report: dict,
                    checked_links: dict):
    """
    Identify all the links in the page at the input url and recursively
    checks their status, and crawl those who are on the same domain as
    the base_url
    :param crawling_state: Activer/ Désactiver le Crawling
    :param checked_links:
    :param input_file:
    :param input_url:
    :param link_status_report:
    """

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
            if parse.urlparse(base_url).netloc in link[0]: # Crawl only links on the same domain
                try:
                    recursive_check(input_url=link[0], link_status_report=link_status_report, crawling_state=True,
                                    checked_links=crawler.get_checked())
                except NotHTMLException:
                    print("link is not html page, skipping...")
                pass


if __name__ == '__main__':
    main()



