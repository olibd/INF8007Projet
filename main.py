import json
from Crawler import Crawler
from Scraper import Scraper, NotHTMLException
from urllib import parse
import sys

base_url = "https://spacejam.com"


# input_stdin: Page HTML à Crawler OU liste de sites Web à vérifier OU liste de fichiers à vérifier

# Type argument possibles pour std:in:
# - html
# - websites
# - files
# Argument url : url
# Argument fichier local : fichier

def main():
    link_status_report = {}
    dict_arg = {}
    # Création d'un dictionnaire pour gérer les arguments
    for i in range(1, len(sys.argv), 2):
        try:
            dict_arg[sys.argv[i]] = sys.argv[i + 1]
        except IndexError:
            sys.stderr.write("Il manque le nom ou la valeur d'un argument")  # Chaque argument doit avoir un nom et une valeur
            sys.exit()
    # Gestion de la variable crawling_state
    # Si pas d'argument spécifié, crawling_state = True
    try:
        if dict_arg['crawling'] == 'true' or dict_arg['crawling'] == 'True':
            crawling_state = True
        elif dict_arg['crawling'] == 'false' or dict_arg['crawling'] == 'False':
            crawling_state = False
        else:
            sys.stderr.write("Erreur : valeur variable crawling (true or false). Valeur prise par défaut : True")
        if len(dict_arg) > 2:
            sys.stderr.write("Erreur: Trop d'inputs")
        elif len(dict_arg) == 1:
            sys.stderr.write("Erreur: Pas d'inputs")
            sys.exit()
    except KeyError:
        if len(dict_arg) > 1:
            sys.stderr.write("Erreur: Trop d'inputs")
        sys.stderr.write("Erreur : variable crawling. Valeur prise par défaut : True")

    # Gestion de l'input du logiciel
    if 'url' in dict_arg:
        input_url = dict_arg['url']
        print("Url : ", input_url)
    elif 'fichier' in dict_arg:
        input_file = dict_arg['fichier']
        print("File : ", input_file)
    elif 'stdin' in dict_arg:
        type_stdin = dict_arg['stdin']
        print("Type du stdin : ", type_stdin)
    else:
        sys.stderr.write("Erreur: nom variable d'entrée (url ou fichier ou stdin)")
        sys.exit()

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
            if parse.urlparse(base_url).netloc in link[0]:  # Crawl only links on the same domain
                try:
                    recursive_check(input_url=link[0], link_status_report=link_status_report, crawling_state=True,
                                    checked_links=crawler.get_checked())
                except NotHTMLException:
                    print("link is not html page, skipping...")
                pass


if __name__ == '__main__':
    main()
