import json
from Crawler import Crawler
from Scraper import Scraper, NotHTMLException
from urllib import parse
import sys

from INF8007Projet.Crawler import Crawler
from INF8007Projet.Scraper import Scraper, NotHTMLException

base_url = "https://spacejam.com"


# input_stdin: Page HTML à Crawler OU liste de sites Web à vérifier OU liste de fichiers à vérifier

# Type argument possibles pour std:in:
# - html
# - websites
# - files
# Argument url : url
# Argument fichier local : fichier

def main():
    stdin = sys.stdin.read()
    url, file, stdin, stdinval = None
    link_status_report = {}
    dict_arg = {}
    # Création d'un dictionnaire pour gérer les arguments
    for i in range(1, len(sys.argv), 2):
        try:
            dict_arg[sys.argv[i]] = sys.argv[i+1]
        except IndexError:
            print("Il manque un argument")      # Chaque argument doit avoir un nom et une valeur
            sys.exit()

    if stdin is not None:
        if stdinval.val == "html":
            scrape_and_crawl(stdin, "", link_status_report, {})
        elif stdinval.val == "filelist":
            all_checked_links = {}
            for file in stdin:
                with open(file, 'r') as f:
                    scrape_and_crawl(f.read(), file, link_status_report, all_checked_links)
        elif stdinval.val == "urllist":
            all_checked_links = {}
            for url in stdin:
                recursive_check(url, link_status_report, all_checked_links, base_url=url)
    elif url is not None:
        recursive_check(url, link_status_report, {}, base_url=url)
    elif file is not None:
        with open(file, 'r') as f:
            scrape_and_crawl(f.read(), file, link_status_report, {})

    with open('./link_status_report.json', 'w') as file:
        print(link_status_report)
        json.dump(link_status_report, file)

    # Gestion de la variable crawling_state
    try:
        if dict_arg['crawling'] == 'true' or dict_arg['crawling'] == 'True':
            crawling_state = True
        elif dict_arg['crawling'] == 'false' or dict_arg['crawling'] == 'False':
            crawling_state = False
        else:
            print("Quel est l'état du Crawling ? (True or False)")
            sys.exit()
    except KeyError:
        print("Il manque l'argument 'crawling' ")
        sys.exit()

    # Gestion de l'input du logiciel
    if 'url' in dict_arg and 'fichier' not in dict_arg and 'stdin' not in dict_arg:
        input_url = dict_arg['url']
        print("Url : ", input_url)
    elif 'fichier' in dict_arg and 'stdin' not in dict_arg and 'url' not in dict_arg:
        input_file = dict_arg['fichier']
        print("File : ", input_file)
    elif 'stdin' in dict_arg and 'fichier' not in dict_arg and 'url' not in dict_arg:
        type_stdin = dict_arg['stdin']
        print("Type du stdin : ", type_stdin)
    else:
        if len(dict_arg) > 2:
            print("Il y a trop d'arguments")
        else:
            print("Il n'y a pas assez d'argument ou typo dans le nom de l'argument")
        sys.exit()

def recursive_check(input_url: str, link_status_report: dict, all_checked_links: dict, base_url: str = "", crawling_state: bool = True):
    """
    Identify all the links in the page at the input url and recursively
    checks their status, and crawl those who are on the same domain as
    the base_url
    :param base_url:
    :param all_checked_links:
    :param crawling_state: Activer/ Désactiver le Crawling
    :param input_url:
    :param link_status_report:
    """
    print(input_url)
    input_page = Crawler.get_html(input_url)
    newly_checked_links, all_checked_links = scrape_and_crawl(input_page, input_url, link_status_report, all_checked_links)

    valid_links = filter(lambda link: link[1] == 200, newly_checked_links)

    if crawling_state is True:
        valid_links = filter(lambda link: link[1] == 200, checked_links)

        for link in valid_links:
            if link[0] in link_status_report.keys():
                continue
            if parse.urlparse(base_url).netloc in link[0]:  # Crawl only links on the same domain
                try:
                    recursive_check(input_url=link[0], link_status_report=link_status_report, crawling_state=True,
                                    checked_links=crawler.get_checked())
                except NotHTMLException:
                    print("link is not html page, skipping...")
                pass


def scrape_and_crawl(input_page: str, file_path: str, link_status_report: {}, all_checked_links: {}):
    scraper = Scraper()
    links = list(scraper.extract_links(input_page, file_path))
    crawler = Crawler(urls=links, checked=all_checked_links)
    crawler.crawl()
    checked_links = crawler.get_responses()
    link_status_report[file_path] = checked_links
    return checked_links, crawler.get_checked()


if __name__ == '__main__':
    main()
