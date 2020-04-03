import json
from urllib import parse

import requests

from Crawler import Crawler
from Scraper import Scraper, NotHTMLException
from error_handling import *


# input stdin: Page HTML à Crawler OU liste de sites Web à vérifier OU liste de fichiers à vérifier

# Type argument possibles pour std:in:
# - html
# - urllist
# - filelist
# Argument url : url
# Argument fichier local : file
def main():
    url = None
    file = None
    stdin = None
    link_status_report = {}

    # Création d'un dictionnaire pour gérer les arguments
    dict_arg = {}
    for i in range(1, len(sys.argv), 2):
        try:
            if sys.argv[i] == "help":
                dict_arg[sys.argv[i]] = 0
            else:
                dict_arg[sys.argv[i]] = sys.argv[i + 1]
        except IndexError:
            error_print("Il manque un argument, chaque argument doit avoir un nom et une valeur")

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
            error_print("Il y a trop d'arguments")
        else:
            error_print("Il n'y a pas assez d'argument ou typo dans le nom de l'argument")

    # Scrape and crawl based on input type
    if stdin is not None:
        try:
            stdinvalue = sys.stdin.read()
        except Exception as ex:
            error_print("Error reading from the stdin. Please verify your query. ", ex)

        if stdin == "html":
            scrape_and_crawl(stdinvalue, "", link_status_report, {})
        elif stdin == "filelist":
            try:
                stdinvalue = json.loads(stdinvalue)
            except Exception as ex:
                error_print("Error loading filelist. Check the path and if this is valid JSON. ", ex)

            all_checked_links = {}
            for file in stdinvalue:
                try:
                    with open(file, 'r') as f:
                        scrape_and_crawl(f.read(), file, link_status_report, all_checked_links, is_local_file=True)
                except (IOError, OSError) as ex:
                    error_print("Skipping {}, moving on to the next because there was an error opening/reading "
                                "given file. ".format(file), ex, stop_script=False)
        elif stdin == "urllist":
            try:
                stdinvalue = json.loads(stdinvalue)
            except Exception as ex:
                error_print("Error loading urllist. Check the path and if this is valid JSON. ", ex)

            all_checked_links = {}
            for url in stdinvalue:
                try:
                    recursive_check_and_crawl(url, link_status_report, all_checked_links, base_url=url,
                                              crawling_state=crawling_state)
                except requests.exceptions.ConnectionError as ex:
                    error_print("Skipping {}, moving on to the next because there was an error connecting to "
                                "the supplied website. ".format(url), ex, stop_script=False)
                except requests.exceptions.InvalidURL as ex:
                    error_print("Skipping {}, moving on to the next because there was an invalid url "
                                "supplied. ".format(url), ex, stop_script=False)
                except requests.exceptions.InvalidSchema:
                    error_print("Skipping {}, moving on to the next because there was an invalid schema "
                                "for url. ".format(url), stop_script=False)
                except requests.exceptions.MissingSchema as ex:
                    # relative link with no base url
                    error_print("Skipping {}, moving on to the next because there was is a missing "
                                "schema. ".format(url),
                                ex, stop_script=False)
        else:
            error_print("Invalid stdin value '{}', should be html|urllist|filelist".format(stdin))
    elif url is not None:
        try:
            recursive_check_and_crawl(url, link_status_report, {}, base_url=url, crawling_state=crawling_state)
        except requests.exceptions.ConnectionError as e:
            error_print("Error connecting to the supplied website. ", e)
        except requests.exceptions.InvalidURL as e:
            error_print("Invalid url supplied. ", e)
        except requests.exceptions.InvalidSchema:
            error_print("Invalid schema for url. ")
        except requests.exceptions.MissingSchema as e:
            # relative link with no base url
            error_print("Missing schema. ", e)
    elif file is not None:
        try:
            with open(file, 'r') as f:
                scrape_and_crawl(f.read(), "", link_status_report, {}, is_local_file=True)
        except (IOError, OSError) as ex:
            error_print("Error opening/reading given file. ", ex)

    with open('./link_status_report.json', 'w') as file:
        json.dump(link_status_report, file)


# Fonction pure
def check_crawling_state(dict_arg: dict):
    # Gestion de la variable crawling_state
    try:
        if dict_arg['crawling'] == 'true' or dict_arg['crawling'] == 'True':
            crawling_state = True
        elif dict_arg['crawling'] == 'false' or dict_arg['crawling'] == 'False':
            crawling_state = False
        else:
            print("Warning: invalid value supplied for 'crawling', using default value (true)")
            crawling_state = True
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
    try:
        main()
    except Exception as e:
        error_print(exception=e)
