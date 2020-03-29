import json
import sys
from urllib import parse

from Crawler import Crawler
from Scraper import Scraper, NotHTMLException


# input_stdin: Page HTML à Crawler OU liste de sites Web à vérifier OU liste de fichiers à vérifier

# Type argument possibles pour std:in:
# - html
# - websites
# - files
# Argument url : url
# Argument fichier local : fichier

def main():
    url = None
    file = None
    stdin = None
    link_status_report = {}
    dict_arg = {}
    # Création d'un dictionnaire pour gérer les arguments
    for i in range(1, len(sys.argv), 2):
        try:
            dict_arg[sys.argv[i]] = sys.argv[i + 1]
        except IndexError:
            print("Il manque un argument, chaque argument doit avoir un nom et une valeur")
            print_help()
            sys.exit()

    # Gestion de l'input du logiciel
    if "help" in dict_arg:
        print_help()
    elif 'url' in dict_arg and 'file' not in dict_arg and 'stdin' not in dict_arg:
        url = dict_arg['url']
        crawling_state = check_crawling_state(dict_arg)
    elif 'file' in dict_arg and 'stdin' not in dict_arg and 'url' not in dict_arg:
        file = dict_arg['file']
    elif 'stdin' in dict_arg and 'file' not in dict_arg and 'url' not in dict_arg:
        stdin = dict_arg['stdin']
        if stdin == "urllist":
            crawling_state = check_crawling_state(dict_arg)
    else:
        if len(dict_arg) > 2:
            print("Il y a trop d'arguments")
            print_help()
        else:
            print("Il n'y a pas assez d'argument ou typo dans le nom de l'argument")
            print_help()
        sys.exit()

    if stdin is not None:
        stdinvalue = sys.stdin.read()
        if stdin == "html":
            scrape_and_crawl(stdinvalue, "", link_status_report, {})
        elif stdin == "filelist":
            all_checked_links = {}
            stdinvalue = json.loads(stdinvalue)
            for file in stdinvalue:
                with open(file, 'r') as f:
                    scrape_and_crawl(f.read(), file, link_status_report, all_checked_links, is_local_file=True)
        elif stdin == "urllist":
            stdinvalue = json.loads(stdinvalue)
            all_checked_links = {}
            for url in stdinvalue:
                recursive_check_and_crawl(url, link_status_report, all_checked_links, base_url=url,
                                          crawling_state=crawling_state)
    elif url is not None:
        recursive_check_and_crawl(url, link_status_report, {}, base_url=url, crawling_state=crawling_state)
    elif file is not None:
        with open(file, 'r') as f:
            scrape_and_crawl(f.read(), "", link_status_report, {}, is_local_file=True)

    with open('./link_status_report.json', 'w') as file:
        json.dump(link_status_report, file)


def print_help():
    print("----------------------------------------------")
    print("Usage examples:")
    print("main.py url http://google.com")
    print("main.py url http://google.com crawling false")
    print("main.py file /path/to/file.html")
    print("main.py stdin html|filelist|urllist:")
    print("   echo [\\\"https://spacejam.com\\\"] | python main.py stdin urllist")
    print("   echo [\\\"./tests/spacejam.html\\\"] | python main.py stdin filelist")
    print("   echo \<html\>\<a href=\\\"https://spacejam.com\\\"\>\</html\> | python main.py stdin html")
    print("----------------------------------------------")
    print("Parameter details:")
    print("help -> shows this message")
    print("url -> string url")
    print("file -> string path to a file")
    print("stdin -> accepted values are:")
    print("   html -> will tell the program to expect html in the stdin")
    print("   filelist -> will tell the program expect a JSON array of file paths in the stdin")
    print("   urllist -> will tell the program expect a JSON array of urls in the stdin")
    print("!!!! NOTE: url, file, and stdin are mutually exclusive. You must only use one of them.")
    print("crawling -> true (default) or false. (can be capitalized) To be used whenever the program reads URLs")
    print("----------------------------------------------")


def check_crawling_state(dict_arg):
    # Gestion de la variable crawling_state
    try:
        if dict_arg['crawling'] == 'true' or dict_arg['crawling'] == 'True':
            crawling_state = True
        elif dict_arg['crawling'] == 'false' or dict_arg['crawling'] == 'False':
            crawling_state = False
        else:
            print("Quel est l'état du Crawling ? (True or False)")
            print_help()
            sys.exit()
    except KeyError:
        crawling_state = True
    return crawling_state


def recursive_check_and_crawl(input_url: str, link_status_report: dict, all_checked_links: dict, base_url: str = "",
                              crawling_state: bool = True):
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
    newly_checked_links, all_checked_links = scrape_and_crawl(input_page, input_url, link_status_report,
                                                              all_checked_links)

    if crawling_state is True:
        valid_links = filter(lambda link: link[1] == 200, newly_checked_links)

        for link in valid_links:
            if link[0] in link_status_report.keys():
                continue
            if parse.urlparse(base_url).netloc in link[0]:  # Crawl only links on the same domain
                try:
                    recursive_check_and_crawl(input_url=link[0], link_status_report=link_status_report,
                                              all_checked_links=all_checked_links, base_url=base_url)
                except NotHTMLException:
                    print("link is not html page, skipping...")


def scrape_and_crawl(input_page: str, file_path: str, link_status_report: dict = {}, all_checked_links: dict = {},
                     is_local_file: bool = False):
    scraper = Scraper()
    if is_local_file:
        links = list(scraper.extract_links(input_page, ""))
    else:
        links = list(scraper.extract_links(input_page, file_path))
    crawler = Crawler(urls=links, checked=all_checked_links)
    crawler.crawl()
    checked_links = crawler.get_responses()
    link_status_report[file_path] = checked_links
    return checked_links, crawler.get_checked()


if __name__ == '__main__':
    main()
